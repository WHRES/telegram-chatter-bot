from model.base import BaseModel

class MemorizeModel(BaseModel):
    def __init__(self):
        self.text_last = {}
        self.text_dict = {}
        self.sticker_last = {}
        self.sticker_dict = {}

    def text(self, message):
        if message.chat.id in self.text_last:
            last = self.text_last[message.chat.id]

            if last not in self.text_dict:
                self.text_dict[last] = set()

            self.text_dict[last].add(message.text)

        self.text_last[message.chat.id] = message.text

        if message.text in self.text_dict:
            pool = self.text_dict[message.text]

            return [
                (1 / len(pool), text)
                for text in pool
            ]
        else:
            return []

    def sticker(self, message):
        if message.chat.id in self.sticker_last:
            last = self.sticker_last[message.chat.id]

            if last not in self.sticker_dict:
                self.sticker_dict[last] = []

            self.sticker_dict[last].add(message.sticker.file_id)

        self.sticker_last[message.chat.id] = message.sticker.file_id

        if message.sticker.file_id in self.sticker_dict:
            pool = self.sticker_dict[message.sticker.file_id]

            return [
                (1 / len(pool), sticker)
                for sticker in pool
            ]
        else:
            return []
