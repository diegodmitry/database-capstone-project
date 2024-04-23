DELIMITER $$

CREATE PROCEDURE AddBooking(
    IN new_booking_id SMALLINT,
    IN new_date DATE,
    IN new_table_number INT,
    IN new_staff_id SMALLINT,
    IN new_customer_id SMALLINT
)
BEGIN
    -- Inserting a new record into the bookings table
    INSERT INTO bookings (booking_id, date, table_number, staff_information_staff_id, customers_idcustomer)
    VALUES (new_booking_id, new_date, new_table_number, new_staff_id, new_customer_id);
END$$

DELIMITER ;

