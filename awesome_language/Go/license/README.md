# 1. 生成 RSA 私钥 (2048 位)
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048

# 2. 从私钥中提取公钥
openssl rsa -pubout -in private.pem -out public.pem