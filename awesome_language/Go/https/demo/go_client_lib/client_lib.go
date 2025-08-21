package main

import (
	"crypto/tls"
	"crypto/x509"
	_ "embed"
	"fmt"
	"io"
	"net/http"
	"unsafe"
)

// #include <stdlib.h>
import "C"

//go:embed certs/ca.crt
var caCert []byte

//go:embed certs/go-server.crt
var clientCert []byte

//go:embed certs/go-server.key
var clientKey []byte

// export MakeSecureRequest 是提供给 Python 调用的函数
//
//export MakeSecureRequest
func MakeSecureRequest(url *C.char) *C.char {
	// 1. 从嵌入数据中加载证书和密钥
	cert, err := tls.X509KeyPair(clientCert, clientKey)
	if err != nil {
		return C.CString(fmt.Sprintf("Failed to load client cert: %v", err))
	}

	caCertPool := x509.NewCertPool()
	if ok := caCertPool.AppendCertsFromPEM(caCert); !ok {
		return C.CString("Failed to append CA cert")
	}

	// 2. 配置 TLS 客户端
	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		RootCAs:      caCertPool,
	}

	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: tlsConfig,
		},
	}

	// 3. 发起安全的 HTTPS 请求
	resp, err := client.Get(C.GoString(url))
	if err != nil {
		return C.CString(fmt.Sprintf("Request failed: %v", err))
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return C.CString("Failed to read response body")
	}

	return C.CString(string(body))
}

// FreeString 函数用于释放 MakeSecureRequest 分配的内存
// Python 必须在接收到字符串后调用此函数
//
//export FreeString
func FreeString(ptr unsafe.Pointer) {
	C.free(ptr)
}
func main() {}
