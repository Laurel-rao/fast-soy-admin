from app.core.crud import CRUDBase
from app.models.system import Message
from app.schemas.menus import MenuCreate, MenuUpdate


class MessageController(CRUDBase[Message, MenuCreate, MenuUpdate]):
    def __init__(self):
        super().__init__(model=Message)


message_controller = MessageController()
