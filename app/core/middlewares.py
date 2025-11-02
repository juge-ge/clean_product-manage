import json
import re
import urllib.parse
from datetime import datetime
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.dependency import AuthControl
from app.models.admin import AuditLog, User

from .bgtask import BgTasks


class SimpleBaseMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        response = await self.before_request(request) or self.app
        await response(request.scope, request.receive, send)
        await self.after_request(request)

    async def before_request(self, request: Request):
        return self.app

    async def after_request(self, request: Request):
        return None


class BackGroundTaskMiddleware(SimpleBaseMiddleware):
    async def before_request(self, request):
        await BgTasks.init_bg_tasks_obj()

    async def after_request(self, request):
        await BgTasks.execute_tasks()


class HttpAuditLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, methods: list[str], exclude_paths: list[str]):
        super().__init__(app)
        self.methods = methods
        self.exclude_paths = exclude_paths
        self.audit_log_paths = ["/api/v1/auditlog/list"]
        self.max_body_size = 1024 * 1024  # 1MB 响应体大小限制

    async def get_request_args(self, request: Request) -> dict:
        args = {}
        # 获取查询参数
        for key, value in request.query_params.items():
            args[key] = value

        # 获取请求体
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
                # 只有当body是字典时才更新args，如果是列表（如批量操作），则跳过
                if isinstance(body, dict):
                    args.update(body)
                # 如果是列表，为了审计日志记录，可以添加一个标记
                elif isinstance(body, list):
                    args["_batch_data"] = True
                    args["_batch_count"] = len(body)
            except json.JSONDecodeError:
                try:
                    body = await request.form()
                    # args.update(body)
                    for k, v in body.items():
                        if hasattr(v, "filename"):  # 文件上传行为
                            args[k] = v.filename
                        elif isinstance(v, list) and v and hasattr(v[0], "filename"):
                            args[k] = [file.filename for file in v]
                        else:
                            args[k] = v
                except Exception:
                    pass

        return args

    async def get_response_body(self, request: Request, response: Response) -> Any:
        # 检查是否为文件下载响应（通过content-type或content-disposition判断）
        content_type = response.headers.get("content-type", "").lower()
        content_disposition = response.headers.get("content-disposition", "").lower()
        
        # 检查是否是文件下载（通过content-disposition中的attachment判断）
        is_file_download = "attachment" in content_disposition
        
        file_content_types = [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # Word文档
            "application/msword",  # 旧版Word
            "application/pdf",  # PDF
            "application/octet-stream",  # 二进制流
            "application/zip",  # ZIP
            "application/x-zip-compressed",  # ZIP压缩
            "image/",  # 所有图片类型
            "video/",  # 所有视频类型
            "audio/",  # 所有音频类型
        ]
        
        # 如果是文件下载，直接返回简单标记，不解析body（避免读取二进制数据）
        if is_file_download or any(ct in content_type for ct in file_content_types):
            filename = response.headers.get("content-disposition", "")
            if "filename=" in filename or "filename*=" in filename:
                try:
                    # 提取文件名（支持UTF-8编码的文件名）
                    if "filename*=" in filename:
                        filename_part = filename.split("filename*=")[1].split(";")[0]
                        # 移除UTF-8编码前缀
                        if filename_part.startswith("utf-8''"):
                            filename_part = filename_part[7:]
                    else:
                        filename_part = filename.split("filename=")[1].split(";")[0].strip('"\'')
                    # URL解码
                    try:
                        filename_part = urllib.parse.unquote(filename_part)
                    except:
                        pass
                    return {"code": 200, "msg": "File download", "data": {"filename": filename_part}}
                except Exception:
                    pass
            return {"code": 200, "msg": "File download", "data": None}
        
        # 检查Content-Length（对于非文件响应）
        content_length = response.headers.get("content-length")
        if content_length and int(content_length) > self.max_body_size:
            return {"code": 0, "msg": "Response too large to log", "data": None}

        # 尝试获取响应体（仅用于非文件响应）
        try:
            if hasattr(response, "body"):
                body = response.body
            else:
                body_chunks = []
                async for chunk in response.body_iterator:
                    if not isinstance(chunk, bytes):
                        chunk = chunk.encode(response.charset) if hasattr(response, "charset") else chunk.encode('utf-8')
                    body_chunks.append(chunk)

                response.body_iterator = self._async_iter(body_chunks)
                body = b"".join(body_chunks)
        except Exception as e:
            # 如果读取响应体失败（可能是文件响应），返回简单标记
            return {"code": response.status_code, "msg": "Response body read failed", "data": None}

        if any(request.url.path.startswith(path) for path in self.audit_log_paths):
            try:
                data = self.lenient_json(body)
                # 只保留基本信息，去除详细的响应内容
                if isinstance(data, dict):
                    data.pop("response_body", None)
                    if "data" in data and isinstance(data["data"], list):
                        for item in data["data"]:
                            item.pop("response_body", None)
                return data
            except Exception:
                return None

        return self.lenient_json(body)

    def lenient_json(self, v: Any) -> Any:
        if isinstance(v, bytes):
            # 尝试UTF-8解码，如果失败则返回标记信息
            try:
                decoded = v.decode('utf-8')
                try:
                    return json.loads(decoded)
                except (ValueError, TypeError):
                    # 如果解码成功但不是JSON，返回原始字符串（截断以避免过长）
                    return decoded[:500] if len(decoded) > 500 else decoded
            except (UnicodeDecodeError, AttributeError):
                # 二进制数据（如图片、文件等），返回标记
                return {"_type": "binary_data", "size": len(v)}
        elif isinstance(v, str):
            try:
                return json.loads(v)
            except (ValueError, TypeError):
                # 不是JSON格式的字符串，返回原始值（截断以避免过长）
                return v[:500] if len(v) > 500 else v
        return v

    async def _async_iter(self, items: list[bytes]) -> AsyncGenerator[bytes, None]:
        for item in items:
            yield item

    async def get_request_log(self, request: Request, response: Response) -> dict:
        """
        根据request和response对象获取对应的日志记录数据
        """
        data: dict = {"path": request.url.path, "status": response.status_code, "method": request.method}
        # 路由信息
        app: FastAPI = request.app
        for route in app.routes:
            if (
                isinstance(route, APIRoute)
                and route.path_regex.match(request.url.path)
                and request.method in route.methods
            ):
                data["module"] = ",".join(route.tags) if route.tags else ""
                data["summary"] = route.summary if route.summary else ""
        # 获取用户信息
        try:
            token = request.headers.get("token")
            user_obj = None
            if token:
                user_obj: User = await AuthControl.is_authed(token)
            data["user_id"] = user_obj.id if user_obj else 0
            data["username"] = user_obj.username if user_obj else ""
        except Exception:
            data["user_id"] = 0
            data["username"] = ""
        return data

    async def before_request(self, request: Request):
        request_args = await self.get_request_args(request)
        request.state.request_args = request_args

    async def after_request(self, request: Request, response: Response, process_time: int):
        if request.method in self.methods:
            for path in self.exclude_paths:
                if re.search(path, request.url.path, re.I) is not None:
                    return
            
            # 检查是否为文件下载响应，如果是则跳过审计日志（避免二进制数据序列化错误）
            content_type = response.headers.get("content-type", "").lower()
            content_disposition = response.headers.get("content-disposition", "").lower()
            is_file_download = "attachment" in content_disposition
            file_content_types = [
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/msword",
                "application/pdf",
                "application/octet-stream",
                "application/zip",
                "application/x-zip-compressed",
            ]
            is_file_response = is_file_download or any(ct in content_type for ct in file_content_types)
            
            if is_file_response:
                # 对于文件下载，完全跳过审计日志记录，避免二进制数据序列化问题
                return response
            
            try:
                data: dict = await self.get_request_log(request=request, response=response)
                data["response_time"] = process_time

                data["request_args"] = request.state.request_args
                response_body = await self.get_response_body(request, response)
                # 确保response_body是可序列化的（避免二进制数据）
                if isinstance(response_body, dict):
                    data["response_body"] = response_body
                else:
                    # 如果不是字典，尝试安全转换
                    data["response_body"] = self.lenient_json(response_body) if response_body else None
                
                await AuditLog.create(**data)
            except (UnicodeDecodeError, TypeError, ValueError) as e:
                # 如果序列化失败（可能是二进制数据），记录简单信息
                try:
                    data: dict = await self.get_request_log(request=request, response=response)
                    data["response_time"] = process_time
                    data["request_args"] = request.state.request_args
                    data["response_body"] = {"_error": "Failed to serialize response body", "_type": "binary_or_invalid_data"}
                    await AuditLog.create(**data)
                except Exception:
                    # 如果创建日志完全失败，则跳过（不中断响应）
                    pass
            except Exception as e:
                # 其他错误也跳过，不中断响应
                import traceback
                traceback.print_exc()
                pass

        return response

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time: datetime = datetime.now()
        await self.before_request(request)
        response = await call_next(request)
        end_time: datetime = datetime.now()
        process_time = int((end_time.timestamp() - start_time.timestamp()) * 1000)
        await self.after_request(request, response, process_time)
        return response
