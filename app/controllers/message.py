from app.core.crud import CRUDBase
from app.models.system import Message
from app.schemas.menus import MenuCreate, MenuUpdate
from app.schemas.message import MessageCreate


class MessageController(CRUDBase[Message, MessageCreate, MenuUpdate]):
    def __init__(self):
        super().__init__(model=Message)


message_controller = MessageController()
