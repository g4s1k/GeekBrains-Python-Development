from . import PrivateChat
from PyQt5 import QtCore
from handlers.EventHandlers import EventHandlers as EH


class PrivateChatWindow(PrivateChat.Ui_PrivateChat):
    def __init__(self, client, companion, private_list):
        super().__init__()
        self.companion = companion
        self.client = client
        self.setup()
        self._exit = False
        self.private_list = private_list

    def setup(self):
        self.setupUi(self)
        self.MainUserLabel.setText(self.client._username)
        self.RecipLabel.setText(self.companion)
        self.SendButton.clicked.connect(self.send_private)
        self.show()

    def send_private(self):
        if self.client._username:
            message = self.InputBox.toPlainText()
            self.InputBox.clear()
            self.print_message(self.client._username, message)
            EH.send_message(message, self.client, self.companion)
        else:
            self.print_message('System', 'You should be authorised user for chating!')

    def print_message(self, username, message):
        time = QtCore.QTime.currentTime()
        time = f'[{time.toString()}]'
        message = f'{time}{username}: {message}'
        self.Chat.append(message)

    def run(self):
        while not self._exit:
            self.show()

    def closeEvent(self, event):
        self._exit = True
        self.private_list.remove(self)
        event.accept()