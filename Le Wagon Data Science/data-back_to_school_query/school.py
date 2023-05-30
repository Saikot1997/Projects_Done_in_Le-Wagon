# pylint:disable=C0111,C0103
#import sqlite3
#conn = sqlite3.connect('data/school.sqlite')
#db = conn.cursor()

def students_from_city(db, city):
    """return a list of students from a specific city"""
    query = f"""SELECT first_name|| ' ' ||last_name AS Student_Name
    FROM students
    WHERE birth_city = "{city}"
    """
    db.execute(query)
    name = db.fetchall()
    return [name[0] for name in name]



# To test your code, you can **run it** before running `make`
#   => Uncomment the following lines + run:
#   $ python school.py
#print(students_from_city(db, 'Paris'))
