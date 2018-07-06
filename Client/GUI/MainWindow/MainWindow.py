from threading import Thread
from queue import Queue
from . import ClientMW
from PyQt5.QtCore import pyqtSlot, QTime
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ..AuthWindow.AuthorisationForm import AuthorisationForm
from ..RegWindow.RegistrationForm import RegistrationForm
from ..PrivateWindow.PrivateChatWindow import PrivateChatWindow
from handlers.EventHandlers import EventHandlers as EH


class MainWindow(ClientMW.Ui_MainWindow):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.auth_form = AuthorisationForm()
        self.reg_form = RegistrationForm()
        self.private_list = []
        self.setup()

    def setup(self):
        self.setupUi(self)
        self.actionConnect.triggered.connect(self.connect)
        self.actionAuthorisation.triggered.connect(self.auth_form.show)
        self.actionRegistration.triggered.connect(self.reg_form.show)
        self.actionDisconnect.triggered.connect(self.disconnect)
        self.SendButton.clicked.connect(self.send_all)
        self.auth_form.accepted.connect(self.authorise)
        self.reg_form.accepted.connect(self.registration)
        self.client.incomingMessage.connect(self.print_incoming_message)
        self.show()
        self.list_item_model = QStandardItemModel()
        self.UsersList.setModel(self.list_item_model)
        self.UsersList.doubleClicked.connect(self.open_private)
        self.client.onlineListRecieved.connect(self.show_online_list)
        self.client.newUserOnline.connect(self.add_online_user)
        self.client.userDisconnected.connect(self.del_user)

    def send_all(self):
        if self.client._username:
            message = self.InputBox.toPlainText()
            self.InputBox.clear()
            self.print_message(self.client._username, message)
            EH.send_message(message, self.client, 'All users')
        else:
            self.print_message('System', 'You should be authorised user for chating!')

    def connect(self):
        self.start_net_listening()
        EH.connect(self.client)

    def disconnect(self):
        EH.disconnect(self.client)
        self.list_item_model.clear()

    def create_private(self, comp_name):
        private_window = PrivateChatWindow(self.client, comp_name, self.private_list)
        private_window.new_thread = Thread(target=private_window.run)
        private_window.new_thread.daemon = True
        private_window.new_thread.start()
        self.private_list.append(private_window)
        return private_window

    def open_private(self, index):
        companion = self.list_item_model.itemFromIndex(index)
        comp_name = companion.text()
        self.create_private(comp_name)

    def authorise(self):
        login = self.auth_form.login
        password = self.auth_form.password
        EH.authorise(login, password, self.client)

    def registration(self):
        name = self.reg_form.username
        login = self.reg_form.login
        password = self.reg_form.password
        EH.registration(name, login, password, self.client)

    def print_message(self, username, message):
        time = QTime.currentTime()
        time = f'[{time.toString()}]'
        message = f'{time}{username}: {message}'
        self.Chat.append(message)

    @pyqtSlot(Queue)
    def print_incoming_message(self, mail_bag):
        mail = mail_bag.get()
        if mail:
            type = mail[0]
            username = mail[1]
            message = mail[2]
            if type != 'private':
                self.print_message(username, message)
                mail_bag.task_done()
            else:
                flag = False
                for pw in self.private_list:
                    if username == pw.companion:
                        pw.print_message(username, message)
                        flag = True
                if not flag:
                    pw = self.create_private(username)
                    pw.print_message(username, message)
                mail_bag.task_done()

    @pyqtSlot()
    def show_online_list(self):
        for id, name in self.client._online_list.items():
            if int(id) > 2:
                item = QStandardItem()
                item.setText(name)
                item.Id = id
                item.setEditable(False)
                self.list_item_model.appendRow(item)

    @pyqtSlot(dict)
    def add_online_user(self, user):
        item = QStandardItem()
        item.Id = tuple(user.keys())[0]
        item.setText(user[item.Id])
        item.setEditable(False)
        self.list_item_model.appendRow(item)

    @pyqtSlot(dict)
    def del_user(self, user):
        count = len(self.client._online_list.values())
        print(count)
        user_id = user.popitem()[0]
        print(user_id)
        for i in range(count):
            item = self.list_item_model.item(i)
            print(item.Id)
            if item.Id == user_id:
                self.list_item_model.removeRow(i)


    def start_net_listening(self):
        self.net_thread = Thread(target = self.client.listen)
        self.net_thread.daemon = True
        self.net_thread.start()