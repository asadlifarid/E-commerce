from flask import render_template, request, redirect, url_for, flash
from app import app
from models import * 
from forms import *
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user ,current_user




@app.route('/products', methods=['GET', 'POST'])  
@login_required
def shop():
    favorites_count = Favorite.query.filter_by(
        user_id=current_user.id).count()
    products = Products.query.all()
    cat = Category.query.all()
    subcategories = Subcategory.query.all()
    sizes = Size.query.all()
    colors = Color.query.all()
    category = request.args.get('category')
    color = request.args.get('color')
    size = request.args.get('size')
    sub_category = request.args.get('sub_category')
    min_price = request.args.get('min')
    max_price = request.args.get('max')
    
    product_count = Color.count_color()
    product_count = Size.count_size()
    product_count = Category.count_cat()
    
    name = request.args.get('name')
    
    
    if name:
        products = Products.query.filter(Products.name.ilike(f'%{name}%')).all()
        
    if category:
        products = Category.query.filter_by(id=category).first().relation_3
        
    if sub_category:
        products = Subcategory.query.filter_by(id=sub_category).first().subcategory_
        
    if color:
        products = Color.query.filter_by(id=color).first().relation_1
        
    if size:
        products = Size.query.filter_by(id=size).first().relation_2
        
    if min_price and max_price:
        products = Products.query.filter(Products.price.between(min_price, max_price)).all()
        
    form = NewsletterForm()

    if request.method == 'POST':
        form = NewsletterForm(request.form)

        if form.validate_on_submit():
            newsletter = Newsletter(
                name = form.name.data, 
                email = form.email.data
            )
            newsletter.save()
        redirect(url_for('shop'))
    return render_template('shop.html', cat = cat, products=products, subcategories = subcategories, form=form, sizes=sizes, colors=colors, product_count=product_count, favorites_count=favorites_count )






@app.route('/detail/<int:id>', methods=['GET', 'POST'])
def product_detail(id):
    print(id)
    p = Products.query.first()
    colors = Color.query.all()
    size = Size.query.all()
    p_string = Products.query.filter_by(id=id).first()
    form = ReviewForm(formdata=None)
    print('form post olundu')
    if request.method == 'POST':
        form = ReviewForm(request.form)
        print(request.form)
        if form.validate_on_submit():
            print('validate olunub')
            review = Reviews(
                message = form.message.data,
                product_id = id,
                user_id = current_user.id
            )
            review.save()
        form = ReviewForm(formdata=None)    
    reviews=Reviews.query.filter_by(product_id=id).all()
    products = Products.query.filter_by(id=id).first()
    return render_template('detail.html', p = p, colors = colors, size = size, p_string = p_string, products=products, form=form, reviews=reviews)






@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.form)
        print('valid')
        user = User.query.filter_by(email = form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('User signed in!')
            return redirect(url_for('shop'))
        else:
            flash("User didn't sign in. Something went wrong ")
            return redirect(url_for('login_page')), "Maybe you don't have any account. Do you want to register?"
    return render_template('login.html', form = form, error = error)




@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactsForm()
    print('post!!!!!!!!')
    print(request.form)
    if request.method == 'POST':
        print('sent')
        form = ContactsForm(request.form)
        print(request.form)
        if form.validate_on_submit():
            print('valid')
            contacts = Contacts(
                name = form.name.data, 
                email = form.email.data, 
                subject = form.subject.data, 
                message = form.message.data
                )
            contacts.save()
        return redirect(url_for('shop'))
    return render_template('contact.html', form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')




@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            user = User(
                full_name = form.name.data,
                email = form.email.data,
                password = generate_password_hash(form.password.data)
                
            )
            user.save()
        return redirect(url_for('login_page'))
    return render_template('register.html', form = form)





@app.route('/myfavorite/<int:products_id>', methods=['POST', 'GET'])
def my_favorite(products_id):
    product = Products.query.get_or_404(products_id)
    print(product)

        
    favorite = Favorite(
        products_id=products_id,
        user_id=current_user.id
    )
    if Favorite.query.filter_by(products_id = products_id, user_id=current_user.id).first() is not None:
        flash("You have already made a choice :) ")
        
    else: 
        db.session.add(favorite)
        db.session.commit()

    return myfavorite()
    


@app.route('/my_favs', methods=['GET'])
def myfavorite():
    favorites_count = Favorite.query.filter_by(user_id=current_user.id).count()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    
    return render_template('favorites.html', favorites=favorites, fav_count=favorites_count)
 
 
 
 
@app.route('/products/<int:id>', methods=['GET', 'POST']) 
def remove_favs(id):
    
    fav = Favorite.query.filter_by(products_id=id,
                                 user_id=current_user.id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return myfavorite()
    return render_template('favorites.html')
