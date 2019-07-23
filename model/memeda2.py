from model.base import BaseModel


class Memeda2Model(BaseModel):
    def text(self, message, predict):
        if predict:
            if message.from_user.first_name == '纯纯umiki':
                return [(1, message.from_user.first_name + ' 么么哒～')]

            return []
