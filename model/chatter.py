from chatterbot import ChatBot
from chatterbot.conversation import Statement

from model.base import BaseModel


class ChatterModel(BaseModel):
    def __init__(self):
        self.bot = ChatBot('tgbot')
        self.text_last = {}

    def _get(self, message, c_last, payload, predict):
        # update the bot

        statement = Statement(payload)

        if message.chat.id in c_last:
            last = c_last[message.chat.id]

            self.bot.learn_response(statement, last)

        c_last[message.chat.id] = statement

        # choose the best reply

        if predict:
            response = self.bot.generate_response(statement)

            return [(response.confidence, response.text)]

    def text(self, message, predict):
        return self._get(
            message,
            self.text_last,
            message.text,
            predict
        )
