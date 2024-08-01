# 使用官方Python运行时作为父镜像
FROM python:3.9-slim

# 维护者信息
LABEL maintainer="moqi"

# 设置工作目录为 /usr/src/app，这是应用程序文件存放的地方
WORKDIR /usr/src/app

# 将当前目录下的所有文件复制到容器中的工作目录
COPY . /usr/src/app

# 安装requirements.txt中指定的Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 对外暴露80端口，供外部访问容器
EXPOSE 80

# 设置环境变量
ENV NAME World

# 指定容器启动时运行的命令
CMD ["python", "main.py"]