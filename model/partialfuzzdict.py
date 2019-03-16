from model.base import BaseModel

from fuzzywuzzy import fuzz


class PartialFuzzDictModel(BaseModel):
    def __init__(self):
        self.text_set = set()

    def _get(self, message, c_set, payload, predict):
        # update the set

        c_set.add(payload)

        # choose the best reply

        if predict:
            result = [
                (
                    (0.01 * fuzz.partial_ratio(payload, test_payload)) ** 2,
                    test_payload,
                )
                for test_payload in c_set
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
        return self._get(
            message,
            self.text_set,
            message.text,
            predict
        )
