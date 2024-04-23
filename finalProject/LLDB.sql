CREATE DATABASE LLDB;
USE LLDB;

CREATE TABLE Customers (
    Customer_ID VARCHAR(255) PRIMARY KEY,
    Customer_Name VARCHAR(255),
    City VARCHAR(255),
    Country VARCHAR(255),
    Postal_Code VARCHAR(255),
    Country_Code VARCHAR(2)
);

CREATE TABLE Orders (
    Order_ID VARCHAR(255) PRIMARY KEY,
    Customer_ID VARCHAR(255),
    Order_Date DATE,
    Delivery_Date DATE,
    Sales DECIMAL(10, 3),
    Quantity INT,
    Discount DECIMAL(10, 2),
    Delivery_Cost DECIMAL(10, 2),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID)
);

CREATE TABLE Products (
    Product_ID INT AUTO_INCREMENT PRIMARY KEY,
    Course_Name VARCHAR(255),
    Cuisine_Name VARCHAR(255),
    Starter_Name VARCHAR(255),
    Desert_Name VARCHAR(255),
    Drink VARCHAR(255),
    Sides VARCHAR(255)
);

CREATE TABLE Orders_Products (
    Order_ID VARCHAR(255),
    Product_ID INT,
    Quantity INT,
    Cost DECIMAL(10, 2),
    FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID),
    FOREIGN KEY (Product_ID) REFERENCES Products(Product_ID),
    PRIMARY KEY (Order_ID, Product_ID)
);
