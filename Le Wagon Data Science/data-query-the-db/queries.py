# pylint:disable=C0111,C0103

def query_orders(db):
    # return a list of orders displaying each column
    query = """SELECT *
    FROM Orders
    ORDER BY OrderID"""
    results = db.execute(query)
    result = results.fetchall()
    return result

def get_orders_range(db, date_from, date_to):
    # return a list of orders displaying all columns with OrderDate between
    # date_from and date_to (excluding date_from and including date_to)
    query = f"""SELECT *
    FROM Orders
    WHERE OrderDate > '{date_from}' AND OrderDate <= '{date_to}'"""
    results = db.execute(query)
    result = results.fetchall()
    return result

def get_waiting_time(db):
    # get a list with all the orders displaying each column
    # and calculate an extra TimeDelta column displaying the number of days
    # between OrderDate and ShippedDate, ordered by ascending TimeDelta
    query = """SELECT *,
    CAST(julianday(ShippedDate) - julianday(OrderDate) AS INTEGER)
    + 365 * (strftime('%Y', ShippedDate) - strftime('%Y', OrderDate))
    + CAST((julianday(strftime('%Y-', ShippedDate) || strftime('%m-', ShippedDate) || '01') - julianday(strftime('%Y-', OrderDate) || strftime('%m-', OrderDate) || '01')) / 30 AS INTEGER)
    AS TimeDelta
    FROM Orders
    ORDER BY TimeDelta
    """
    results = db.execute(query)
    result = results.fetchall()
    return result
