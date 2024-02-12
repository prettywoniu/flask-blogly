"""Blogly application."""

from flask import Flask, request, render_template, redirect
#from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
#debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    Alan = User(first_name='Alan', last_name='Alda')
    Joel = User(first_name='Joel', last_name='Burton')
    Jane = User(first_name='Jane', last_name='Smith')
    db.session.add(Alan)
    db.session.add(Joel)
    db.session.add(Jane)

    post1 = Post(title='First Post!', content='Yeah!', user_id='2')
    post2 = Post(title='Yet Another Post', content='Yeah! Another one!', user_id='2')
    post3 = Post(title='Flask Is Awesome', content='Yeah! The third one!', user_id='2')
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)

    db.session.commit()

@app.route('/')
def home_page():
    """show home page"""
    return redirect("/users")


@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    with app.app_context():
        users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def show_add_form():
    return render_template('new_user.html')


@app.route('/users/new', methods=["POST"])
def add_user():
    """add new user"""
    fname = request.form['first-name']
    lname = request.form['last-name']
    img_url = request.form['img-url']
    
    user = User(first_name=fname, last_name=lname, img_url=img_url)
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show info on a single user."""
    user =  User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("detail_user.html", user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_edit(user_id):
    """Edit info on a single user."""
    fname = request.form['first-name']
    lname = request.form['last-name']
    img_url = request.form['img-url']

    with app.app_context():
        db.session.query(User).filter_by(id=user_id).update({'first_name': fname, 'last_name': lname, 'img_url': img_url})
        db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete an user."""
    #?????????????????????
    #sqlalchemy.exc.InvalidRequestError: 
    #Object '<User at 0x7f36c876e710>' is already attached to session '2' (this is '3')
    # User.query.filter_by(id=user_id).delete()
    # u = User.query.get(user_id)
    with app.app_context():
        #??????  db.session.delete(u)
        db.session.query(User).filter_by(id=user_id).delete()
        db.session.commit()
    
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def show_add_post_page(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template("new_post.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Add a new post for a user"""
    title = request.form["title"]
    content = request.form["content"]
    post = Post(title=title, content=content, user_id=user_id)

    with app.app_context():
        db.session.add(post)
        db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    """ Show a post """
    post = Post.query.get_or_404(post_id)
    user_name = post.user.first_name + post.user.last_name
    return render_template('detail_post.html', post=post, name=user_name)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    title = request.form["title"]
    content = request.form["content"]

    with app.app_context():
        db.session.query(Post).filter_by(id=post_id).update({'title': title, 'content': content})
        db.session.commit()
    
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    with app.app_context():
        db.session.query(Post).filter_by(id=post_id).delete()
        db.session.commit()
    
    return redirect(f"/users/{user_id}")