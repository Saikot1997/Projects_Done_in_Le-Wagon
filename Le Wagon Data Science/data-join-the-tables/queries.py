# pylint:disable=C0111,C0103

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''
    query = """SELECT OrderID, ContactName,FirstName
    FROM Orders AS O
    JOIN Customers C ON C.CustomerID = O.CustomerID
    JOIN Employees E ON E.EmployeeID = O.EmployeeID
    ORDER BY OrderID"""

    db.execute(query)
    result = db.fetchall()
    return result

def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''
    query = """SELECT C.ContactName, SUM(OD.UnitPrice * OD.Quantity) AS TotalAmount
    FROM Orders AS O
    JOIN Customers C ON C.CustomerID = O.CustomerID
    JOIN OrderDetails OD ON OD.OrderID = O.OrderID
    GROUP BY O.CustomerID, C.ContactName
    ORDER BY TotalAmount;
    """
    db.execute(query)
    result = db.fetchall()
    return result

def best_employee(db):
    '''Implement the best_employee method to determine who’s the best employee!
    By “best employee”, we mean the one who sells the most.
    We expect the function to return a tuple like: ('FirstName', 'LastName',
    6000 (the sum of all purchase)). The order of the information is irrelevant'''
    query = """SELECT E.FirstName,E.LastName, SUM(OD.UnitPrice*OD.Quantity) AS TotalSum
    FROM Orders AS O
    JOIN Employees E ON E.EmployeeID = O.EmployeeID
    JOIN OrderDetails OD ON OD.OrderID = O.OrderID
    GROUP BY E.EmployeeID
    ORDER BY TotalSum DESC"""
    db.execute(query)
    result = db.fetchall()
    return result[0]


def orders_per_customer(db):
    '''Return a list of tuples where each tuple contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''
    query= """SELECT C.ContactName,COUNT(O.OrderID) AS NumOrders
    FROM Customers C
    LEFT JOIN Orders AS O ON O.CustomerID = C.CustomerID
    GROUP BY C.CustomerID
    ORDER BY NumOrders ASC"""
    db.execute(query)
    result = db.fetchall()
    return result
