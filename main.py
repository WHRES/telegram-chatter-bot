import config
import bottoken
import log
from model.repeat import RepeatModel
from model.memeda import MemedaModel

import random
from telegram.ext import Updater, MessageHandler, Filters

models = [
    (0.1, RepeatModel()),
    (0.02, MemedaModel()),
]


def error_handler(bot, update, error):
    log.error(update, error)


def choose(candidates):
    weights = [weight for weight, payload in candidates]

    if random.random() < max(weights):
        # choose one from the candidates

        target = sum(weights) * random.random()

        if config.debug:
            print(target)

        for weight, payload in candidates:
            target -= weight

            if target <= 0:
                return payload
    else:
        # skip

        return None


def text_handler(bot, update):
    log.log(update)

    # collect the candidates

    candidates = []

    for prob, model in models:
        weight, text = model.text(update.message)
        candidates.append((prob * weight, text))

    if config.debug:
        print(candidates)

    # choose and send reply

    text = choose(candidates)

    if text is not None:
        update.message.reply_text(text)


def sticker_handler(bot, update):
    log.log(update)

    # collect the candidates

    candidates = []

    for prob, model in models:
        weight, sticker = model.sticker(update.message)
        candidates.append((prob * weight, sticker))

    if config.debug:
        print(candidates)

    # choose and send reply

    sticker = choose(candidates)

    if sticker is not None:
        update.message.reply_sticker(sticker)


def main():
    updater = Updater(bottoken.token)

    updater.dispatcher.add_error_handler(error_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.sticker, sticker_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
