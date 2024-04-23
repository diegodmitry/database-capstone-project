import pandas as pd
import mysql.connector as connector

HOST = "localhost"
PORT = 3306
USER = "dbadmin"
PASSWORD = "dbadmin"
DATABASE = "LLDB"

# Establish a database connection
connection = connector.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

cursor = connection.cursor()

print('cursor', cursor)

def check_existence(table, column, value):
    """ Check if a specific value exists in a column of a table """
    query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {column} = %s)"
    cursor.execute(query, (value,))
    return cursor.fetchone()[0]

def get_order_id(order_id):
    query = "SELECT Order_ID FROM Orders WHERE Order_ID = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_product_id(course_name, cuisine_name, starter_name, desert_name, drink, sides):
    """Retrieve Product_ID based on detailed product attributes."""
    query = """
    SELECT Product_ID FROM Products
    WHERE Course_Name = %s AND Cuisine_Name = %s AND Starter_Name = %s 
    AND Desert_Name = %s AND Drink = %s AND Sides = %s
    """
    cursor.execute(query, (course_name, cuisine_name, starter_name, desert_name, drink, sides))
    result = cursor.fetchone()
    return result[0] if result else None


# Function to execute insert statements
def execute_insert(query, values):
    try:
        cursor.execute(query, values)
        connection.commit()
    except connector.Error as e:
        print("MySQL Error:", e)
        # connection.rollback()
    
try:
    file_path = './_LittleLemon_data.xlsx'

    # Read the Excel file
    data = pd.read_excel(file_path)

    # Customers table
    customers_data = data[['Customer ID', 'Customer Name', 'City', 'Country', 'Postal Code', 'Country Code']].drop_duplicates()
    print("customers_data:", customers_data)
    row_customer_count = 0
    for _, row in customers_data.iterrows():
        if row_customer_count < 200:
            insert_query = (
                "INSERT INTO Customers (Customer_ID, Customer_Name, City, Country, Postal_Code, Country_Code) VALUES (%s, %s, %s, %s, %s, %s)"
            )
            # print("row:", row)
            execute_insert(insert_query, tuple(row))
            row_customer_count += 1
        else:
            break
        
    # Orders table
    orders_data = data[['Order ID', 'Customer ID', 'Order Date', 'Delivery Date', 'Sales', 'Quantity', 'Discount', 'Delivery Cost']]
    row_order_count = 0
    for _, row in orders_data.iterrows():
        if row_order_count < 200:
            insert_query = (
                "INSERT INTO Orders (Order_ID, Customer_ID, Order_Date, Delivery_Date, Sales, Quantity, Discount, Delivery_Cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )
            execute_insert(insert_query, tuple(row))
            row_order_count += 1
        else:
            break
        
    # Products table - Assumes Product_ID is auto-incremented
    products_data = data[['Course Name', 'Cuisine Name', 'Starter Name', 'Desert Name', 'Drink', 'Sides']].drop_duplicates()
    row_product_data = 0
    for _, row in products_data.iterrows():
        if row_product_data < 200:
            insert_query = (
                "INSERT INTO Products (Course_Name, Cuisine_Name, Starter_Name, Desert_Name, Drink, Sides) VALUES (%s, %s, %s, %s, %s, %s)"
            )
            execute_insert(insert_query, tuple(row))
            row_product_data += 1
        else:
            break
        
    # Orders_Products table - Requires retrieving the Product_ID assuming 'Course Name' can be used as a unique identifier
    row_ordersProducts_data = 0
    for _, row in data.iterrows():
        if row_ordersProducts_data < 200:
            order_id = get_order_id(row['Order ID'])

            product_id = get_product_id(row['Course Name'], row['Cuisine Name'], row['Starter Name'], row['Desert Name'], row['Drink'],row['Sides'])

            if order_id and product_id:
                insert_query = """INSERT INTO Orders_Products (Order_ID, Product_ID, Quantity, Cost) VALUES (%s, %s, %s, %s)"""
                try:
                    cursor.execute(insert_query, (order_id, product_id, row['Quantity'], row[' Cost']))
                    connection.commit()
                    print("lines:", row_ordersProducts_data)
                    row_ordersProducts_data += 1
                    print(f"Inserted data for Order_ID: {order_id} and Product_ID: {product_id}")
                except connector.Error as error:
                    print(f"Failed to insert data: {error}")
                    connection.rollback()
            else:
                print(f"Order ID or Product ID not found for Order ID: {row['Order ID']}, Course Name: {row['Course Name']}")
        else:
            break

except Exception as e:
    print("An error occurred:", e)
    
finally:
    # Close the cursor and connection
    if cursor is not None:
        cursor.close()
    if connection.is_connected():
        connection.close()

print("Database population is complete.")