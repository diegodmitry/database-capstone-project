DELIMITER $$

CREATE PROCEDURE UpdateBooking(
    IN update_booking_id SMALLINT,
    IN update_date DATE
)
BEGIN
    -- Update the booking date in the bookings table based on the booking ID
    UPDATE bookings
    SET date = update_date
    WHERE booking_id = update_booking_id;
END$$

DELIMITER ;
