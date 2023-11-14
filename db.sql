USE HotelManagementSystem;

CREATE TABLE Admin_Login (
    Username VARCHAR(15) NOT NULL PRIMARY KEY,
    Password TEXT NOT NULL
);

CREATE TABLE Customer (
    CNIC VARCHAR(15) NOT NULL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    PhoneNumber VARCHAR(13),
    Email TEXT,
    Address TEXT,
    DOB DATE,
    Password TEXT NOT NULL
);

CREATE TABLE Hotel (
    Branch_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Location TEXT,
    PhoneNumber VARCHAR(13)
);

CREATE TABLE RoomType (
    RoomType_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    NumberOfBeds INT,
    Type TEXT,
    Price INT,
    Image TEXT
);

CREATE TABLE Room (
    Room_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    RoomType_ID INT NOT NULL,
    RoomNumber INT NOT NULL,
    Branch_ID INT NOT NULL,
    isBooked VARCHAR(5) NOT NULL DEFAULT 'False',
    FOREIGN KEY (Branch_ID) REFERENCES Hotel(Branch_ID) ON DELETE CASCADE,
    FOREIGN KEY (RoomType_ID) REFERENCES RoomType(RoomType_ID) ON DELETE CASCADE
);


CREATE TABLE Billing (
    Billing_ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    User_ID VARCHAR(15),
    Status TEXT
);

CREATE TABLE Booking (
    Room_ID INT,
    Billing_ID INT,
    CurrentDate DATE,
    NumberOfDays INT,
    isBooked TEXT DEFAULT 'False',
    FOREIGN KEY (Room_ID) REFERENCES Room(Room_ID) ON DELETE SET NULL ON UPDATE SET NULL,
    FOREIGN KEY (Billing_ID) REFERENCES Billing(Billing_ID)
);

-- Triggers/Functions/Procedures/Views

-- Default Page Function (additional function) - MARYAM
DELIMITER //

CREATE PROCEDURE CheckAvailability(loc TEXT, Type TEXT, noofbeds INT)
BEGIN
     CREATE TEMPORARY TABLE temp_available AS
    SELECT Room.RoomType_ID
    FROM RoomType
    JOIN Room ON Room.RoomType_ID = RoomType.RoomType_ID
    WHERE NumberOfBeds = noofbeds AND Type = Type
    AND Room.Branch_ID IN (SELECT Branch_ID FROM Hotel WHERE Location = loc)
    AND isBooked = 'False';
    
     -- Select the data from the temporary table
    SELECT * FROM temp_available;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS temp_available;

END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE catalog(loc TEXT)
BEGIN
    -- Create a temporary table to store the results
    CREATE TEMPORARY TABLE temp_catalog AS
    SELECT DISTINCT (Room.RoomType_ID), NumberOfBeds, Type, Price, Image
    FROM Room
    JOIN RoomType ON Room.RoomType_ID = RoomType.RoomType_ID
    WHERE Branch_ID IN (SELECT Hotel.Branch_ID FROM Hotel WHERE Location = loc)
    AND Room.isBooked = 'False';

    -- Select the data from the temporary table
    SELECT * FROM temp_catalog;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS temp_catalog;
END //
DELIMITER ;


DELIMITER //


DELIMITER //


DELIMITER //

CREATE PROCEDURE BookRoom(
  IN userid VARCHAR(255),
  IN roomtypeid INT,
  IN loc VARCHAR(255),
  IN days INT
)
BEGIN
  DECLARE billingid INT;
  DECLARE roomid INT;

  IF EXISTS (SELECT * FROM Billing WHERE User_ID = userid AND Status = 'Not Paid') THEN
    -- User has an existing unpaid billing record
    SELECT Billing_ID INTO billingid FROM Billing WHERE User_ID = userid AND Status = 'Not Paid';

    -- Find an available room
    SELECT Room_ID INTO roomid
    FROM (
      SELECT Room_ID
      FROM Room
      WHERE RoomType_ID = roomtypeid
        AND Branch_ID IN (SELECT Branch_ID FROM Hotel WHERE Location LIKE loc)
        AND isBooked = 'False'
      LIMIT 1
    ) AS temptable;

    -- Update room status to booked
    UPDATE Room SET isBooked = 'True' WHERE Room_ID = roomid;

    -- Insert booking record
    INSERT INTO Booking (Room_ID, Billing_ID, CurrentDate, NumberOfDays, isBooked)
    VALUES (roomid, billingid, CURDATE(), days, 'True');
  ELSE
   
    -- Create a new billing record
    INSERT INTO Billing (User_ID, Status)
    VALUES (userid, 'Not Paid');

    -- Get the new billing ID
    SET billingid = LAST_INSERT_ID();

    -- Find an available room
    SELECT Room_ID INTO roomid
    FROM (
      SELECT Room_ID
      FROM Room
      WHERE RoomType_ID = roomtypeid
        AND Branch_ID IN (SELECT Branch_ID FROM Hotel WHERE Location LIKE loc)
        AND isBooked = 'False'
      LIMIT 1
    ) AS temptable;

    -- Update room status to booked
    UPDATE Room SET isBooked = 'True' WHERE Room_ID = roomid;

    -- Insert booking record
    INSERT INTO Booking (Room_ID, Billing_ID, CurrentDate, NumberOfDays, isBooked)
    VALUES (roomid, billingid, CURDATE(), days, 'True');
  END IF;
