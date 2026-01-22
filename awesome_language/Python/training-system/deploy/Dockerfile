FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y git build-essential

# 安装 Python 依赖
# 注意: Unsloth 安装比较特殊，需要按顺序
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 默认命令
CMD ["python", "main.py"]
