from models import User, Contact, Notification
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from commands import restart_tables, fill_database
from extensions import db, login_manager
from datetime import timedelta, datetime
import random
import string
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

db.init_app(app)
login_manager.init_app(app)
app.cli.add_command(restart_tables)
app.cli.add_command(fill_database)

login_manager.login_view = 'app.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


''' HOME '''


@app.route("/", methods=['GET', 'POST'])
def home():
    user = User.query.first()
    return render_template("home.html", user=user)


@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    username = request.form.get("username")
    print(username)
    user = User.query.first()
    user.username = username
    db.session.commit()

    return jsonify({'result': 'success', 'username': username})


@app.route("/filter_contacts", methods=['GET', 'POST'])
def filter_contacts():
    user = User.query.first()
    searchbox = request.form.get("text")
    contained = []
    not_contained = []
    contacts = Contact.query.filter(
        Contact.name.contains(str(searchbox))).all()
    for contact in contacts:
        if(contact in user.contacts):
            contained.append(contact)
        else:
            not_contained.append(contact)

    return render_template('contacts.html', contained=contained, not_contained=not_contained)


@app.route("/filter_notifications", methods=['GET', 'POST'])
def filter_notifications():
    searchbox = request.form.get("text")
    notifications_time = Notification.query.filter(
        Notification.time_created.contains(str(searchbox))).all()
    notifications_date = Notification.query.filter(
        Notification.date_created.contains(str(searchbox))).all()

    notifs = Notification.query.all()
    notif_list = []
    for notif in notifs:
        if str(searchbox) in notif.contact.name:
            notif_list.append(notif)

    notifications = notifications_date + notifications_time + notif_list

    return render_template('notifications.html', notifications=notifications)


@ app.route("/deleteContact", methods=['GET', 'POST'])
def deleteContact():
    user = User.query.first()
    contact = Contact.query.filter_by(
        id=int(request.form.get("contact_id"))).first()
    user.contacts.remove(contact)
    db.session.commit()
    return render_template('contacts.html', contained=user.contacts)


@ app.route("/addContact", methods=['GET', 'POST'])
def addContact():
    user = User.query.first()
    contact = Contact.query.filter_by(
        id=int(request.form.get("contact_id"))).first()
    user.contacts.append(contact)
    db.session.commit()
    return render_template('contacts.html', contained=user.contacts)


@ app.route("/showall_contacts", methods=['GET', 'POST'])
def showall_contacts():
    user = User.query.first()
    return render_template('contacts.html', contained=user.contacts)


@ app.route("/showall_notifications", methods=['GET', 'POST'])
def showall_notifications():
    notifications = Notification.query.all()
    return render_template('notifications.html', notifications=notifications)


@ app.route("/createNotification", methods=['GET', 'POST'])
def createNotification():

    today = datetime.now()
    today_date = today.strftime("%d/%m/%Y")
    today_time = today.strftime("%H:%M:%S")
    user = User.query.first()
    contact = Contact.query.filter_by(
        id=int(request.form.get("contact_id"))).first()
    notification = Notification(
        from_user=1, date_created=today_date, time_created=today_time, timestamp=request.form.get("timestamp"), confirmed=0)
    db.session.commit()
    user.notifications.append(notification)
    contact.notifications.append(notification)
    db.session.commit()

    notifications = Notification.query.all()
    return render_template('notifications.html', notifications=notifications)


@ app.route("/confirmNotification", methods=['GET', 'POST'])
def confirmNotification():
    notification = Notification.query.filter_by(
        id=int(request.form.get("notification_id"))).first()
    print(notification.confirmed)
    notification.confirmed = 1
    db.session.commit()
    notifications = Notification.query.all()
    return render_template('notifications.html', notifications=notifications)


@ app.route("/deleteNotification", methods=['GET', 'POST'])
def deleteNotification():
    notification = Notification.query.filter_by(
        id=int(request.form.get("notification_id"))).first()
    db.session.delete(notification)
    db.session.commit()
    notifications = Notification.query.all()
    return render_template('notifications.html', notifications=notifications)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
