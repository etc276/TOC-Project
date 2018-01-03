from transitions.extensions import GraphMachine
import Beauty
import Deck
import time
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler, ConversationHandler)

index = -1
beauty_articles = []
beauty_urls = []
PTT_URL = 'https://www.ptt.cc'


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_staying_at_idle(self, update):
        text = update.message.text
        return text.lower() == 'start'

    def is_going_to_beauty(self, update):
        text = update.message.text
        return text.lower() == 'beauty'

    def is_going_to_deck(self, update):
        text = update.message.text
        return text.lower() == 'deck'
    
    def is_staying_at_beauty(self, update):
        text = update.message.text
        return text.lower() == 'next'

    def is_going_to_ok(self, update):
        text = update.message.text
        return text.lower() == 'ok'

    def is_going_to_joke(self, update):
        text = update.message.text
        return text.lower() == 'joke'

    def is_going_back_to_idle(self, update):
        text = update.message.text
        return text.lower() == 'cancel'

# ///////////////////////////////////////////////////////////////////

    def on_enter_idle(self, update):
        global index
        index = -1
        reply_keyboard = [['beauty', 'deck', 'joke']]
        update.message.reply_text(
            "Hello",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                             one_time_keyboard=True)
        )

    def on_enter_beauty(self, update):
        global first, index
        global beauty_articles, beauty_urls
        
        beauty_articles = Beauty.get_today_articles()
        index = index + 1

        if index >= len(beauty_articles):
            update.message.reply_text("there is no more beauty today")
            self.go_back(update)
        
        while(beauty_articles[index]['push_count'] < 10):
            index = index + 1
            if index >= len(beauty_articles):
                update.message.reply_text("there is no more beauty today")
                self.go_back(update) 
        
        article = beauty_articles[index]
        page = Beauty.get_web_page(PTT_URL + article['href'])
        if page:
            beauty_urls = Beauty.parse_img(page)
        
        if len(beauty_urls) == 0:
            print("this page has no picture") 

        reply_keyboard = [['next', 'ok']]
        update.message.reply_photo(
            photo=beauty_urls[0],
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                             one_time_keyboard=True)
        )

    def on_enter_ok(self, update):
        for url in beauty_urls:
            if(url == beauty_urls[0]):
                continue
            update.message.reply_photo(photo=url)
        
        self.go_back(update)

    def on_enter_deck(self, update):
        deck_codes = Deck.get_deck_code()
        for code in deck_codes:
            update.message.reply_text(code)
        print("finish reply code")
        self.go_back(update)

    def on_enter_joke(self, update):
        update.message.reply_text("哪個殺手只會講英文 ?? (給你五秒唷)")
        time.sleep(5)
        update.message.reply_text("銀翼殺手")
        self.go_back(update)

# ////////////////////////////////////////////////////////////////////

    def on_exit_beauty(self, update):
        print('Leaving beauty')

    def on_exit_deck(self, update):
        print('Leaving deck')
