DELIMITER $$

CREATE PROCEDURE CancelBooking(
    IN cancel_booking_id SMALLINT
)
BEGIN
    -- Deleting a booking from the bookings table based on the booking ID
    DELETE FROM bookings
    WHERE booking_id = cancel_booking_id;
END$$

DELIMITER ;
