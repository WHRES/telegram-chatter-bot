from model.base import BaseModel


class NaiveDictModel(BaseModel):
    def __init__(self):
        self.text_last = {}
        self.text_dict = {}
        self.sticker_last = {}
        self.sticker_dict = {}

    def _get(self, message, c_last, c_dict, payload):
        # update the dict

        if message.chat.id in c_last:
            last = c_last[message.chat.id]

            c_dict[last] = c_dict.get(last, set())
            c_dict[last].add(payload)

        c_last[message.chat.id] = payload

        # choose the best reply

        if self._ready:
            if payload in c_dict:
                return [
                    (1 / len(c_dict[payload]), reply_payload)
                    for reply_payload in c_dict[payload]
                ]
            else:
                return []

    def text(self, message):
        return self._get(
            message,
            self.text_last,
            self.text_dict,
            message.text
        )

    def sticker(self, message):
        return self._get(
            message,
            self.sticker_last,
            self.sticker_dict,
            message.sticker.file_id
        )
