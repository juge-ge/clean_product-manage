from typing import AsyncGenerator, Optional, List, Literal, Any

import json
import httpx
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse

from app.settings import settings


router = APIRouter()


async def _stream_gitee_openai(
    messages: List[dict],
    model: str,
    temperature: float,
    top_p: float,
    max_tokens: int,
    stream: bool,
    extra_body: Optional[dict] = None,
) -> AsyncGenerator[bytes, None]:
    url = f"{settings.AI_API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json",
        # 明确声明希望使用 SSE 流
        "Accept": "text/event-stream, application/json",
    }
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": stream,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "frequency_penalty": 1,
    }
    if extra_body:
        payload["extra_body"] = extra_body

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, headers=headers, json=payload) as resp:
            resp.raise_for_status()
            # 如果不是 event-stream，直接读取全部 JSON 后一次性输出
            content_type = resp.headers.get("content-type", "")
            if "text/event-stream" not in content_type:
                full = await resp.aread()
                try:
                    data = json.loads(full)
                    if data and "choices" in data and data["choices"]:
                        choice0 = data["choices"][0]
                        # 非流式：message.content
                        message = choice0.get("message") or {}
                        content = message.get("content")
                        if content:
                            yield content.encode("utf-8")
                        else:
                            # 兼容某些服务直接返回 content 字段
                            content2 = choice0.get("text") or choice0.get("content")
                            if content2:
                                yield str(content2).encode("utf-8")
                except Exception:
                    # 无法解析则回传原文
                    if full:
                        yield full
                return

            async for line in resp.aiter_lines():
                if not line:
                    continue
                # OpenAI 兼容流："data: {json}"
                if line.startswith("data: "):
                    data_str = line[len("data: ") :].strip()
                else:
                    data_str = line.strip()

                if data_str == "[DONE]":
                    break

                try:
                    data = json.loads(data_str)
                except Exception:
                    # 直接将原始行透传，防御式处理
                    yield (data_str + "\n").encode("utf-8")
                    continue

                if not data or "choices" not in data or not data["choices"]:
                    continue

                choice0 = data["choices"][0]
                delta = choice0.get("delta") or {}
                # reasoning_content 或 content 二选一
                chunk = delta.get("reasoning_content") or delta.get("content")
                if not chunk:
                    # 兼容一些服务把数据放到 message.content
                    message = choice0.get("message") or {}
                    chunk = message.get("content")
                if chunk:
                    yield chunk.encode("utf-8")


@router.post("/chat", summary="AI 聊天流式接口")
async def chat(
    messages: List[dict] = Body(..., description="OpenAI 格式的 messages"),
    model: str = Body("gpt-oss-120b"),
    temperature: float = Body(0.7),
    top_p: float = Body(0.7),
    max_tokens: int = Body(1024),
    stream: bool = Body(True),
    extra_body: Optional[dict] = Body({}),
):
    async def generator():
        async for chunk in _stream_gitee_openai(
            messages=messages,
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=stream,
            extra_body=extra_body or None,
        ):
            yield chunk

    return StreamingResponse(
        generator(),
        media_type="text/event-stream; charset=utf-8",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


