# --- Frontend Build Stage ---
FROM node:18.12.0-alpine3.16 AS web

WORKDIR /opt/vue-fastapi-admin/web

# 1. 在 Node 环境中全局安装 pnpm
#    这是使用 pnpm 的标准步骤
RUN npm install -g pnpm

# 2. 只复制 package.json 和 pnpm-lock.yaml 文件
#    注意这里的文件名是 pnpm-lock.yaml
COPY web/package.json web/pnpm-lock.yaml ./

# 3. 使用 pnpm install 命令安装依赖
#    --frozen-lockfile 参数等同于 npm ci，确保严格按照锁文件安装
RUN pnpm install --frozen-lockfile --registry=https://registry.npmmirror.com

# 4. 在依赖安装完成后，再复制所有的源代码
COPY web/ ./

# 5. 使用 pnpm 运行构建命令
RUN pnpm run build
FROM python:3.11-slim-bullseye

WORKDIR /opt/vue-fastapi-admin
ADD . .
COPY /deploy/entrypoint.sh .

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,id=core-apt \
    --mount=type=cache,target=/var/lib/apt,sharing=locked,id=core-apt \
    sed -i "s@http://.*.debian.org@http://mirrors.ustc.edu.cn@g" /etc/apt/sources.list \
    && rm -f /etc/apt/apt.conf.d/docker-clean \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev bash nginx vim curl procps net-tools

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY --from=web /opt/vue-fastapi-admin/web/dist /opt/vue-fastapi-admin/web/dist
ADD /deploy/web.conf /etc/nginx/sites-available/web.conf
RUN rm -f /etc/nginx/sites-enabled/default \ 
    && ln -s /etc/nginx/sites-available/web.conf /etc/nginx/sites-enabled/ 

ENV LANG=zh_CN.UTF-8
EXPOSE 80

ENTRYPOINT [ "sh", "entrypoint.sh" ]