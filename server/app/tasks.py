from app.workers import celery
from datetime import datetime
import time
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required,login_user,current_user,auth_required
from .models import  Cards, Decks, Users, Roles
from .database import db
from flask import Flask,send_file,send_from_directory
import os

from celery.schedules import crontab


from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# send_email("lakshaydhiman12@gmail.com","hello kaise ho","This is a test message bro")



# @celery.task()
# def say_hello(item): 
#     for i in item:
#         time.sleep(1)
#         print("INSIDE TASK")
#         print("i")
#     return "done"
        

# export job, csv format for decks and cards

# ---------- csv format ------------ #
#
# deck name, deck last rev, deck sore, deck count, card front, card back, card score
#
# ----------------------------------#


@celery.task()
def create_csv(user_id): 
    # time.sleep(5)
    decks = Decks.query.filter_by(user_id = user_id).all()
    deck_info = []
    for deck in decks:
        string = str(deck.id)+ ", " + str(deck.name)+ ", " + str(deck.last_rev) + ", " + str(deck.count)+ ", " + str(deck.score)
        deck_info.append(string)

    complete_info = []
    complete_info.append("deck id, deck name, deck last rev, deck count, deck score, card front, card back, card id\n")
    for deck in deck_info:
        deck_id = int(deck.split(",")[0])
        # print(deck_id)
        cards = Cards.query.filter_by(deck_id = deck_id).all()
        for card in cards:
            complete_info.append(str(deck)+", "+str(card.front)+", "+str(card.back)+", "+str(card.id)+"\n")
    print(complete_info)

    try:
        filename = 'exports/export_'+str(user_id)+'.csv'
        if os.path.exists(filename):
            os.remove(filename)
        fileIn =  open(filename,'a+')
        for line in complete_info:
            fileIn.write(line)
        return filename
    except Exception as e:
        return e
    
@celery.task()
def delete_csv(user_id): 
    try:
        filename = 'exports/export_'+str(user_id)+'.csv'
        os.remove(filename)
        return "done"
    except Exception as e:
        return e


@celery.task()
def upload_and_read_csv(user_id,filename): 
    file = open(filename,'r')
    count = 0
    for line in file:
        if count == 0:
            count = 1
            continue
        else:
            data = line.split(", ")
            # if not len(data) == 8:
            #     return "Invalid CSV file"
            # print(data)
            deck_name = data[1]

            deck = Decks.query.filter_by( name = deck_name , user_id = user_id ).first()
            if not deck:
                deck_last_rev = datetime.strptime(data[2], '%Y-%m-%d %H:%M:%S.%f')
                deck_count = data[3]
                deck_score = data[4]
                newDeck = Decks(name = deck_name, user_id = int(user_id) , last_rev = deck_last_rev, count = int(deck_count), score = int(deck_score))
                db.session.add(newDeck)
                db.session.commit()
                print("decks added")
                deckId = Decks.query.filter_by( name = deck_name , user_id = user_id ).first().id
                print(deckId)

                deck_id = deckId
            else:
                deck_id = deck.id
            
            card_front = data[5]
            card_back = data[6]
            newCard = Cards(front = card_front, back = card_back, deck_id = deck_id)
            db.session.add(newCard)
            db.session.commit()
    os.remove(filename)
    return "Successfull"





def send_email(to_address, subject, message):
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "flashkards@gmail.com"
    SENDER_PASSWORD = ""
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(host = SMTP_SERVER_HOST, port = SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour = 9, minute=30),
        daily_reminder.s(),
        name="everyday"
    )

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_month = 29, hour=7, minute=0),
        monthly_report.s(),
        name="every month"
    )

@celery.task()
def daily_reminder():
    all_users = Users.query.all()
    for user in all_users:
        if not user.revised:
            message = "We noticed you have not revised any deck today till now, it's a reminder for you to revise the decks and improve your learning experience."
            subject = "Reminder | Revise the decks on FLASHKARDS"
            email = user.email
            send_email(email,subject,message)
        user.revised = False
        db.session.commit()
    return "done"



@celery.task()
def monthly_report():
    users = Users.query.all()
    for user in users:
        (email , deck_no, card_no, revised_no) = (user.email, user.decks_created_month, user.cards_created_month, user.revised_month)
        with open("template/monthly_report.html") as file_ :
            template = Template(file_.read())
            message = template.render(email= str(email), deck_no =str(deck_no), card_no=str(card_no),revised_no=str(revised_no))
            print("sending email")
        (user.decks_created_month, user.cards_created_month, user.revised_month) = (0,0,0)
        db.session.commit()
        send_email(email, "MONTHLY REPORT | FLASHKARDS", message)
    return "success"

