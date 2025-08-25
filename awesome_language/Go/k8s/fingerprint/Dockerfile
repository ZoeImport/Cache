# 使用官方 Go 镜像作为构建环境
FROM golang:1.24-alpine AS builder

WORKDIR /app

# 复制 go.mod 和 go.sum 文件
COPY go.mod go.sum ./
RUN go mod tidy

# 复制源代码并编译
COPY . .
RUN CGO_ENABLED=0 go build -o /get-cluster-id .

# 使用轻量级镜像作为运行时环境
FROM alpine:latest
WORKDIR /
COPY --from=builder /get-cluster-id .

# 在容器启动时运行程序
CMD ["/get-cluster-id"]