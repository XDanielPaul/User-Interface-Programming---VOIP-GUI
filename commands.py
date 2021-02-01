import click
from flask.cli import with_appcontext
from models import User, Contact, Notification
from extensions import db


@click.command(name='restart_tables')
@with_appcontext
def restart_tables():
    db.drop_all()
    db.create_all()


@click.command(name='fill_database')
@with_appcontext
def fill_database():
    user = User(username="User", image_path="/static/profile.jpg")
    db.session.add(user)
    db.session.commit()
    c_jotaro = Contact(name="Jotaro", image_path="/static/jotaro.jpg")
    db.session.add(c_jotaro)
    c_dio = Contact(name="Dio", image_path="/static/dio.jpg")
    db.session.add(c_dio)
    c_joseph = Contact(name="Joseph", image_path="/static/joseph.jpg")
    db.session.add(c_joseph)
    c_polnareff = Contact(name="Polnareff", image_path="/static/polnareff.jpg")
    db.session.add(c_polnareff)
    c_yoshikage = Contact(name="Yoshikage", image_path="/static/yoshikage.jpg")
    db.session.add(c_yoshikage)
    c_zepelli = Contact(name="Zepelli", image_path="/static/zepelli.jpg")
    db.session.add(c_zepelli)
    db.session.commit()

    user.contacts.append(c_jotaro)
    user.contacts.append(c_dio)
    user.contacts.append(c_joseph)
    user.contacts.append(c_polnareff)
    user.contacts.append(c_yoshikage)
    user.contacts.append(c_zepelli)
    db.session.commit()
