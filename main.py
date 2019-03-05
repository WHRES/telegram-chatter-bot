import config
import bottoken
import log
from model.fuzzdict import FuzzDictModel
from model.memeda import MemedaModel
from model.memeda2 import Memeda2Model
from model.naivedict import NaiveDictModel
from model.partialfuzzdict import PartialFuzzDictModel
from model.repeat import RepeatModel

import random
import jsonpickle
from telegram.ext import Updater, MessageHandler, Filters

models = [
    (0.5, 0, FuzzDictModel()),
    (0.05, 0, MemedaModel()),
    (0.1, 0, Memeda2Model()),
    (0.25, 1, NaiveDictModel()),
    (0.25, 0, PartialFuzzDictModel()),
    (0.1, 0.25, RepeatModel()),
]


def error_handler(bot, update, error):
    log.error(update, error)


def collect(operation, event_index):
    candidates = []

    for text_weight, sticker_weight, model in models:
        for weight, payload in operation(model):
            candidates.append((
                (text_weight, sticker_weight)[event_index] * weight,
                payload,
            ))

    if config.debug:
        print(candidates)

    return candidates


def choose(candidates):
    # choose one from the candidates

    total = sum(
        weight
        for weight, payload in candidates
    )

    if random.random() < total:
        target = total * random.random()

        for weight, payload in candidates:
            target -= weight

            if target <= 0:
                if config.debug:
                    print(payload)

                return payload
    else:
        return None


def handler(bot, update, event_index, collect_operation, reply_operation):
    log.log(update)

    if random.random() < (config.rate_text, config.rate_sticker)[event_index]:
        # collect the candidates

        candidates = collect(collect_operation, 0)

        # choose and send reply

        payload = choose(candidates)

        if payload is not None:
            reply_operation(payload)


def text_handler(bot, update):
    handler(
        bot,
        update,
        0,
        lambda model: model.text(update.message),
        lambda payload: update.message.reply_text(payload)
    )


def sticker_handler(bot, update):
    handler(
        bot,
        update,
        1,
        lambda model: model.sticker(update.message),
        lambda payload: update.message.reply_sticker(payload)
    )


def main():
    # load historic data

    with open(config.path_log, 'r') as file:
        for line in file:
            update = jsonpickle.decode(line)

            if update.message is not None:
                if update.message.text is not None:
                    for text_weight, sticker_weight, model in models:
                        model.text(update.message)
                if update.message.sticker is not None:
                    for text_weight, sticker_weight, model in models:
                        model.sticker(update.message)

    for text_weight, sticker_weight, model in models:
        model.ready()

    if config.debug:
        print('ready')

    # start the bot

    updater = Updater(bottoken.token)

    updater.dispatcher.add_error_handler(error_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.sticker, sticker_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
