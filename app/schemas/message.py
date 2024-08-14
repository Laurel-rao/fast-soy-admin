from typing import Annotated, Any

from pydantic import BaseModel, Field

from app.models.system import IconType, MenuType


class MessageBase(BaseModel):
    content: str = Field(alias="content", description="菜单名称")
    image: MenuType = Field(alias="image", description="菜单类型")
    channel: str = Field(alias="channel", description="路由名称")
    status: str = Field(alias="status", description="路由路径")

    class Config:
        allow_extra = True
        populate_by_name = True


class MessageCreate(MessageBase):
    ...


class MessageUpdate(MessageBase):
    ...
