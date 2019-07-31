import random
import traceback

import jsonpickle
from telegram.ext import Updater, MessageHandler, Filters

import bottoken
import config
import log
from model.charbagdict import CharBagDictModel
from model.charbagdict2 import CharBagDict2Model
# from model.chatter import ChatterModel
from model.fuzzdict import FuzzDictModel
from model.memeda import MemedaModel
from model.memeda2 import Memeda2Model
from model.naivedict import NaiveDictModel
from model.partialcharbagdict import PartialCharBagDictModel
from model.partialfuzzdict import PartialFuzzDictModel
from model.repeat import RepeatModel

models = [
    (0.1, 0, CharBagDictModel()),
    (0.1, 0, CharBagDict2Model()),
    # (0, 0, ChatterModel()), # TODO
    (0.3, 0, FuzzDictModel()),
    (0.02, 0, MemedaModel()),
    (0.03, 0, Memeda2Model()),
    (0.15, 0.8, NaiveDictModel()),
    (0.1, 0, PartialCharBagDictModel()),
    (0.15, 0, PartialFuzzDictModel()),
    (0.05, 0.2, RepeatModel()),
]


def error_handler(_bot, update, err):
    log.error(update, err)


def train(operation):
    for _, _, model in models:
        operation(model, False)


def collect(operation, event_index):
    candidates = []

    for text_weight, sticker_weight, model in models:
        for weight, payload in operation(model, True):
            candidates.append((
                (text_weight, sticker_weight)[event_index] * weight,
                payload,
            ))

    if config.debug:
        print(candidates)

    return candidates


def choose(candidates, force):
    # choose one from the candidates

    total = sum(
        weight
        for weight, payload in candidates
    )

    if force or random.random() < total:
        target = total * random.random()

        for weight, payload in candidates:
            target -= weight

            if target <= 0:
                if config.debug:
                    print(payload)

                return payload

    return None


def handler(bot, update, event_index, collect_operation, reply_operation):
    log.log(update)

    try:
        if update.message.reply_to_message is not None:
            force = update.message.reply_to_message.from_user.id == bottoken.self
        else:
            force = False
        rate = (config.rate_text, config.rate_sticker)[event_index]

        if force or random.random() < rate:
            # collect the candidates

            candidates = collect(collect_operation, 0)

            # choose and send reply

            payload = choose(candidates, force)

            if payload is not None:
                reply_operation(payload)
        else:
            # train without collecting

            train(collect_operation)
    except:
        traceback.print_exc()
        error_handler(bot, update, 'internal error')


def text_handler(bot, update):
    handler(
        bot,
        update,
        0,
        lambda model, predict: model.text(update.message, predict),
        update.message.reply_text
    )


def sticker_handler(bot, update):
    handler(
        bot,
        update,
        1,
        lambda model, predict: model.sticker(update.message, predict),
        update.message.reply_sticker
    )


def main():
    # load historic data

    count = 0

    with open(config.path_log, 'r') as file:
        for line in file:
            update = jsonpickle.decode(line)

            count += 1
            if count % 1000 == 0:
                print('load:', count)

            if update.message is not None:
                if update.message.text is not None:
                    for _, _, model in models:
                        model.text(update.message, False)
                if update.message.sticker is not None:
                    for _, _, model in models:
                        model.sticker(update.message, False)

    print('total:', count)
    print('ready')

    # start the bot

    updater = Updater(bottoken.token)

    updater.dispatcher.add_error_handler(error_handler)
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, text_handler)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.sticker, sticker_handler)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
