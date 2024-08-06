from fastapi import APIRouter, Query
from tortoise.functions import Count

from app.api.v1.utils import insert_log
from app.controllers.message import message_controller

from app.models.system import Message, StatusType
from app.models.system import LogType, LogDetailType

from app.schemas.base import Success, SuccessExtra

router = APIRouter()


async def build_menu_tree(messages: list[Message], parent_id: int = 0, simple: bool = False) -> list[dict]:
    """
    递归生成菜单树
    :param messages:
    :param parent_id:
    :param simple: 是否简化返回数据
    :return:
    """
    tree = []
    for Message in messages:
        if Message.parent_id == parent_id:
            children = await build_menu_tree(messages, Message.id, simple)
            if simple:
                menu_dict = {"id": Message.id, "label": Message.menu_name, "pId": Message.parent_id}
            else:
                menu_dict = await Message.to_dict()
                menu_dict["buttons"] = [await button.to_dict() for button in await Message.buttons]
            if children:
                menu_dict["children"] = children
            tree.append(menu_dict)
    return tree


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


@router.get("/messages/tree/", summary="查看菜单树")
async def _():
    messages = await Message.filter(constant=False)
    # 递归生成菜单
    menu_tree = await build_menu_tree(messages, simple=True)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.MenuGetTree, by_user_id=0)
    return Success(data=menu_tree)


@router.get("/messages/{message_id}", summary="查看菜单")
async def get_menu(message_id: int):
    menu_obj: Message = await message_controller.get(id=message_id)
    await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.MenuGetOne, by_user_id=0)
    return Success(data=await menu_obj.to_dict())


# @router.post("/messages", summary="创建菜单")
# async def _(menu_in: MessageCreate):
#     # is_exist = await message_controller.model.exists(route_path=menu_in.route_path)
#     # if is_exist:
#     #     raise HTTPException(
#     #         code="4090",
#     #         msg="The Message with this route_path already exists in the system.",
#     #     )
#
#     new_menu = await message_controller.create(obj_in=menu_in, exclude={"buttons"})
#     if new_menu and menu_in.buttons:
#         await message_controller.update_buttons_by_code(new_menu, menu_in.buttons)
#     await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.MenuCreateOne, by_user_id=0)
#     return Success(msg="Created Successfully", data={"created_id": new_menu.id})


# @router.patch("/messages/{message_id}", summary="更新菜单")
# async def _(message_id: int, menu_in: MessageUpdate):
#     menu_obj = await message_controller.update(id=message_id, obj_in=menu_in, exclude={"buttons"})
#     if menu_obj and menu_in.buttons:
#         await message_controller.update_buttons_by_code(menu_obj, menu_in.buttons)
#     await insert_log(log_type=LogType.AdminLog, log_detail_type=LogDetailType.MenuUpdateOne, by_user_id=0)
#     return Success(msg="Updated Successfully", data={"updated_id": message_id})


@router.get("/messages/lists/", summary="查看一级菜单")
async def _():
    messages = await Message.filter(status=StatusType.enable)
    data = list(messages)
    return Success(data=data)
