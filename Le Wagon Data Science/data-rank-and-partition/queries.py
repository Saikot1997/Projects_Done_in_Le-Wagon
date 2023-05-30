# pylint:disable=C0111,C0103

def order_rank_per_customer(db):
    query = """SELECT OrderID, CustomerID, OrderDate,
    RANK() OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS OrderRank
    FROM Orders
    ORDER BY CustomerID, OrderDate"""
    db.execute(query)
    result = db.fetchall()
    return result


def order_cumulative_amount_per_customer(db):
    query = """SELECT O.OrderID, O.CustomerID, O.OrderDate,
    SUM(SUM(OD.UnitPrice * OD.Quantity)) OVER (PARTITION BY O.CustomerID ORDER BY O.OrderDate) AS OrderCumulativeAmount
    FROM Orders AS O
    JOIN OrderDetails AS OD ON O.OrderID = OD.OrderID
    GROUP BY O.OrderID;"""
    db.execute(query)
    result = db.fetchall()
    return result
