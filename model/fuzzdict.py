from model.base import BaseModel

from fuzzywuzzy import fuzz


class FuzzDictModel(BaseModel):
    def __init__(self):
        self.text_last = {}
        self.text_set = set()
        self.sticker_last = {}
        self.sticker_set = set()

    def _get(self, message, c_last, c_set, payload):
        # update the set

        if message.chat.id in c_last:
            last = c_last[message.chat.id]

            c_set.add((last, payload))

        c_last[message.chat.id] = payload

        result = [
            (
                (0.01 * fuzz.ratio(payload, test_payload)) ** 2,
                reply_payload,
            )
            for test_payload, reply_payload in c_set
        ]
        total = sum(
            weight
            for weight, reply_payload in result
            if weight > 0.25
        )

        return [
            (weight / total, reply_payload)
            for weight, reply_payload in result
            if weight > 0.25
        ]

    def text(self, message):
        return self._get(
            message,
            self.text_last,
            self.text_set,
            message.text
        )

    def sticker(self, message):
        return self._get(
            message,
            self.sticker_last,
            self.sticker_set,
            message.sticker.file_id
        )
