from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional, List
import json

# 定义数据结构 (Schema)
class TrainingTask(BaseModel):
    # 必填字段 (Go: ID int)
    task_id: int 
    
    # 带默认值的字段 (Go: Source string `default:"web"`)
    source: str = "web"
    
    # 字段别名，读取 json 中的 "content" 字段映射到 input_text (Go: Content string `json:"content"`)
    input_text: str = Field(alias="content", min_length=5) 
    
    # 嵌套列表
    tags: List[str] = []

    # 自定义校验逻辑 (Go: func (t *TrainingTask) Validate() error)
    @field_validator('source')
    def check_source(cls, v):
        allowed = ['web', 'chat', 'book']
        if v not in allowed:
            raise ValueError(f"Source must be one of {allowed}")
        return v

# --- 测试运行 ---
if __name__ == "__main__":
    print("=== 1. 正常数据测试 ===")
    raw_data = {
        "task_id": 101,
        "content": "这是一条用来训练大模型的文本数据", # 注意这里用了 content，会自动映射到 input_text
        "source": "chat",
        "tags": ["AI", "NLP"]
    }
    
    try:
        # 解析数据 (Unmarshalling)
        task = TrainingTask(**raw_data)
        print(f"✅ 解析成功: ID={task.task_id}, Input={task.input_text}")
        print(f"   转回字典: {task.model_dump()}")
        print(f"   转回JSON: {task.model_dump_json()}")
    except ValidationError as e:
        print(e)

    print("\n=== 2. 脏数据测试 (模拟报错) ===")
    bad_data = {
        "task_id": "不是数字",  # 类型错误
        "content": "短",        # 长度不够
        "source": "unknown"     # 值不在允许范围内
    }
    try:
        TrainingTask(**bad_data)
    except ValidationError as e:
        print("❌ 拦截到错误:")
        print(e.json()) # 打印出非常详细的错误日志