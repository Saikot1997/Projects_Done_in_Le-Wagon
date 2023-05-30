# pylint: disable=C0103, missing-docstring


def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    query = """SELECT m.title, m.genres, d.name
    FROM movies AS m
    JOIN directors AS d ON m.director_id = d.id"""
    db.execute(query)
    hlw = db.fetchall()
    return hlw


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query = """SELECT m.title
    FROM movies AS m
    JOIN directors AS d ON m.director_id = d.id
    WHERE m.start_year > d.death_year"""
    db.execute(query)
    hi = db.fetchall()
    return [g[0] for g in hi]


def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    query = f"""SELECT COUNT(*) AS num_movies, AVG(m.rating) AS avg_rating,
    MIN(m.minutes) AS min_duration, MAX(m.minutes) AS max_duration
    FROM movies AS m
    WHERE m.genres LIKE "%Action%"
    """
    db.execute(query)
    result = db.fetchall()
    stats = {
        'num_movies': result[0],
        'avg_rating': round(result[1], 2),
        'min_duration': result[2],
        'max_duration': result[3]
    }
    return stats

def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query = f"""SELECT d.name, COUNT(*) AS num_movies
    FROM movies AS m
    JOIN directors AS d ON m.director_id = d.id
    WHERE m.genres LIKE "{genre_name}"
    GROUP BY d.id
    ORDER BY num_movies DESC, d.name ASC
    LIMIT 5"""
    db.execute(query)
    hii = db.fetchall()
    return hii


def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    pass  # YOUR CODE HERE


def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    pass  # YOUR CODE HERE
