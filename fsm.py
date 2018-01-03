from transitions.extensions import GraphMachine


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        # print(update.message.chat.id)
        return text.lower() == 'go to state1'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'go to state2'
    
    def is_staying_at_state1(self, update):
        text = update.message.text
        return text.lower() == 'stay at state1'

    def is_going_to_user(self, update):
        text = update.message.text
        return text.lower() == 'ok'

    def on_enter_user(self, update):
        update.message.reply_text("I'm entering user")

    def on_enter_state1(self, update):
        update.message.reply_text("I'm entering state1")
        # self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("I'm entering state2")
        self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')
