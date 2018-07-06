from . import Auth


class AuthorisationForm(Auth.Ui_Authorisation):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)

    def accept(self):
        self.login = self.LoginInputBox.text()
        self.password = self.PassInputBox.text()
        super().accept()