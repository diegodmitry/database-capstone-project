DELIMITER $$

CREATE PROCEDURE GetMaxQuantity()
BEGIN
    -- Selecting the maximum quantity from the Orders table
    SELECT MAX(Quantity) AS MaxQuantity FROM Orders;
END$$

DELIMITER ;

CALL GetMaxQuantity();