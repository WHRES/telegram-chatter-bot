from model.base import BaseModel

import random

pool = ['~鸭~', '~好哦~', '~哟~', '_(:з」∠)_', '(*/ω＼*)']

class RepeatModel(BaseModel):
    def text(self, message):
        return (1, message.text + pool[random.randint(0, len(pool) - 1)])
