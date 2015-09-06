"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, url_for


from model import User, Rating, connect_to_db, db

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

@app.route('/beer-list')
def beers_list_page():
    """Movie List Page. Can Organize Movie info in a table that you can Organize by title or release date
        WILL NEED ROUTES FOR AJAX
    """
    beers = Movie.query.order_by(Movie.title).all()
    return render_template('beers-list.html', beers=beers)


@app.route('/beer-detail/<int:id_beer>', methods=["GET"])
def beer_detail_page(id_beer):
    """Individual Movie Info Page.


        1.Given a user U who has not rated beer M, find all other users who have rated that beer.
        2.For each other user O, find the beers they have rated in common with user U.
        3.Pair up the common beers, then feed each pair list into the Pearson function to find similarity S.
        4.Rank the users by their similarities, and find the user with the highest similarity, O.
        5.Multiply the similarity coefficient of user O with their rating for beer M. This is your predicted rating.
    """

    beer = Movie.query.filter(Movie.beer_id == id_beer).one()
    ratings = Rating.query.filter(Rating.beer_id == id_beer)

     #will return None if none   
    user_who_have_rated = ratings.filter(Rating.beer_id == id_beer).all()

    #Average Rating
    #Pearson Prediction
    #Insult

    # # ADD PEARSON CORRELATION
    # if session.get('user_id'):
    #     has_user_rated = Rating.query.filter(Rating.user_id == session['user_id']).all()
    #     if has_user_rated == None:




    return render_template("beer-detail.html", beer=beer, ratings=ratings)
    #will need to pass beer query information through jinja into template


#to add a rating to db
@app.route('/beer-detail/<int:id_beer>',methods=["POST"])
def beer_detail_page_score(id_beer):
    """Individual Movie Info Page."""
    beer = Movie.query.filter(Movie.beer_id == id_beer).one()
    
    score = request.form.get('score')
    user_id = session['user_id']
    beer_id = beer.beer_id

    score_to_add = Rating(user_id=user_id, beer_id=beer_id, score=score) 
    db.session.add(score_to_add)
    db.session.commit()    

    flash('You added a score!')
    # return redirect('/beer-detail/%s' % beer_id)
    return redirect(url_for('beer_detail_page', id_beer=beer_id))
    #will need to pass beer query information through jinja into template


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
    email_input = request.form.get("email")
    pword_input = request.form.get("password")

    user = User.query.filter(User.email == email_input).first()

    if user:
        if pword_input != user.password:
            flash("Your email and password did not match our records.")
            return redirect("/login")
        else:
            current_user = User.query.filter_by(email=email_input).first()
            current_user_dict = current_user.__dict__
            session['current_user_id'] = current_user_dict['user_id']
            print session['current_user_id']
            session['logged_in_customer_email'] = email_input
            return redirect("/profile")
        
    else:
        flash("Your email and password did not match our records.")
        return redirect("/login") 
         

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


    app.run()