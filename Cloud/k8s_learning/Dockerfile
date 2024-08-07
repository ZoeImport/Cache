# 构建阶段
FROM golang:1.22-alpine AS build

WORKDIR /app

COPY ./main.go .

RUN go mod init app && go mod tidy && go build -o myapp

# 运行阶段
FROM debian:buster

WORKDIR /app

COPY --from=build /app/myapp .

EXPOSE 3000

CMD ["./myapp"]
