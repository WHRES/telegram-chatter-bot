from fuzzywuzzy import fuzz

from model.base import BaseModel


class PartialFuzzDictModel(BaseModel):
    def __init__(self):
        self.text_set = set()

    def _get(self, c_set, payload, predict):
        # update the set

        c_set.add(payload)

        # choose the best reply

        if predict:
            result = [
                (
                    (
                        0.01 * fuzz.partial_ratio(payload, reply_payload)
                    ) ** 1.5,
                    reply_payload,
                )
                for reply_payload in c_set
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

    def text(self, message, predict):
        if len(message.text) >= 3:
            return self._get(
                self.text_set,
                message.text,
                predict
            )
        elif predict:
            return []
