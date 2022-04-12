from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from app import workers
# from flask_caching import Cache
from app import cache

app = Flask(__name__)
CORS(app)
cache.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SECRET_KEY'] = 'sakujotitla'
app.config['SECURITY_TOKEN_HEADER'] = "Authentication-Token"
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_PASSWORD_HASH'] = "bcrypt"
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/register'
app.config['SECURITY_PASSWORD_SALT'] = 'sakujotitlaisarealname'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_UNAUTHORIZED_View'] = None
app.config['SECURITY_CONFIRMABLE'] = False
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/1"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/2"
app.config['UPLOAD_FOLDER'] = '/uploads'
# app.config['CACHE_TYPE'] = "RedisCache"
# app.config['CACHE_REDIS_HOST'] = "localhost"
# app.config['CACHE_REDIS_PORT'] = 6379

# cache = Cache(app)
from app.database import db

celery = workers.celery
celery.conf.update(
    broker_url = app.config["CELERY_BROKER_URL"],
    result_backend = app.config["CELERY_RESULT_BACKEND"]
)

celery.Task = workers.ContextTask


db.init_app(app)
app.app_context().push()


#api thingy
api = Api(app)

# from app.routes import *
from app.api import AddCard, AddDeck, DeleteDeck, Logout, Register,Login, ReturnCards, ReturnDeckOwner, ReturnDecks, Review,EditCard,UserEmail,Work, DeleteCSV,UploadFile,Reminders_daily, AllDecks, AllCards, EditDeck, Monthly_report
api.add_resource(Register,'/api/register')
api.add_resource(Login,'/api/login')
api.add_resource(AddDeck,'/api/add/deck')
api.add_resource(ReturnDecks,'/api/get/decks')
api.add_resource(AddCard,'/api/add/card')
api.add_resource(ReturnDeckOwner,'/api/get/deckowner')
api.add_resource(ReturnCards,'/api/get/cards')
api.add_resource(Review,'/api/put/review')
api.add_resource(DeleteDeck,'/api/delete/deck')
api.add_resource(Logout,'/api/user/logout')
api.add_resource(EditCard,'/api/edit/card')
api.add_resource(UserEmail,'/api/get/useremail')
api.add_resource(Work,'/api/user/createcsv')
api.add_resource(DeleteCSV,'/api/user/delete_csv')
api.add_resource(UploadFile,'/api/user/upload')

api.add_resource(AllDecks,'/api/alldecks')
api.add_resource(AllCards,'/api/allcards')
api.add_resource(EditDeck,'/api/editdeck')

api.add_resource(Reminders_daily,'/api/remind')
api.add_resource(Monthly_report,'/api/report')






# from app.controler import *

if __name__ == '__main__':
    app.run(debug=True,host = '127.0.0.1',port = 8081)