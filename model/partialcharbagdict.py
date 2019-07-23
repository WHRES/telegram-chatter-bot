from model.base import BaseModel


class PartialCharBagDictModel(BaseModel):
    def __init__(self):
        self.text_set = set()

    def _get(self, message, c_last, c_set, payload, predict):
        # update the set

        c_set.add((set(payload), payload))

        # choose the best reply

        if predict:
            payload_set = set(payload)
            result = [
                (
                    (
                        len(payload_set.intersection(reply_set))
                            / (len(payload_set) + len(reply_set))
                    ) ** 1.5,
                    reply_payload,
                )
                for reply_set, reply_payload in c_set
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
                message,
                self.text_last,
                self.text_set,
                message.text,
                predict
            )
        elif predict:
            return []