END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE BookedRoom(IN userid VARCHAR(255))
BEGIN
    SELECT
        Hotel.Location,
        Room.RoomNumber,
        RoomType.NumberOfBeds,
        RoomType.Type,
        Booking.NumberOfDays,
        RoomType.Price,
        Booking.Room_ID,
        Booking.isBooked
    FROM
        Booking
    JOIN
        Room ON Booking.Room_ID = Room.Room_ID
    JOIN
        RoomType ON RoomType.RoomType_ID = Room.RoomType_ID
    JOIN
        Hotel ON Hotel.Branch_ID = Room.Branch_ID
    WHERE
        Billing_ID IN (
            SELECT Billing_ID
            FROM Billing
            WHERE User_ID = userid AND Status = 'Not Paid'
        );
END;
//

DELIMITER ;





-- DELIMITER //

-- --this has error will checkafter mids
-- CREATE FUNCTION TotalBill(userid VARCHAR(255))
-- RETURNS INT
-- BEGIN
--   DECLARE total INT DEFAULT 0;
--   DECLARE history INT;
--   DECLARE offer_discount DECIMAL(10, 2);

--   SELECT SUM(NumberOfDays * Price)
--   INTO total
--   FROM BookedRoom
--   WHERE UserID = userid;

--   RETURN total;
-- END //

DELIMITER ;

DELIMITER //
CREATE PROCEDURE checkoutRoom(roomid INT, userid VARCHAR(255))
BEGIN
    UPDATE Room
    SET isBooked = 'False'
    WHERE Room_ID = roomid;
    
    UPDATE Booking
    SET isBooked = 'False'
    WHERE Room_ID = roomid
    AND Billing_ID IN (
        SELECT Billing_ID
        FROM Billing
        WHERE User_ID = userid
    );
END//

DELIMITER ;

DELIMITER //
-- Procedure: Checkout
CREATE PROCEDURE Checkout(userid VARCHAR(255))
BEGIN
  UPDATE Booking SET isBooked = 'False'
  WHERE Billing_ID IN (
    SELECT Billing_ID
    FROM Billing
    WHERE User_ID = user_id
  ); 

UPDATE Booking SET isBooked='False' 
WHERE Billing_ID IN(
  SELECT Billing_ID 
  FROM Billing 
  WHERE User_ID=userid
  );
END //
DELIMITER ;


-- View: ShowRooms
CREATE VIEW ShowRooms AS
SELECT
  Room.Room_ID,
  Room.RoomNumber,
  Hotel.Location,
  Room.RoomType_ID,
  RoomType.Type,
  RoomType.NumberOfBeds,
  RoomType.Price
FROM
  Room
JOIN RoomType ON RoomType.RoomType_ID = Room.RoomType_ID
JOIN Hotel ON Hotel.Branch_ID = Room.Branch_ID;

-- View: Payments
CREATE VIEW Payments AS
SELECT *
FROM Billing
WHERE Status = 'Not Paid';


DELIMITER //

CREATE PROCEDURE Paid(IN Billing_id INT)
BEGIN
  SET @id = (SELECT User_ID FROM Billing WHERE Billing_ID = Billing_id LIMIT 1);

  SET @totalAmount = 0;

  -- Calculate the total amount using the TotalBill function
  SET @totalAmount = TotalBill(@id);

  -- Call the Checkout procedure
  CALL Checkout(@id);

  -- Mark the Billing as Paid
  UPDATE Billing
  SET Status = 'Paid'
  WHERE Billing_ID = Billing_id;
