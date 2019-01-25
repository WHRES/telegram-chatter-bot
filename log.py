import config

import jsonpickle

def log(update):
    file_log = open(config.path_log, 'a')
    file_log.write(
        jsonpickle.encode(update) + '\n'
    )
    file_log.close()


def error(update, error):
    file_err = open(config.path_err, 'a')
    file_err.write(
        jsonpickle.encode(update) + '\n'
        + jsonpickle.encode(error) + '\n'
    )
    file_err.close()
