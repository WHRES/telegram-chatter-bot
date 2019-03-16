from model.base import BaseModel

pool = ['~鸭~', '~好哦~', '~哟~', '_(:з」∠)_', '(*/ω＼*)', '', '', '']


class RepeatModel(BaseModel):
    def text(self, message, predict):
        if predict:
            return [
                (1 / len(pool), message.text + postfix)
                for postfix in pool
            ]

    def sticker(self, message, predict):
        if predict:
            return [(1, message.sticker.file_id)]
