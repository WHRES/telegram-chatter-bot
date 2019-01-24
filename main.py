import jsonpickle
import random
from telegram.ext import Updater, MessageHandler, Filters

import config
import bottoken
from chat.meow import MeowChatter
from chat.memeda import MemedaChatter

debug = True

chatters = [
    (0.02, MemedaChatter()),
    (0.1, MeowChatter()),
]


def choose(candidates):
    weights = [weight for weight, payload in candidates]

    if random.random() < max(weights):
        # choose one from the candidates

        target = sum(weights) * random.random()

        if debug:
            print(target)

        for weight, payload in candidates:
            target -= weight

            if target <= 0:
                return payload
    else:
        # skip

        return None


def handler(bot, update):
    file_log = open(config.path_log, 'a')
    file_log.write(
        jsonpickle.encode(update) + '\n'
    )
    file_log.close()

    # collect the candidates

    candidates = []

    for prob, chatter in chatters:
        weight, text = chatter.talk(update.message)
        candidates.append((prob * weight, text))

    if debug:
        print(candidates)

    # determine whether reply or not

    text = choose(candidates)

    if text is not None:
        update.message.reply_text(text)


def error(bot, update, error):
    file_err = open(config.path_err, 'a')
    file_err.write(
        jsonpickle.encode(update) + '\n'
        + jsonpickle.encode(error) + '\n'
    )
    file_err.close()


def main():
    updater = Updater(bottoken.token)

    updater.dispatcher.add_handler(MessageHandler(Filters.text, handler))
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
