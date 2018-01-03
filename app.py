import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine

import Beauty
import Deck

API_TOKEN = ''
WEBHOOK_URL = '' + '/hook'



app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'idle',
        'beauty',
        'ok',
        'deck',
        'joke'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': ['idle', 'beauty', 'ok', 'deck', 'joke'],
            'dest': 'idle',
            'conditions': 'is_going_back_to_idle'
        },
        {
            'trigger': 'advance',
            'source': 'idle',
            'dest': 'idle',
            'conditions': 'is_staying_at_idle'
        },
        {
            'trigger': 'advance',
            'source': 'idle',
            'dest': 'joke',
            'conditions': 'is_going_to_joke'
        },
        {
            'trigger': 'advance',
            'source': 'beauty',
            'dest': 'beauty',
            'conditions': 'is_staying_at_beauty'
        },
        {
            'trigger': 'advance',
            'source': 'beauty',
            'dest': 'ok',
            'conditions': 'is_going_to_ok'
        },
        {
            'trigger': 'advance',
            'source': 'idle',
            'dest': 'beauty',
            'conditions': 'is_going_to_beauty'
        },
        {
            'trigger': 'advance',
            'source': 'idle',
            'dest': 'deck',
            'conditions': 'is_going_to_deck'
        },
        {
            'trigger': 'go_back',
            'source': [
                'beauty',
                'ok',
                'deck',
                'joke'
            ],
            'dest': 'idle'
        }
    ],
    initial='idle',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
