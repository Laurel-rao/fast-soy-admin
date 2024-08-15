from fastapi import APIRouter, Query

from app.api.v1.utils import insert_log
from app.controllers.message import message_controller

from app.models.system import Message, StatusType, Channel
from app.models.system import LogType, LogDetailType

from app.schemas.base import Success, SuccessExtra
from app.schemas.message import MessageCreate

router = APIRouter()


@router.get("/messages", summary="查看用户菜单")
async def _(
        current: int = Query(1, description="页码"),
        size: int = Query(100, description="每页数量")
):
    total, messages = await message_controller.list(page=current, page_size=size, order=["id"])
    # 递归生成菜单
    records = []
    for obj in messages:
        data = await obj.to_dict()
        records.append(data)
    data = {"records": records}
    return SuccessExtra(data=data, total=total, current=current, size=size)


@router.get("/messages/{message_id}", summary="查看菜单")
async def get_menu(message_id: int):
    menu_obj: Message = await message_controller.get(id=message_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.MenuGetOne, by_user_id=0)
    return Success(data=await menu_obj.to_dict())


@router.get("/messages/lists/", summary="查看一级菜单")
async def _():
    messages = await Message.filter(status=StatusType.enable)
    data = list(messages)
    return Success(data=data)


@router.post("/messages", summary="创建消息")
async def _(post_data: MessageCreate):
    post_data.channel = await Channel.get(id=post_data.channel)
    new_menu = await message_controller.create(obj_in=post_data)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.MessageCreateOne, by_user_id=0)
    return Success(msg="Created Successfully", data={"created_id": new_menu.id})