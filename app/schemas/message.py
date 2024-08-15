from typing import Annotated, Any

from pydantic import BaseModel, Field

from app.models.system import IconType, MenuType


class MessageBase(BaseModel):
    content: str = Field(alias="content", description="消息内容")
    image: str = Field(alias="image", description="消息附图")
    channel: int = Field(alias="channel", description="发送管道")
    status: str = Field(alias="status", description="消息状态")

    class Config:
        allow_extra = True
        populate_by_name = True


class MessageCreate(MessageBase):
    ...


class MessageUpdate(MessageBase):
    ...