END//

DELIMITER ;

DELIMITER //

-- View: CurrentBookings
CREATE VIEW CurrentBookings AS
SELECT
  User_ID AS CNIC,
  RoomNumber,
  Location,
  NumberOfDays,
  CurrentDate AS CheckInDate,
  Room.Room_ID
FROM
  Booking
JOIN Room ON Booking.Room_ID = Room.Room_ID
JOIN Billing ON Billing.Billing_ID = Booking.Billing_ID
JOIN Hotel ON Hotel.Branch_ID = Room.Branch_ID
WHERE
  Room.isBooked = 'True';

-- View: CustomerInfo
CREATE VIEW CustomerInfo AS
SELECT
  CNIC,
  FirstName,
  LastName,
  Address,
  PhoneNumber,
  Email,
  DOB,
FROM
  Customer;

DELIMITER ;

-- Create a procedure to retrieve booking information
DELIMITER //
CREATE PROCEDURE ViewBooking(id INT)
BEGIN
  SELECT
    Hotel.Location,
    Room.RoomNumber,
    RoomType.NumberOfBeds,
    RoomType.Type,
    Booking.NumberOfDays,
    RoomType.Price
  FROM Booking
  JOIN Room ON Booking.Room_ID = Room.Room_ID
  JOIN RoomType ON RoomType.RoomType_ID = Room.RoomType_ID
  JOIN Hotel ON Hotel.Branch_ID = Room.Branch_ID
  WHERE Billing_ID = id;
END;
//
DELIMITER ;



DELIMITER //

CREATE FUNCTION TotalBillById(userid VARCHAR(255)) RETURNS INT
BEGIN
  DECLARE total INT;
  SET total = 0;

  SELECT SUM(NumberOfDays * Price) INTO total FROM ViewBooking WHERE UserID = userid;

  RETURN total;
END //

DELIMITER ;


-- Procedure isBillPresent
DELIMITER //
CREATE PROCEDURE isBillPresent (
  IN id INT,
  OUT flag INT
)
BEGIN
  IF EXISTS (SELECT * FROM Booking WHERE Billing_ID = id AND Room_ID IS NULL) THEN
    SET flag = 1;
  ELSE
    SET flag = 0;
  END IF;
END//
DELIMITER ;

-- Additional Feature: AutomaticCheckOut
DELIMITER //
CREATE PROCEDURE AutomaticCheckOut ()
BEGIN
  UPDATE Room
  SET isBooked = 'False'
  WHERE Room_ID IN (SELECT Booking.Room_ID FROM Booking WHERE DATEDIFF(CURDATE(), Booking.CurrentDate) >= Booking.NumberOfDays);

  UPDATE Booking
  SET isBooked = 'False'
  WHERE Booking.Room_ID IN (SELECT Booking.Room_ID FROM Booking WHERE DATEDIFF(CURDATE(), Booking.CurrentDate) >= Booking.NumberOfDays);
END//
DELIMITER ;

-- Delete triggers


DELIMITER //

CREATE TRIGGER BeforeDeleteRoomType
BEFORE DELETE ON RoomType
FOR EACH ROW
BEGIN
  DECLARE id INT;
  SET id = OLD.RoomType_ID;

  IF EXISTS (SELECT * FROM Billing WHERE Billing_ID IN (SELECT Billing_ID FROM Booking WHERE Room_ID IN (SELECT Room_ID FROM Room WHERE RoomType_ID = id)) AND Status = 'Not Paid') THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Not Deleted';
  END IF;
END;

DELIMITER ;


DELIMITER //

CREATE TRIGGER BeforeDeleteBranch
BEFORE DELETE ON Hotel
FOR EACH ROW
BEGIN
  DECLARE id INT;
  SET id = OLD.Branch_ID;

  IF EXISTS (SELECT * FROM Billing WHERE Billing_ID IN (SELECT Billing_ID FROM Booking WHERE Room_ID IN (SELECT Room_ID FROM Room WHERE Branch_ID = id)) AND Status = 'Not Paid') THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Not Deleted';
  END IF;
END;

DELIMITER ;


-- Admin Insert INTO Admin_Login values('admin','admin');
INSERT INTO Admin_Login (Username, Password) VALUES ('admin', 'admin');


