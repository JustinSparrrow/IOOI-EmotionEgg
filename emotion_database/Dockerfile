# ========== 构建阶段 ==========
FROM golang:1.23-alpine AS builder

WORKDIR /src

# 先只复制依赖清单，利用镜像层缓存：
# 只要 go.mod / go.sum 没变，下面这层就会命中缓存，不必重新下载依赖。
# 若把 COPY . . 放在前面，任何一行代码改动都会让依赖缓存失效。
COPY go.mod go.sum ./
RUN go mod download

COPY . .

# CGO_ENABLED=0 生成不依赖系统 C 库的静态二进制，
# 这样才能放进精简的运行镜像里正常执行。
# -trimpath 去掉构建机的绝对路径，-s -w 去掉符号表与调试信息，减小体积。
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/server .

# ========== 运行阶段 ==========
FROM alpine:3.20

# 时区数据用于正确写入 timestamp，CA 证书用于后续发起 HTTPS 请求
RUN apk add --no-cache ca-certificates tzdata

WORKDIR /app
COPY --from=builder /out/server ./server

EXPOSE 8080
ENTRYPOINT ["./server"]
