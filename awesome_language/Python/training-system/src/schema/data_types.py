from pydantic import BaseModel, Field
from typing import Optional, Literal

class TrainingSample(BaseModel):
    """
    [DTO] 数据传输对象
    Go类比: struct { ID int, Instruction string ... }
    """
    id: int
    instruction: str
    input_text: str = Field(alias="input", default="")
    output_text: str = Field(alias="output")
    status: Literal['pending', 'trained'] = 'pending'

    class Config:
        populate_by_name = True
