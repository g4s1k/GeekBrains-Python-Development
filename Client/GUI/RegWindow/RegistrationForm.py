from . import Reg


class RegistrationForm(Reg.Ui_Registration):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)

    def accept(self):
        self.username = self.UsernameInputBox.text()
        self.login = self.LoginInputBox.text()
        self.password = self.PassInputBox.text()
        super().accept()