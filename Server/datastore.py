from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
import sqlalchemy.orm.exc as db_exc
from Server import admin
import logging

deblog = logging.getLogger('deblogger')
errlog = logging.getLogger('errlogger')

engine = create_engine('sqlite:///server_database.db3')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):

    __tablename__ = 'User'
    Id = Column(Integer, primary_key=True)
    Username = Column(String)
    Login = Column(String)
    Password = Column(String)
    Contacts = Column(String)

    @classmethod
    def authorise(cls, session, login, password):
        try:
            user = session.query(cls).filter(cls.Login == login).one()
            if user.Password == password:
                return user
        except db_exc.NoResultFound:
            pass

    @classmethod
    def registration(cls, session, username, login, password):
        try:
            user = session.query(cls).filter(cls.Username == username).one()
        except db_exc.NoResultFound:
            try:
                user = session.query(cls).filter(cls.Login == login).one()
            except db_exc.NoResultFound:
                user = cls()
                user.Username = username
                user.Login = login
                user.Password = password
                session.add(user)
                session.commit()
                return user


class Action(Base):

    __tablename__ = 'Action'
    Id = Column(Integer, primary_key=True)
    Name = Column(String)

    def __init__(self, name):

        self.Name = name

    @classmethod
    def get_action_id(cls, session, action):
        try:
            act = session.query(cls).filter(cls.Name == action).one()
            return act.Id
        except db_exc.NoResultFound:
            errlog.error('Incorrect action name')


class Adress(Base):

    __tablename__ = 'Adress'
    Id = Column(Integer, primary_key=True)
    Adress = Column(String)

    @classmethod
    def get_adr_id(cls, session, adress):
        if isinstance(adress, tuple):
            adress = list(adress)
            adress[1] = str(adress[1])
            adress = ':'.join(adress)
        adr = session.query(cls).filter(cls.Adress == adress).all()
        if not adr:
            adr = cls()
            adr.Adress = adress
            session.add(adr)
            session.commit()
        else:
            adr = adr[0]
        return adr.Id


class Message(Base):

    __tablename__ = 'Message'
    Id = Column(Integer, primary_key=True)
    Rec_Id = Column(Integer, ForeignKey('User.Id'))
    Rec_Adr_Id = Column(Integer, ForeignKey('Adress.Id'))
    Text = Column(String)
    Recipient = relationship('User', backref='Messages')
    Rec_Adr = relationship('Adress', backref='Messages')

    @classmethod
    def add_message(cls, session, rec_user_id, rec_adr_id, text):
        message = cls()
        message.Rec_Id = rec_user_id
        message.Rec_Adr_Id = rec_adr_id
        message.Text = text
        session.add(message)
        session.commit()
        return message


class Journal(Base):

    __tablename__ = 'Journal'
    Id = Column(Integer, primary_key=True)
    Datetime = Column(DateTime, default=func.now())
    Action_Id = Column(Integer, ForeignKey('Action.Id'))
    Sender_Id = Column(Integer, ForeignKey('User.Id'))
    Sender_Adr_Id = Column(Integer, ForeignKey('Adress.Id'))
    Message_Id = Column(Integer, ForeignKey('Message.Id'))
    Action = relationship('Action', backref='Actions')
    Sender = relationship('User', backref='Actions')
    Sender_Adr = relationship('Adress', backref='Actions')
    Message = relationship('Message', backref='Info')

    @classmethod
    def write(cls, session, action, sender_adr_id, sender_id=None, mes_id=None):
        act_id = Action.get_action_id(session, action)
        sen_adr_id = sender_adr_id
        event = cls()
        event.Action_Id = act_id
        event.Sender_Id = sender_id
        event.Sender_Adr_Id = sen_adr_id
        event.Message_Id = mes_id
        session.add(event)
        session.commit()
        return event


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()
    actions = session.query(Action).all()
    if not actions:
        connected = Action('Connected')
        authorised = Action('Authorised')
        registered = Action('Registered')
        disconnected = Action('Disconnected')
        mes = Action('Message')
        session.add_all([connected, authorised, registered, disconnected, mes])
        session.commit()
        User.registration(session, admin.USERNAME, admin.LOGIN, admin.PASSWORD)
        User.registration(session, 'All users', 'dfsdhfoas', 'lfvl;df')
        Adress.get_adr_id(session, 'Offline')
