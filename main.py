import config
import bottoken
import log
from model.memeda import MemedaModel
from model.memorize import MemorizeModel
from model.repeat import RepeatModel

import random
import jsonpickle
from telegram.ext import Updater, MessageHandler, Filters

models = [
    (0.02, MemedaModel()),
    (0.5, MemorizeModel()),
    (0.1, RepeatModel()),
]


def error_handler(bot, update, error):
    log.error(update, error)


def collect(predictions):
    candidates = []

    for model_weight, model in models:
        for weight, text in predictions:
            candidates.append((model_weight * weight, text))

    if config.debug:
        print(candidates)

    return candidates


def choose(candidates):
    weights = [
        weight
        for weight, payload in candidates
    ]

    if random.random() < max(weights):
        # choose one from the candidates

        target = sum(weights) * random.random()

        for weight, payload in candidates:
            target -= weight

            if target <= 0:
                if config.debug:
                    print(payload)

                return payload
    else:
        # skip

        return None


def text_handler(bot, update):
    log.log(update)

    # collect the candidates

    candidates = collect(model.text(update.message))

    # choose and send reply

    text = choose(candidates)

    if text is not None:
        update.message.reply_text(text)


def sticker_handler(bot, update):
    log.log(update)

    # collect the candidates

    candidates = collect(model.sticker(update.message))

    # choose and send reply

    sticker = choose(candidates)

    if sticker is not None:
        update.message.reply_sticker(sticker)


def main():
    # load historic data

    with open(config.path_log, 'r') as file:
        for line in file:
            update = jsonpickle.decode(line)

            if update.message is not None:
                if update.message.text is not None:
                    for prob, model in models:
                        model.text(update.message)
                if update.message.sticker is not None:
                    for prob, model in models:
                        model.sticker(update.message)

    # start the bot

    updater = Updater(bottoken.token)

    updater.dispatcher.add_error_handler(error_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.sticker, sticker_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
