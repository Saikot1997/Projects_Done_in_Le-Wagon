# pylint: disable=missing-docstring, C0103


# => list (rows) of tuples (columns)

def directors_count(db):
    # return the number of directors contained in the database
    query = """SELECT COUNT(d.id)
    FROM directors AS d"""
    db.execute(query)
    count = db.fetchall()
    return count[0][0]


def directors_list(db):
    # return the list of all the directors sorted in alphabetical order
    query = """SELECT "d".name
    FROM directors AS d
    ORDER BY name ASC;"""
    db.execute(query)
    d_list = db.fetchall()
    return [d[0] for d in d_list]

def love_movies(db):
    # return the list of all movies which contain the exact word "love"
    # in their title, sorted in alphabetical order
    db.execute("""SELECT movie.title
               FROM movies AS movie
               WHERE title LIKE "love"
               OR title LIKE "% love"
               OR title LIKE "love %"
               OR title LIKE "% love %"
               OR title LIKE "love, %"
               OR title LIKE "% love'%"
               OR title LIKE "%'love %"
               OR title LIKE "% love."
               ORDER BY title ASC;""")
    love = db.fetchall()
    return [movie[0] for movie in love]

def directors_named_like_count(db, name):
    # return the number of directors which contain a given word in their name
    query =f"""SELECT COUNT(*)
        FROM directors AS d WHERE name LIKE "%{name}%" """
    db.execute(query)
    Dname = db.fetchall()
    return Dname[0][0]

def movies_longer_than(db, min_length):
    # return this list of all movies which are longer than a given duration,
    # sorted in the alphabetical order
    query = f"""SELECT d.title
    FROM movies AS d
    WHERE minutes > {min_length}
    ORDER BY title"""
    db.execute(query)
    longdur = db.fetchall()
    return [long[0] for long in longdur]
