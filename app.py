"""Blogly application."""

from flask import Flask, request, render_template, redirect
from sqlalchemy import desc
#from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
#debug = DebugToolbarExtension(app)

connect_db(app)

# with app.app_context():
#     db.drop_all()
#     db.create_all()

#     Alan = User(first_name='Alan', last_name='Alda')
#     Joel = User(first_name='Joel', last_name='Burton')
#     Jane = User(first_name='Jane', last_name='Smith')
#     db.session.add(Alan)
#     db.session.add(Joel)
#     db.session.add(Jane)

#     post1 = Post(title='First Post!', content='Yeah!', user_id='2')
#     post2 = Post(title='Yet Another Post', content='Yeah! Another one!', user_id='2')
#     post3 = Post(title='Flask Is Awesome', content='Yeah! The third one!', user_id='2')
#     db.session.add(post1)
#     db.session.add(post2)
#     db.session.add(post3)

#     tag1 = Tag(name='General')
#     tag2 = Tag(name='Fun')
#     tag3 = Tag(name='Bloop')
#     db.session.add(tag1)
#     db.session.add(tag2)
#     db.session.add(tag3)

#     post_tag1 = PostTag(post_id=1, tag_id=1)
#     post_tag2 = PostTag(post_id=1, tag_id=2)
#     post_tag3 = PostTag(post_id=2, tag_id=2)
#     post_tag4 = PostTag(post_id=3, tag_id=1)
#     db.session.add(post_tag1)
#     db.session.add(post_tag2)
#     db.session.add(post_tag3)
#     db.session.add(post_tag4)   

#     db.session.commit()

############### Part I ####################
@app.route('/')
def home_page():
    """show home page"""
    posts = db.session.query(Post).order_by(desc(Post.created_at)).limit(5).all()
    return render_template('home.html', posts=posts)


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
    with app.app_context():
        #??????  db.session.delete(u)
        db.session.query(User).filter_by(id=user_id).delete()
        db.session.commit()
    
    return redirect('/users')

############### Part II ##################
@app.route('/users/<int:user_id>/posts/new')
def show_add_post_page(user_id):
    """Add a new post for a user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Add a new post for a user"""
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = request.form.getlist("tags")
    post = Post(title=title, content=content, user_id=user_id)
    
    with app.app_context(): 
        db.session.add(post)
        db.session.flush()
        for tag_id in tag_ids:
            post_tag = PostTag(post_id=post.id, tag_id=tag_id)
            db.session.add(post_tag)
        db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    """ Show a post """
    post = Post.query.get_or_404(post_id)
    user_name = post.user.first_name + post.user.last_name
    tags = post.tags
    return render_template('detail_post.html', post=post, name=user_name, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_page(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = request.form.getlist("tags")

    with app.app_context():
        db.session.query(Post).filter_by(id=post_id).update({'title': title, 'content': content})
        db.session.flush()
        for tag_id in tag_ids:
            post_tag = PostTag(post_id=post_id, tag_id=tag_id)
            db.session.add(post_tag)
        db.session.commit()
    
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  
    pts = post.assignments 
    user_id = post.user_id

    with app.app_context():
        for pt in pts:
            db.session.query(PostTag).filter_by(post_id=pt.post_id).delete()
        db.session.query(Post).filter_by(id=post_id).delete()
        db.session.commit()
    
    return redirect(f"/users/{user_id}")

############## Part III ################
@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)

@app.route('/tags/new')
def show_create_tag_page():
    return render_template('new_tag.html')

@app.route('/tags/new', methods=["POST"])
def create_tag():
    name = request.form['tag-name']
    tag = Tag(name=name)
    with app.app_context():
        db.session.add(tag)
        db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Show all the posts that have this tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('detail_tag.html',tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_page(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    name = request.form['tag-name']

    with app.app_context():
        db.session.query(Tag).filter_by(id=tag_id).update({'name': name})
        db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    pts = tag.assignments
    with app.app_context():
        for pt in pts:
            db.session.query(PostTag).filter_by(post_id=pt.post_id).delete()
        db.session.query(Tag).filter_by(id=tag_id).delete()
        db.session.commit()

    return redirect('/tags')