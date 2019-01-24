class MemedaChatter:
    def talk(self, message):
        return (
            1 if message.from_user.first_name else 0,
            message.from_user.first_name + ' 么么哒～',
        )
