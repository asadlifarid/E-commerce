from app import app
from extensions import db, login_manager
from flask_login import UserMixin, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy.schema import UniqueConstraint
from flask_security import RoleMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer , primary_key = True)
    full_name = db.Column(db.String(100) , nullable = False)
    email = db.Column(db.String(100) , nullable = False)
    password = db.Column(db.String(255) , nullable = False)
   

    def __init__(self , full_name , email , password):
        self.full_name = full_name
        self.email = email
        self.password = password
        

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.full_name

    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
class Color(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    name = db.Column(db.String(100))
    relation_1 = db.relationship('Products', backref = 'color')
    
    @classmethod
    def count_color(cls):
        return cls.query.count()
   
   
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()    
        
        
class Size(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    relation_2 = db.relationship('Products', backref = 'size')
    
    @classmethod
    def count_size(cls):
        return cls.query.count()
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()    
        




class Category(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100))
    relation_3 = db.relationship('Products', backref = 'category')
    
    @classmethod
    def count_cat(cls):
        return cls.query.count()
    
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()      
        
   
   
        
class Subcategory(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    subcategory_ = db.relationship('Products', backref = 'subcategory')
    
    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id
        
    def __repr__(self):
        return self.name

    
    def save(self):
        db.session.add(self)
        db.session.commit()
  
  
  
class Reviews(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.String(255))
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='reviews')
    
    
    def __init__(self, message, product_id, user_id):
        self.message = message
        self.product_id = product_id
        self.user_id = user_id
        
    def __repr__(self):
        return self.message
    
    def save(self):
        db.session.add(self)
        db.session.commit()



  
class Favorite(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    products_id = db.Column(db.ForeignKey('products.id'), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.relationship('Products', backref=db.backref('favorite', lazy=True))
    __table_args__ = (UniqueConstraint(user_id, products_id), )
    
    @classmethod
    def count_fave(cls):
        return cls.query.count()
    

    def __init__(self, products_id, user_id):
        self.products_id = products_id,
        self.user_id=user_id
        
    def __repr__(self):
        return self.products_id
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        



class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=False)
    old_price = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(100), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    
    def __init__(self, name, price, old_price, category_id, size_id, color_id, description, image_url, subcategory_id):
        self.name = name
        self.price = price
        self.old_price = old_price
        self.category_id = category_id
        self.size_id = size_id
        self.color_id = color_id
        self.description = description
        self.image_url = image_url
        self.subcategory_id=subcategory_id
        
    
     
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()  
        
        
        
class Contacts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    message = db.Column(db.String(300))
    
    def __init__(self, name, email, subject, message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
    def __repr__(self):
        return self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()  

    