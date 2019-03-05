class BaseModel:
    _ready = False

    def text(self, message):
        return []

    def sticker(self, message):
        return []

    def ready(self):
        self._ready = True
