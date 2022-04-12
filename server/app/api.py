from os import replace
from flask_restful import Resource
from flask import request,redirect,session, render_template
from flask_restful import reqparse
from flask.helpers import flash
from flask_sqlalchemy import _record_queries
from requests.api import delete
from sqlalchemy.util.langhelpers import portable_instancemethod
import werkzeug
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app as app

from app import tasks
from flask import Flask,send_file,send_from_directory
# from flask_cors import cross_origin
from . import cache

import random
import string

from .models import  Cards, Decks, Users, Roles
from .database import db

import datetime

from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required,login_user,current_user,auth_required,logout_user

from time import perf_counter_ns

# login_manager = LoginManager()
# login_manager.init_app(app)
# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(user_id)

user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = Security(app, user_datastore)








deck_owner_post_args = reqparse.RequestParser()
deck_owner_post_args.add_argument('deck_id')






#---------------------------------not kaam ka anymore--------------------------------------------------------
user_post_args = reqparse.RequestParser()
user_post_args.add_argument('email')
user_post_args.add_argument('password')

class Register(Resource):

    def post(self):

        #post variables
        args = user_post_args.parse_args()

        #length constraint
        if len(args['email']) < 6:
            return ('username short',320)
        elif len(args['password']) < 6:
            return ('password short',320)

        #user instance check
        user = Users.query.filter_by(email = args['email']).first()

        if not user:
            new_user = Users(email = args['email'], 
                            password=generate_password_hash(args['password'],method='sha256'),
                            fs_uniquifier = ''.join(random.choice(string.printable) for i in range(15)),
                            )
            print(new_user,args['email'])
            try:
                #success
                db.session.add(new_user)
                db.session.commit()
                # login_user(new_user)
                return ('Success',200)
            except:
                # unknown error
                return ('error',500)
        else:
            #username taken
            return ('username taken',320)
class Login(Resource):
    @auth_required("token")
    def post(self):
        # #taking parameters
        # args = user_post_args.parse_args()
        # # print("####################################################freezed############################################### ")
        # #checking user instance
        # user = Users.query.filter_by(username = args['username']).first()

        # if user:
        #     if check_password_hash(user.password,args['password']):
        #         login_user(user)
        #         #success
        #         return 'success'
        #     else:
        #         flash('Password not correct', category='error')
        #         return 'error'
        # else:
        #         flash('user not found', category='error')
        #         return 'error'
        return current_user.id
#---------------------------------not kaam ka anymore--------------------------------------------------------

# -----------------------------------------working------------------------------------- #

# used to add deck and takes deck name as parameter
deck_add_post_args = reqparse.RequestParser()
deck_add_post_args.add_argument('name')
class AddDeck(Resource):
    # @cross_origin()
    @auth_required("token")
    def post(self):
        args = deck_add_post_args.parse_args()
        exists = Decks.query.filter_by(name = args['name'] , user_id = current_user.id ).first() 
        error = {
            "meta" : {
                "code" : 312
            },
            "response":{
                "error" : "error"
            }
        } 
        #no name
        if args['name'] == '':
            error["response"]["error"] = "Name not provided"
            return error

        #name exists
        if exists:
            error["response"]["error"] = "Deck name exists"
            return error
        else:
            new = Decks(name = args['name'],user_id = current_user.id)
            user = Users.query.filter_by(id = current_user.id).first()
            user.decks_created_month +=1
        try:
            db.session.add(new)
            db.session.commit()
            success ={
                "meta" : {
                    "code" : 200
                },
                "response":{
                    "message" : "deck_info"
                }
            } 
            #success
            return success
        except Exception as err:
            return err


class ReturnDecks(Resource):
    @auth_required("token")
    def get(self):
        decks_init = Decks.query.filter_by(user_id=current_user.id)
        decks = []
        # user = Users.query.filter_by(id = current_user.id).first()
        # user.visited_month += user.visited_month + 1 
        # db.session.commit()
        for deck in decks_init:
            #score
            if(deck.count!=0):
                final_score = "{:.2f}".format(deck.score/deck.count)
            else:
                final_score = 0

            #date method
            date_now_arr = ([deck.last_rev.strftime('%d'),'-',deck.last_rev.strftime('%m'),'-',deck.last_rev.strftime('%G'),' | ',deck.last_rev.strftime('%H'),':',deck.last_rev.strftime('%M')])
            date_now_final= ''.join(date_now_arr)

            #info dictionary
            deck_info = {
                "id" : deck.id,
                "name" : deck.name,
                "last_rev" : date_now_final,
                "score" : final_score
            }
            decks.append(deck_info)
        if decks == []:
            response = {
                "meta" : {
                    "code" : 420
                },
                "response" : {
                    "message" : "No Decks to show"
                }
            }
            return response   
        success = {
            "meta" : {
                "code" : 200
            },
            "response" : {
                "data" : decks
            }       
        }    
        return success