-- Customer
INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password)
VALUES ('35202-8433941-2', 'Ali', 'Ahmed', '+923013561457', 'ailahmed533@gmail.com', '44B-Model Town Lahore', '1998-04-23', '12345678');

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password)
VALUES ('35202-1111111-1', 'Amna', 'Abid', '+923021111111', 'amnaabid@gmail.com', '3A-Garden Town Lahore', '1995-06-07', '11111111');

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password)
VALUES ('35202-2222222-0', 'Faris', 'Ali', '+923032222222', 'farisali@gmail.com', '58F-Johar Town Lahore', '1990-01-09', '22222222');

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password)
VALUES ('35202-3333333-2', 'Kamil', 'Jamil', '+923043333333', 'kamiljamil@gmail.com', '48-F-2 Islamabad', '2000-09-04', '33333333');

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password)
VALUES ('35202-4444444-1', 'Sara', 'Nasir', '+923054444444', 'saranasir@gmail.com', '7B-Pak Sectt. Islamabad', '1991-01-01', '44444444');

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password)
VALUES ('35202-5555555-0', 'Saba', 'Khan', '+923065555555', 'sabakhan@gmail.com', '9A-Clifton Karachi', '1995-12-01', '55555555');

-- Branch
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Lahore', '+923013561457'); -- 1
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Karachi', '+923556153911'); -- 2
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Islamabad', '+923644325788'); -- 3
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Peshawar', '+923358460852'); -- 4
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Quetta', '+923550294607'); -- 5

-- Room Type
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (1, 'Deluxe', 1000, 'd1.jpeg'); -- 1
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (2, 'Deluxe', 1200, 'd2.jpeg'); -- 2
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (2, 'Deluxe', 1300, 'd21.jpeg'); -- 3
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (3, 'Deluxe', 1400, 'd3.jpeg'); -- 4
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (4, 'Deluxe', 1600, 'd4.jpeg'); -- 5
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (1, 'Suite', 1500, 's1.jpeg'); -- 6
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (2, 'Suite', 1700, 's2.jpeg'); -- 7
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (2, 'Suite', 1800, 's21.jpeg'); -- 8
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (3, 'Suite', 1900, 's3.jpeg'); -- 9
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image) VALUES (4, 'Suite', 2100, 's4.jpeg'); -- 10

-- Rooms
-- Lahore
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (1, 1, 1); -- 1
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (1, 2, 1); -- 2
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (1, 222, 1); -- 3
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (2, 3, 1); -- 4
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (2, 4, 1); -- 5
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (3, 213, 1); -- 6
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (3, 5, 1); -- 7
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (4, 212, 1); -- 8
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (5, 334, 1); -- 9
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (6, 321, 1); -- 10
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (7, 264, 1); -- 11
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (8, 21, 1); -- 12
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (9, 23, 1); -- 13
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (10, 4, 1); -- 14

-- Karachi
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (1, 1, 2); -- 1
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (1, 2, 2); -- 2
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (1, 222, 2); -- 3
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (2, 12, 2); -- 4
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (3, 20, 2); -- 5
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (3, 233, 2); -- 6
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (3, 5, 2); -- 7
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (4, 212, 2); -- 8
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (7, 334, 2); -- 9
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (6, 321, 2); -- 10
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (7, 264, 2); -- 11
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (8, 21, 2); -- 12
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (9, 23, 2); -- 13
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (10, 4, 2); -- 14

-- Islamabad
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (1, 1, 3); -- 1
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (1, 1, 3); -- 2
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (9, 22, 3); -- 3
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (2, 12, 3); -- 4
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (3, 20, 3); -- 5
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (3, 233, 3); -- 6
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (3, 5, 3); -- 7
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (4, 212, 3); -- 8
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (7, 334, 3); -- 9
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (6, 321, 3); -- 10
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (5, 214, 3); -- 11
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (8, 21, 3); -- 12
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (9, 23, 3); -- 13
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (10, 4, 3); -- 14

-- Peshawar
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (7, 1, 4); -- 1
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (6, 1, 4); -- 2
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (3, 22, 4); -- 3
INSERT INTO Room (RoomType_ID, RoomNumber, Branch_ID) VALUES (8, 12, 4); -- 4

-- Bookings
CALL BookRoom('35202-1111111-1', 3, 'Islamabad', 4);
CALL BookRoom('35202-1111111-1', 8, 'Islamabad', 4);
CALL BookRoom('35202-4444444-1', 9, 'Islamabad', 1);
CALL BookRoom('35202-2222222-0', 3, 'Karachi', 3);
CALL BookRoom('35202-5555555-0', 7, 'Peshawar', 2);


-- Payments
-- CALL Paid(2);