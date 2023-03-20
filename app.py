from flask import Flask, render_template, flash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@127.0.0.1:3306/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'project'

from controllers import *
from extensions import *    
from models import *


admin.add_view(ModelView(Products, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Contacts, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Subcategory, db.session))
admin.add_view(ModelView(Reviews, db.session))
admin.add_view(ModelView(Newsletter, db.session))



if '__name__' == '__main__':
    app.init_app(db)
    app.init_app(migrate)