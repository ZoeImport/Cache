#!/bin/bash

set -e

DEMO_DIR="."
CERT_DIR="$DEMO_DIR/certs"
CONF_DIR="$DEMO_DIR/conf"

echo "Creating project directory structure..."
mkdir -p "$DEMO_DIR"
mkdir -p "$CERT_DIR"
mkdir -p "$DEMO_DIR/auth_proxy"
mkdir -p "$DEMO_DIR/go_internal_service"
mkdir -p "$DEMO_DIR/python_internal_service"

echo "Generating certificates..."
# 1. Generate CA Certificate
openssl req -x509 -new -nodes -keyout "$CERT_DIR/ca.key" -sha256 -days 365 -out "$CERT_DIR/ca.crt" -subj "/CN=MyCA"

# 2. Generate auth_proxy certificates
openssl genrsa -out "$CERT_DIR/auth-proxy.key" 2048
openssl req -new -key "$CERT_DIR/auth-proxy.key" -out "$CERT_DIR/auth-proxy.csr" -config "$CONF_DIR/openssl_proxy.cnf"
openssl x509 -req -in "$CERT_DIR/auth-proxy.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" -CAcreateserial -out "$CERT_DIR/auth-proxy.crt" -days 365 -sha256 -extfile "$CONF_DIR/openssl_proxy.cnf" -extensions v3_req

# 3. Generate go_internal_service certificates
openssl genrsa -out "$CERT_DIR/go-internal.key" 2048
openssl req -new -key "$CERT_DIR/go-internal.key" -out "$CERT_DIR/go-internal.csr" -config "$CONF_DIR/openssl_go.cnf"
openssl x509 -req -in "$CERT_DIR/go-internal.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" -CAcreateserial -out "$CERT_DIR/go-internal.crt" -days 365 -sha256 -extfile "$CONF_DIR/openssl_go.cnf" -extensions v3_req

# 4. Generate python_internal_service certificates
openssl genrsa -out "$CERT_DIR/python-internal.key" 2048
openssl req -new -key "$CERT_DIR/python-internal.key" -out "$CERT_DIR/python-internal.csr" -config "$CONF_DIR/openssl_python.cnf"
openssl x509 -req -in "$CERT_DIR/python-internal.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" -CAcreateserial -out "$CERT_DIR/python-internal.crt" -days 365 -sha256 -extfile "$CONF_DIR/openssl_python.cnf" -extensions v3_req