card_add_post_args = reqparse.RequestParser()
card_add_post_args.add_argument('front')
card_add_post_args.add_argument('back')
card_add_post_args.add_argument('deck_id')

class AddCard(Resource):
    @auth_required("token")
    def post(self):
        error = {
            "meta":{
                "code" : 312
            },
            "response":{
                "error" : "error"
            }
        }

        args = card_add_post_args.parse_args()
        deck_search = Decks.query.filter_by(id=args['deck_id'],user_id= current_user.id).first()
        if(args['front'] == '' or args['back'] == ''):
            error["response"]["error"] = "Fields cannot be empty"
            return error
        if int(deck_search.user_id) == int(current_user.id) :
            new_card = Cards(front = args['front'], back = args['back'], deck_id = args['deck_id'])
            user = Users.query.filter_by(id = current_user.id).first()
            user.cards_created_month += user.cards_created_month + 1 
            db.session.commit()
            try:
                db.session.add(new_card)
                db.session.commit()
                card_info = {
                    "count" : -1,
                    "front" : new_card.front,
                    "back" : new_card.back,
                    "id" : new_card.id
                }
                success ={
                    "meta":{
                        "code" : 200
                    },
                    "response":{
                        "data" : card_info
                }  
                }
                return success
            except Exception as error:
                error["response"]["error"] = "something went wrong"
                return error
        else:
            return 'not allowed'



class ReturnDeckOwner(Resource):
    def get(self):
        args = deck_owner_post_args.parse_args()
        deck = Decks.query.filter_by(id = args['deck_id']).first()
        # user_id = deck['username']
        return deck.user_id



cards_get_args = reqparse.RequestParser()
cards_get_args.add_argument('deck_id')

class ReturnCards(Resource):
    @auth_required("token")
    def post(self):
        args = cards_get_args.parse_args()
        deck = Decks.query.filter_by(id = args['deck_id']).first()
        owned = deck.user_id == current_user.id
        if owned:
            cards_init = Cards.query.filter_by(deck_id = args['deck_id']).all()
            cards = []
            count = 0
            for card in cards_init:
                count += 1
                card_info = {
                    "count" : count,
                    "front" : card.front,
                    "back" : card.back,
                    "id" : card.id
                }
                cards.append(card_info)
            success = {
                "meta" : {
                    "code" : 200
                },
                "response":{
                    "data" : cards,
                    "deck_name" : deck.name
                }
            }
            return success
        else:
            error = {
                "meta" : {
                    "code" : 312
                },
                "response":{
                    "error" : "deck is not owned by this user"
                }                
            }
            return error

score_post_args = reqparse.RequestParser()
score_post_args .add_argument('score')
score_post_args .add_argument('deck_id')
class Review(Resource):
    @auth_required("token")
    def post(self):
        args = score_post_args.parse_args()
        # deck = Decks.query.filter_by(id = args['deck_id']).first()
        # owned = deck.user_id == current_user.id
        # if owned:
        error = {
            "meta" : {
                "code" : 312
            },
            "response":{
                "error" : "error"
            }                
        }
        deck_search = Decks.query.filter_by(id=args['deck_id']).first()
        if deck_search:
            owned = (deck_search.user_id == current_user.id)
        else:
            error["response"]["error"] = "deck not present"
            return error
        # print(args)

        if owned:
            deck_search.score += int(args['score'])
            deck_search.count += 1
            date = datetime.datetime.now()
            # s= ''
            # date_now_arr = ([date.strftime('%d'),'-',date.strftime('%m'),'-',date.strftime('%G'),',',date.strftime('%H'),':',date.strftime('%M')])
            # date_now= s.join(date_now_arr)
            deck_search.last_rev = date
            user = Users.query.filter_by(id = current_user.id).first()
            user.revised = True
            user.revised_month += 1
            # try:    
            db.session.commit()
            success = {
                "meta" : {
                    "code" : 200
                },
                "response":{
                    "message" : "reviewed succesfully"
                }                
            }
            return success
        error["response"]["error"] = "you don't own this deck"
        return error
# -----------------------------------------working-end------------------------------------- #

deck_delete_args = reqparse.RequestParser()
deck_delete_args.add_argument('deck_id')
class DeleteDeck(Resource):
    def post(self):
        args = deck_delete_args.parse_args()
        deck = Decks.query.filter_by(id = args['deck_id']).first()
        # print(deck.user_id,args['user_id'])
        if int(deck.user_id) == current_user.id:
            db.session.delete(deck)
            db.session.commit()
            return 'success'
        else:
            return 'not authorised'

class Logout(Resource):
    def get(self):
        logout_user()
        return "done"

edit_card_post = reqparse.RequestParser()
edit_card_post .add_argument('front')
edit_card_post .add_argument('back')
edit_card_post .add_argument('card_id')
edit_card_post .add_argument('count')



