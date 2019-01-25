import config

import jsonpickle

def log(update):
    with open(config.path_log, 'a') as file:
        file.write(
            jsonpickle.encode(update) + '\n'
        )


def error(update, error):
    with open(config.path_err, 'a') as file:
        file.write(
            jsonpickle.encode(update) + '\n'
            + jsonpickle.encode(error) + '\n'
        )
