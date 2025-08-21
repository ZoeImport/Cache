整体架构
Go 服务：

作为服务端：监听一个 HTTPS 端口，并要求客户端（Python 服务）进行证书验证。

作为客户端：通过调用一个 Go 动态库，向 Python 服务发起安全的 HTTPS 请求，并提供自己的证书。

Python 服务：

作为服务端：使用 ssl 模块监听一个 HTTPS 端口，并要求客户端（Go 服务）进行证书验证。

作为客户端：调用 Go 编译的 .so 动态库，发起 HTTPS 请求。

Go 动态库：

一个独立的 Go 模块，内部使用 go:embed 嵌入了客户端的证书和 CA 证书。

提供一个函数，封装了 mTLS 客户端配置，供 Python 服务调用。

第 1 步：生成证书文件
首先，您需要为两个服务生成证书。这里我们使用 OpenSSL，因为它的命令通用且清晰。

Bash

# 创建一个名为 certs 的目录来存放所有证书
```shell
mkdir certs
```

# 1. 生成 CA 证书和私钥
```shell
openssl req -x509 -new -nodes -keyout certs/ca.key -sha256 -days 365 -out certs/ca.crt -subj "/CN=MyCompanyCA"
```
# 2. 生成 Go 服务的证书和私钥
```shell
openssl genrsa -out certs/go-server.key 2048
openssl req -new -key certs/go-server.key -out certs/go-server.csr -subj "/CN=go-service"
openssl x509 -req -in certs/go-server.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/go-server.crt -days 365 -sha256
```
# 3. 生成 Python 服务的证书和私钥
```shell
openssl genrsa -out certs/python-server.key 2048
openssl req -new -key certs/python-server.key -out certs/python-server.csr -subj "/CN=python-service"
openssl x509 -req -in certs/python-server.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/python-server.crt -days 365 -sha256
```