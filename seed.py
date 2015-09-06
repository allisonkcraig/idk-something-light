"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
from datetime import datetime

def load_users():
    """Load users from u.user into database."""
    with open('seed_data/u.user', 'r') as user_data:
        for line in user_data:
            line.rstrip()
            row = line.split('|')
            age = row[1]
            email = None
            password = None
            zipcode = row[4]
            user_inserted = User(email=email, password=password, age=age, zipcode=zipcode)
            db.session.add(user_inserted)
        db.session.commit()

        

def load_movies():
    """Load movies from u.item into database."""
    with open('seed_data/u.item', 'r') as movie_data:
        for line in movie_data:
            line.rstrip()
            row = line.split('|')
            if row[1] == 'unknown':
                continue
            else:
                title = row[1][:-7]
                date_string = row[2]
                released_at = datetime.strptime(date_string, '%d-%b-%Y') # 01-Jan-1995 needs to be parsed and created as a datetime
                imdb_url = row[4]
                movie_inserted = Movie(title=title, released_at=released_at, imdb_url=imdb_url)
                db.session.add(movie_inserted)
        db.session.commit()

           

def load_ratings():
    """Load ratings from u.data into database."""
    with open('seed_data/u.data', 'r') as rating_data:
        for line in rating_data:
            line.rstrip()
            row = line.split('\t')
            user_id = row[0]
            movie_id = row[1]
            score = row[2]
            rating_inserted = Rating(user_id=user_id, movie_id=movie_id, score=score) 
            db.session.add(rating_inserted)
        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # load_users()
    load_movies()
    # load_ratings()
