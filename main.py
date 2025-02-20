from flask import Flask, render_template, request, session, redirect, url_for, flash
from functools import wraps
import db


app = Flask(__name__)
app.secret_key = "The_Power_Of_Friendship"


# initialize database on startup
db.init_db()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    reviews = db.get_all_reviews()
    return render_template("index.html", reviews=reviews)


@app.route("/search")
def search():
    query = request.args.get('q', '')
    reviews = db.search_reviews(query) if query else []
    return render_template("search.html", reviews=reviews, query=query)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('username'):
        return redirect(url_for('home'))

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.check_login(username, password)
        if user:
            session['id'] = user['id']
            session['username'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get('username'):
        return redirect(url_for('home'))

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if db.register_user(username, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        flash('Username already exists or invalid input', 'error')
    
    return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_review():
    if request.method == "POST":
        game_title = request.form.get('game_title')
        review_text = request.form.get('review_text')
        rating = request.form.get('rating')
        
        if db.add_review(session['id'], game_title, review_text, rating):
            flash('Review added successfully!', 'success')
            return redirect(url_for('home'))
        flash('Error adding review. Please try again.', 'error')
    
    return render_template("add_review.html")


@app.route("/edit/<int:review_id>", methods=["GET", "POST"])
@login_required
def edit_review(review_id):
    review = db.get_review_by_id(review_id)
    
    if not review or review['user_id'] != session['id']:
        flash('You can only edit your own reviews', 'error')
        return redirect(url_for('home'))
    
    if request.method == "POST":
        game_title = request.form.get('game_title')
        review_text = request.form.get('review_text')
        rating = request.form.get('rating')
        
        if db.update_review(review_id, game_title, review_text, rating):
            flash('Review updated successfully!', 'update')
            return redirect(url_for('home'))
        flash('Error updating review. Please try again.', 'error')
    
    return render_template("edit_review.html", review=review)


@app.route("/delete/<int:review_id>")
@login_required
def delete_review(review_id):
    review = db.get_review_by_id(review_id)
    
    if not review or review['user_id'] != session['id']:
        flash('You can only delete your own reviews', 'error')
        return redirect(url_for('home'))
    
    if db.delete_review(review_id):
        flash('Review deleted successfully!', 'delete')
    else:
        flash('Error deleting review', 'error')
    
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
