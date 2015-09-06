"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, url_for

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage.
        Falmingos, Pink, Black 1950's Miami Kitchen.
        Index page that shows options to look at with simple menu
    """

    return render_template('homepage.html')

@app.route('/movie-list')
def movies_list_page():
    """Movie List Page. Can Organize Movie info in a table that you can Organize by title or release date
        WILL NEED ROUTES FOR AJAX
    """
    movies = Movie.query.order_by(Movie.title).all()
    return render_template('movies-list.html', movies=movies)


@app.route('/movie-detail/<int:id_movie>', methods=["GET"])
def movie_detail_page(id_movie):
    """Individual Movie Info Page.


        1.Given a user U who has not rated movie M, find all other users who have rated that movie.
        2.For each other user O, find the movies they have rated in common with user U.
        3.Pair up the common movies, then feed each pair list into the Pearson function to find similarity S.
        4.Rank the users by their similarities, and find the user with the highest similarity, O.
        5.Multiply the similarity coefficient of user O with their rating for movie M. This is your predicted rating.
    """

    movie = Movie.query.filter(Movie.movie_id == id_movie).one()
    ratings = Rating.query.filter(Rating.movie_id == id_movie)

     #will return None if none   
    user_who_have_rated = ratings.filter(Rating.movie_id == id_movie).all()

    #Average Rating
    #Pearson Prediction
    #Insult

    # # ADD PEARSON CORRELATION
    # if session.get('user_id'):
    #     has_user_rated = Rating.query.filter(Rating.user_id == session['user_id']).all()
    #     if has_user_rated == None:




    return render_template("movie-detail.html", movie=movie, ratings=ratings)
    #will need to pass movie query information through jinja into template


#to add a rating to db
@app.route('/movie-detail/<int:id_movie>',methods=["POST"])
def movie_detail_page_score(id_movie):
    """Individual Movie Info Page."""
    movie = Movie.query.filter(Movie.movie_id == id_movie).one()
    
    score = request.form.get('score')
    user_id = session['user_id']
    movie_id = movie.movie_id

    score_to_add = Rating(user_id=user_id, movie_id=movie_id, score=score) 
    db.session.add(score_to_add)
    db.session.commit()    

    flash('You added a score!')
    # return redirect('/movie-detail/%s' % movie_id)
    return redirect(url_for('movie_detail_page', id_movie=movie_id))
    #will need to pass movie query information through jinja into template


@app.route('/user-list')
def user_list_page():
    """List of all users in a pretty pretty table."""

    users = User.query.all()
    return render_template("user-list.html", users=users)


@app.route('/user-profile/<int:id_user>')
def user_detail_page(id_user):
    """User information on a  pretty pretty table."""
    user_id = id_user
    user = User.query.filter(User.user_id == user_id).one()
    ratings = Rating.query.filter(Rating.user_id == user_id).all()
    return render_template("user-detail.html", user=user, ratings=ratings)


@app.route('/login', methods=['GET'])
def loggin_page():
    """List of all users in a pretty pretty table.
        MAY BE MODAL WITH AJAX
    """
    return render_template("loggin.html")


@app.route('/login', methods=['POST'])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user_info = User.user_auth(email, password)
    user_id = user_info[0]
    user_email = user_info[1]

    if user_email != None:
        session['user_id'] = user_id
        return render_template("homepage.html", user_id=user_id, email=user_email)
    else:
        return render_template("register.html", user_id=user_id)   

@app.route('/logout')
def logout_page():
    """List of all users in a pretty pretty table.
        MAY BE MODAL WITH AJAX
    """
    del session['user_id']
    return render_template("homepage.html")


@app.route('/registration')
def register_page():
    """Register new users in the database.
        check that email is not already in database
        and either add to database or ask to loggin if email exists.
    """

    return render_template("register.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()