class EditCard(Resource):
    def post(self):
        args = edit_card_post.parse_args()
        card = Cards.query.filter_by(id = args['card_id']).first()
        card.front = args['front']
        card.back = args['back']
        returnCard = {
            "count" : args['count'],
            "front" : card.front,
            "back" : card.back,
            "id" : card.id
        }
        try:
            db.session.commit()
            return returnCard
        except Exception as e:
            return e

edit_deck_post = reqparse.RequestParser()
edit_deck_post .add_argument('deck_id')
edit_deck_post .add_argument('name')
# edit_deck_post .add_argument('index')
edit_deck_post .add_argument('score')
edit_deck_post .add_argument('rev')


class EditDeck(Resource):
    def post(self):
        args = edit_deck_post.parse_args()
        deck = Decks.query.filter_by(id = args['deck_id']).first()
        deck.name = args['name']
        deck_info = {
            "id" : deck.id,
            "name" : args['name'],
            "last_rev" : args['rev'],
            "score" : args['score']
        }

        try:
            db.session.commit()
            return deck_info
        except Exception as e:
            return e
    

class UserEmail(Resource):
    @auth_required("token")
    def get(self):
        return (current_user.email, 200)
        


class Work(Resource):
    @auth_required('token')
    def post(self):
        user_id = current_user.id
        task = tasks.create_csv.delay(user_id)
        result = task.wait()
        return send_file(result, mimetype = "text/csv")


class DeleteCSV(Resource):
    @auth_required('token')
    def post(self):
        user_id = current_user.id
        task = tasks.delete_csv.delay(user_id)
        result = task.wait()
        return result


upload_file_post = reqparse.RequestParser()
upload_file_post .add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
class UploadFile(Resource):
    @auth_required('token')
    def post(self):

        ALLOWED_EXTENSIONS = {'csv'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        args = upload_file_post.parse_args()
        # print(args['file'])

        if args['file']:
            user_id = current_user.id 
            file = args['file']
            if file and allowed_file(file.filename):
                filename = 'uploads/uploaded_'+str(current_user.id)+'.csv'
                file.save(filename)            
                task = tasks.upload_and_read_csv.delay(user_id,filename)
                result = task.wait()
                return "done"
            return "not valid filetype"

            return result
        return "file not provided"
            

class Reminders_daily(Resource):
    @auth_required('token')
    def post(self):
        # user_id = current_user.id
        task = tasks.daily_reminder.delay()
        result = task.wait()
        return result

class Monthly_report(Resource):
    @auth_required('token')
    def post(self):
        # user_id = current_user.id
        task = tasks.monthly_report.delay()
        result = task.wait()
        return result

class AllDecks(Resource):
    @cache.cached(timeout=50)
    def get(self):
        decks_init = Decks.query.all()
        decks = []
        # user = Users.query.filter_by(id = current_user.id).first()
        # user.visited_month += user.visited_month + 1 
        # db.session.commit()
        for deck in decks_init:
            #score
            if(deck.count!=0):
                final_score = "{:.2f}".format(deck.score/deck.count)
            else:
                final_score = 0

            #date method
            date_now_arr = ([deck.last_rev.strftime('%d'),'-',deck.last_rev.strftime('%m'),'-',deck.last_rev.strftime('%G'),' | ',deck.last_rev.strftime('%H'),':',deck.last_rev.strftime('%M')])
            date_now_final= ''.join(date_now_arr)

            #info dictionary
            deck_info = {
                "id" : deck.id,
                "name" : deck.name,
                "last_rev" : date_now_final,
                "score" : final_score
            }
            decks.append(deck_info)
        if decks == []:
            response = {
                "meta" : {
                    "code" : 420
                },
                "response" : {
                    "message" : "No Decks to show"
                }
            }
            return response   
        success = {
            "meta" : {
                "code" : 200
            },
            "response" : {
                "data" : decks
            }       
        }    
        return success





allcards_get_args = reqparse.RequestParser()
allcards_get_args.add_argument('deck_id')
class AllCards(Resource):
    # @cache.cached(timeout=50)
    def post(self):
        start = perf_counter_ns()
        args = allcards_get_args.parse_args()
        deck = Decks.query.filter_by(id = args['deck_id']).first()

        cards_init = Cards.query.filter_by(deck_id = args['deck_id']).all()
        cards = []
        count = 0
        for card in cards_init:
            count += 1
            card_info = {
                "count" : count,
                "front" : card.front,
                "back" : card.back,
                "id" : card.id
            }
            cards.append(card_info)
        success = {
            "meta" : {
                "code" : 200
            },
            "response":{
                "data" : cards,
                "deck_name" : deck.name
            }
        }
        stop = perf_counter_ns()
        print("time taken", stop-start)
        return success


