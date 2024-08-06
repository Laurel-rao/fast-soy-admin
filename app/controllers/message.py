from loguru import logger

from app.core.crud import CRUDBase
from app.models.system import Message
from app.schemas.menus import ButtonBase, MenuCreate, MenuUpdate


class MessageController(CRUDBase[Message, MenuCreate, MenuUpdate]):
    def __init__(self):
        super().__init__(model=Message)
    #
    # @staticmethod
    # async def update_buttons_by_code(Message: Message, buttons: list[ButtonBase] | None = None) -> bool:
    #     if not buttons:
    #         return False
    #
    #     existing_buttons = [button.button_code for button in await Message.buttons]
    #
    #     menu_buttons = [button.button_code for button in buttons]
    #
    #     for button_code in set(existing_buttons) - set(menu_buttons):
    #         logger.error(f"Button Deleted {button_code}")
    #         await Button.filter(button_code=button_code).delete()
    #
    #     await Message.buttons.clear()
    #     for button in buttons:
    #         button_obj, _ = await Button.update_or_create(button_code=button.button_code, defaults=dict(button_desc=button.button_desc))
    #         await Message.buttons.add(button_obj)
    #
    #     return True


message_controller = MessageController()
