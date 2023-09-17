USE HotelManagementSystem;

CREATE TABLE SecurityQuestions (
    Question_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Text TEXT NOT NULL
);

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
    Password TEXT NOT NULL,
    PaymentHistory FLOAT DEFAULT 0,
    SecurityQuestion1 INT,
    Answer1 TEXT,
    SecurityQuestion2 INT,
    Answer2 TEXT,
    FOREIGN KEY (SecurityQuestion1) REFERENCES SecurityQuestions(Question_ID),
    FOREIGN KEY (SecurityQuestion2) REFERENCES SecurityQuestions(Question_ID)
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
    Image TEXT,
    Rating FLOAT DEFAULT 0,
    NoOfUsersRated INT DEFAULT 0
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

CREATE TABLE Menu (
    Food_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name TEXT,
    Cuisine TEXT,
    Description TEXT,
    Price INT,
    Image TEXT
);

CREATE TABLE SalesAndOffers (
    Offer_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Occasion TEXT,
    Percentage FLOAT,
    Image TEXT
);

CREATE TABLE Billing (
    Billing_ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    User_ID VARCHAR(15),
    Status TEXT,
    History INT DEFAULT 0
);

CREATE TABLE Booking (
    Room_ID INT,
    Billing_ID INT,
    CurrentDate DATE,
    NumberOfDays INT,
    HasRated TEXT DEFAULT 'False',
    isBooked TEXT DEFAULT 'False',
    FOREIGN KEY (Room_ID) REFERENCES Room(Room_ID) ON DELETE SET NULL ON UPDATE SET NULL,
    FOREIGN KEY (Billing_ID) REFERENCES Billing(Billing_ID)
);

CREATE TABLE Orders (
    Food_ID INT,
    Billing_ID INT,
    Quantity INT
);

CREATE TABLE SelectedOffers (
    Offer_ID INT,
    Billing_ID INT
);

-- Triggers/Functions/Procedures/Views

-- Default Page Function (additional function) - MARYAM
DELIMITER //

CREATE FUNCTION CheckAvailability(loc TEXT, Type TEXT, noofbeds INT)
RETURNS INT
BEGIN
    DECLARE RoomType_ID INT;

    SELECT Room.RoomType_ID INTO RoomType_ID
    FROM RoomType
    JOIN Room ON Room.RoomType_ID = RoomType.RoomType_ID
    WHERE NumberOfBeds = noofbeds AND Type = Type
    AND Room.Branch_ID IN (SELECT Branch_ID FROM Hotel WHERE Location = loc)
    AND isBooked = 'False'
    LIMIT 1;

    RETURN RoomType_ID;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE catalog(loc TEXT)
BEGIN
    -- Create a temporary table to store the results
    CREATE TEMPORARY TABLE temp_catalog AS
    SELECT DISTINCT Room.RoomType_ID, NumberOfBeds, Type, Price, Rating, Image
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

CREATE PROCEDURE ViewOffers(IN userid VARCHAR(15), OUT flag INT)
BEGIN
    DECLARE EXIT HANDLER FOR NOT FOUND SET flag = 0; -- Handle case when no rows are found
    
    IF EXISTS(SELECT * FROM Billing WHERE User_ID = userid AND Status = 'Not Paid') THEN
        SET flag = 1; -- bill exists
    ELSE
        SET flag = 0; -- bill does not exist
    END IF;
END//

DELIMITER //

DELIMITER //

-- Create a procedure to retrieve user offers
CREATE PROCEDURE UserOffers(IN userid VARCHAR(255))
BEGIN
  SELECT * FROM SalesAndOffers
  WHERE NOT EXISTS (
    SELECT Offer_ID
    FROM SelectedOffers
    WHERE Billing_ID IN (
      SELECT Billing_ID
      FROM Billing
      WHERE User_ID = userid
      AND Status = 'Not Paid'
    )
  );
END//
DELIMITER ;


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
  DECLARE history INT;

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
    INSERT INTO Booking (Room_ID, Billing_ID, CurrentDate, NumberOfDays, HasRated, isBooked)
    VALUES (roomid, billingid, CURDATE(), days, 'False', 'True');
  ELSE
    -- User does not have an existing unpaid billing record
    SELECT PaymentHistory INTO history FROM Customer WHERE CNIC = userid;

    -- Create a new billing record
    INSERT INTO Billing (User_ID, Status, History)
    VALUES (userid, 'Not Paid', history);

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
    INSERT INTO Booking (Room_ID, Billing_ID, CurrentDate, NumberOfDays, HasRated, isBooked)
    VALUES (roomid, billingid, CURDATE(), days, 'False', 'True');
  END IF;
END //

DELIMITER ;



DELIMITER //
CREATE PROCEDURE PlaceOrder (
  IN userid VARCHAR(255),
  IN foodid INT,
  IN quantity INT
)
BEGIN
  DECLARE billingid INT;
  DECLARE history INT; -- Declare history before the IF statement

  IF EXISTS (SELECT * FROM Billing WHERE User_ID = userid AND Status = 'Not Paid') THEN
    SELECT Billing_ID INTO billingid FROM Billing WHERE User_ID = userid AND Status = 'Not Paid';
  ELSE
    SELECT PaymentHistory INTO history FROM Customer WHERE CNIC = userid;

    INSERT INTO Billing (User_ID, Status, History) VALUES (userid, 'Not Paid', history);
    SET billingid = LAST_INSERT_ID(); -- Use SET to assign the value
  END IF;

  INSERT INTO Orders (Food_ID, Billing_ID, Quantity) VALUES (foodid, billingid, quantity);
END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE SelectOffer (
  IN userid VARCHAR(255),
  IN offerid INT
)
BEGIN
  DECLARE billingid INT;

  IF EXISTS (SELECT * FROM Billing WHERE User_ID = userid AND Status = 'Not Paid') THEN
    SELECT Billing_ID INTO billingid FROM Billing WHERE User_ID = userid AND Status = 'Not Paid';
    INSERT INTO SelectedOffers (Offer_ID, Billing_ID) VALUES (offerid, billingid);
  END IF;
END//
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
        Booking.HasRated,
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


DELIMITER //

CREATE PROCEDURE OrdersPlaced(IN userid VARCHAR(255), OUT Name VARCHAR(255), OUT Quantity INT, OUT Price DECIMAL(10, 2))
BEGIN
    SELECT Menu.Name, Orders.Quantity, Menu.Price
    INTO Name, Quantity, Price
    FROM Orders
    JOIN Menu ON Orders.Food_ID = Menu.Food_ID
    WHERE Billing_ID IN (
        SELECT Billing_ID
        FROM Billing
        WHERE User_ID = userid AND Status = 'Not Paid'
    );
END;
//

DELIMITER ;



DELIMITER //

CREATE PROCEDURE OfferSelected(IN userid VARCHAR(255))
BEGIN
    CREATE TEMPORARY TABLE IF NOT EXISTS tmpOfferSelected (
        Occasion VARCHAR(255),
        Percentage DECIMAL(10, 2)
    );

    INSERT INTO tmpOfferSelected (Occasion, Percentage)
    SELECT SalesAndOffers.Occasion, SalesAndOffers.Percentage
    FROM SelectedOffers
    JOIN SalesAndOffers ON SalesAndOffers.Offer_ID = SelectedOffers.Offer_ID
    WHERE Billing_ID IN (
        SELECT Billing_ID
        FROM Billing
        WHERE User_ID = userid AND Status = 'Not Paid'
    );

    -- Now you can use SELECT to retrieve data from tmpOfferSelected
    SELECT Occasion, Percentage FROM tmpOfferSelected;

    -- Optionally, you can drop the temporary table when done
    DROP TEMPORARY TABLE IF EXISTS tmpOfferSelected;
END;
//
DELIMITER ;


DELIMITER //

CREATE FUNCTION TotalBill(userid VARCHAR(255))
RETURNS INT
BEGIN
  DECLARE total INT DEFAULT 0;
  DECLARE history INT;
  DECLARE offer_discount DECIMAL(10, 2);

  SELECT SUM(NumberOfDays * Price)
  INTO total
  FROM BookedRoom
  WHERE UserID = userid;

  SELECT SUM(Quantity * Price)
  INTO total
  FROM OrdersPlaced
  WHERE UserID = userid;

  SELECT PaymentHistory INTO history
  FROM Customer
  WHERE CNIC = userid;

  IF total IS NOT NULL THEN
    -- Apply OfferSelected logic if applicable
    SELECT Percentage / 100 INTO offer_discount
    FROM OfferSelected
    WHERE UserID = userid;
    
    IF offer_discount IS NOT NULL THEN
      SET total = total - (offer_discount * total);
    END IF;
    
    -- Apply payment history discounts
    IF history > 10000 AND history <= 20000 THEN
      SET total = total - (total * 0.05);
    ELSEIF history > 20000 AND history <= 30000 THEN
      SET total = total - (total * 0.1);
    ELSEIF history > 30000 THEN
      SET total = total - (total * 0.15);
    END IF;
  END IF;

  RETURN total;
END //

DELIMITER ;


-- Procedure: checkoutRoom
CREATE PROCEDURE checkoutRoom(roomid INT, userid VARCHAR(255))
  UPDATE Room SET isBooked = 'False'
  WHERE Room_ID = roomid;

DELIMITER //
-- Procedure: Checkout
CREATE PROCEDURE Checkout(userid VARCHAR(255))
BEGIN
  DECLARE user_id_param VARCHAR(255);
  SET user_id_param = userid;

  UPDATE Booking SET isBooked = 'False'
  WHERE Billing_ID IN (
    SELECT Billing_ID
    FROM Billing
    WHERE User_ID = user_id_param
  );
END //
DELIMITER ;

DELIMITER //

-- Procedure: RatingTable
CREATE PROCEDURE RatingTable(userid VARCHAR(255))
BEGIN
  CREATE TEMPORARY TABLE IF NOT EXISTS result_table (
    Location VARCHAR(255),
    RoomNumber INT
  );

  INSERT INTO result_table
  SELECT BookedRoom.Location, BookedRoom.RoomNumber
  FROM BookedRoom
  JOIN Room ON Room.RoomNumber = BookedRoom.RoomNumber
  WHERE Room.Branch_ID IN (
    SELECT DISTINCT Branch_ID
    FROM Hotel
    WHERE Location = BookedRoom.Location
  )
  AND BookedRoom.HasRated = 'False'
  GROUP BY BookedRoom.Location, BookedRoom.RoomNumber;
END //

DELIMITER ;


-- Procedure: RateRoom
DELIMITER //
CREATE PROCEDURE RateRoom(loc VARCHAR(255), roomno INT, rating FLOAT, userid VARCHAR(255))
BEGIN
  SET @roomtypeid = NULL;
  SET @rate = NULL;
  SET @billingid = NULL;

  -- Find the RoomType_ID based on location and room number
  SELECT Room.RoomType_ID INTO @roomtypeid
  FROM Room
  WHERE Room.RoomNumber = roomno
    AND Room.Branch_ID IN (
      SELECT Branch_ID
      FROM Hotel
      WHERE Location = loc
    );

  -- Calculate the new rating for the room type
  SELECT (NoOfUsersRated * Rating + rating) / (NoOfUsersRated + 1) INTO @rate
  FROM RoomType
  WHERE RoomType_ID = @roomtypeid;

  -- Update the RoomType table with the new rating
  UPDATE RoomType SET Rating = @rate
  WHERE RoomType_ID = @roomtypeid;

  -- Increment the number of users rated for the room type
  UPDATE RoomType SET NoOfUsersRated = NoOfUsersRated + 1
  WHERE RoomType_ID = @roomtypeid;

  -- Find the Billing_ID for the user and room that needs to be rated
  SELECT Billing_ID INTO @billingid
  FROM Billing
  WHERE User_ID = userid
    AND Status = 'Not Paid';

  -- Update the Booking table to indicate that the user has rated the room
  UPDATE Booking SET HasRated = 'True'
  WHERE Room_ID IN (
    SELECT Room_ID
    FROM Room
    WHERE RoomNumber = roomno
      AND Branch_ID IN (
        SELECT Branch_ID
        FROM Hotel
        WHERE Location = loc
      )
  ) AND Billing_ID = @billingid;
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

  -- Update Billing History
  UPDATE Billing
  SET History = (SELECT MAX(PaymentHistory) FROM Customer WHERE CNIC = @id)
  WHERE Billing_ID = Billing_id;

  SET @totalAmount = 0;

  -- Calculate the total amount using the TotalBill function
  SET @totalAmount = TotalBill(@id);

  -- Update PaymentHistory for the user
  UPDATE Customer
  SET PaymentHistory = PaymentHistory + @totalAmount
  WHERE CNIC = @id;

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
  PaymentHistory
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


-- Procedure: ViewOrder
DELIMITER //
CREATE PROCEDURE ViewOrder(id INT)
BEGIN
  SELECT
    Menu.Name,
    Orders.Quantity,
    Menu.Price
  FROM
    Orders
  JOIN Menu ON Orders.Food_ID = Menu.Food_ID
  WHERE
    Billing_ID = id;
END//
DELIMITER ;

-- Procedure: ViewOffer
DELIMITER //
CREATE PROCEDURE ViewOffer(id INT)
BEGIN
  SELECT
    SalesAndOffers.Occasion,
    SalesAndOffers.Percentage
  FROM
    SelectedOffers
  JOIN SalesAndOffers ON SalesAndOffers.Offer_ID = SelectedOffers.Offer_ID
  WHERE
    Billing_ID = id;
END//
DELIMITER ;

DELIMITER //

CREATE FUNCTION TotalBillById(userid VARCHAR(255)) RETURNS INT
BEGIN
  DECLARE total INT;
  DECLARE orderTotal INT;  -- Declare orderTotal here
  DECLARE history INT;

  SET total = 0;

  SELECT SUM(NumberOfDays * Price) INTO total FROM ViewBooking WHERE UserID = userid;

  IF total IS NOT NULL THEN
    SELECT SUM(Quantity * Price) INTO orderTotal FROM ViewOrder WHERE UserID = userid;
    SET total = total + orderTotal;
  END IF;

  SELECT (Percentage / 100) * total INTO total FROM ViewOffer WHERE UserID = userid;

  SELECT PaymentHistory INTO history FROM Customer WHERE CNIC = userid;

  IF history > 10000 AND history <= 20000 THEN
    SET total = total - (total * 0.05);
  ELSEIF history > 20000 AND history <= 30000 THEN
    SET total = total - (total * 0.1);
  ELSEIF history > 30000 THEN
    SET total = total - (total * 0.15);
  END IF;

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
  IF EXISTS (SELECT * FROM Orders WHERE Billing_ID = id AND Food_ID IS NULL) OR
     EXISTS (SELECT * FROM Booking WHERE Billing_ID = id AND Room_ID IS NULL) OR
     EXISTS (SELECT * FROM SelectedOffers WHERE Billing_ID = id AND Offer_ID IS NULL) THEN
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

CREATE TRIGGER BeforeDeleteFood
BEFORE DELETE ON Menu
FOR EACH ROW
BEGIN
  DECLARE food_id INT;
  SET food_id = OLD.Food_ID;

  IF EXISTS (SELECT * FROM Billing WHERE Billing_ID IN (SELECT Billing_ID FROM Orders WHERE Food_ID = food_id) AND Status = 'Not Paid') THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Not Deleted';
  END IF;
END;

DELIMITER ;


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


DELIMITER //

CREATE TRIGGER BeforeDeleteOffer
BEFORE DELETE ON SalesAndOffers
FOR EACH ROW
BEGIN
  DECLARE id INT;
  SET id = OLD.Offer_ID;

  IF EXISTS (SELECT * FROM Billing WHERE Billing_ID IN (SELECT Billing_ID FROM SelectedOffers WHERE Offer_ID = id) AND Status = 'Not Paid') THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Not Deleted';
  END IF;
END;

DELIMITER ;

-- Admin Insert INTO Admin_Login values('admin','admin');
INSERT INTO Admin_Login (Username, Password) VALUES ('admin', 'admin');

-- Security Questions
INSERT INTO SecurityQuestions (Text) VALUES ('What is your Favourite Color?');
INSERT INTO SecurityQuestions (Text) VALUES ('What is your NickName');
INSERT INTO SecurityQuestions (Text) VALUES ('What is your Dream Job?');
INSERT INTO SecurityQuestions (Text) VALUES ('What is your Favourite Movie?');

-- Customer
INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password, SecurityQuestion1, Answer1, SecurityQuestion2, Answer2, PaymentHistory)
VALUES ('35202-8433941-2', 'Ali', 'Ahmed', '+923013561457', 'ailahmed533@gmail.com', '44B-Model Town Lahore', '1998-04-23', '12345678', 1, 'Blue', 3, 'Doctor', 15320);

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password, SecurityQuestion1, Answer1, SecurityQuestion2, Answer2, PaymentHistory)
VALUES ('35202-1111111-1', 'Amna', 'Abid', '+923021111111', 'amnaabid@gmail.com', '3A-Garden Town Lahore', '1995-06-07', '11111111', 1, 'Red', 4, 'Brave', 1111);

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password, SecurityQuestion1, Answer1, SecurityQuestion2, Answer2, PaymentHistory)
VALUES ('35202-2222222-0', 'Faris', 'Ali', '+923032222222', 'farisali@gmail.com', '58F-Johar Town Lahore', '1990-01-09', '22222222', 2, 'Fari', 3, 'Teacher', 2222);

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password, SecurityQuestion1, Answer1, SecurityQuestion2, Answer2, PaymentHistory)
VALUES ('35202-3333333-2', 'Kamil', 'Jamil', '+923043333333', 'kamiljamil@gmail.com', '48-F-2 Islamabad', '2000-09-04', '33333333', 1, 'Green', 4, 'Ice Age', 3333);

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password, SecurityQuestion1, Answer1, SecurityQuestion2, Answer2, PaymentHistory)
VALUES ('35202-4444444-1', 'Sara', 'Nasir', '+923054444444', 'saranasir@gmail.com', '7B-Pak Sectt. Islamabad', '1991-01-01', '44444444', 2, 'Zara', 4, 'The Maze Runner', 4444);

INSERT INTO Customer (CNIC, FirstName, LastName, PhoneNumber, Email, Address, DOB, Password, SecurityQuestion1, Answer1, SecurityQuestion2, Answer2, PaymentHistory)
VALUES ('35202-5555555-0', 'Saba', 'Khan', '+923065555555', 'sabakhan@gmail.com', '9A-Clifton Karachi', '1995-12-01', '55555555', 1, 'Blue', 3, 'Engineer', 5555);

-- Branch
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Lahore', '+923013561457'); -- 1
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Karachi', '+923556153911'); -- 2
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Islamabad', '+923644325788'); -- 3
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Peshawar', '+923358460852'); -- 4
INSERT INTO Hotel (Location, PhoneNumber) VALUES ('Quetta', '+923550294607'); -- 5

-- Room Type
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (1, 'Deluxe', 1000, 'd1.jpeg', 7.5, 4); -- 1
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (2, 'Deluxe', 1200, 'd2.jpeg', 2.3, 12); -- 2
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (2, 'Deluxe', 1300, 'd21.jpeg', 4.1, 6); -- 3
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (3, 'Deluxe', 1400, 'd3.jpeg', 8.2, 7); -- 4
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (4, 'Deluxe', 1600, 'd4.jpeg', 6.3, 8); -- 5
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (1, 'Suite', 1500, 's1.jpeg', 4.5, 15); -- 6
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (2, 'Suite', 1700, 's2.jpeg', 2.4, 7); -- 7
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (2, 'Suite', 1800, 's21.jpeg', 9.1, 9); -- 8
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (3, 'Suite', 1900, 's3.jpeg', 10, 1); -- 9
INSERT INTO RoomType (NumberOfBeds, Type, Price, Image, Rating, NoOfUsersRated) VALUES (4, 'Suite', 2100, 's4.jpeg', 3.8, 20); -- 10

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

-- Menu
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Tacos', 'Mexican', 'An open wrap with a filling of meat, cheese, and lettuce as the star of the show', 500, 'tacos.jpeg');
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Pizza', 'Italian', 'The humble combination of sauce, cheese and bread is one that we all know of', 400, 'pizza.jpeg');
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Moussaka', 'Greek', 'A potato or eggplant based meat dish', 600, 'Moussaka.jpeg');
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Sushi', 'Japanese', 'Raw fish and vegetables wrapped in vinegared rice', 700, 'sushi.jpeg');
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Paella', 'Spanish', 'Slowly cooked rice, vegetables, seafood and spices, till it takes its flavorsome form', 700, 'Paella.jpeg');
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Burrito', 'Mexican', 'Flour tortillas filled with a mixture of ground beef, refried beans, and chiles then topped with sauce and cheese', 800, 'burrito.jpg');
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Rose Pasta', 'Italian', 'A simple and delicious meal made from scratch with a cream and tomato based sauce', 500, 'pasta.jpg');
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Pastitsio', 'Greek', 'Baked layers of pasta, juicy minced beef, bechamel and tomato sauce, topped melted cheese', 800, 'pastitsio.jpg');
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Tempura', 'Japanese', 'A dish of battered and fried fish, seafood, or vegetables', 400, 'tempura.jpg');
INSERT INTO Menu (Name, Cuisine, Description, Price, Image) VALUES ('Masala Dosa', 'Indian', 'A thin pancake-like flatbread made from fermented soaked rice and black gram beans', 300, 'dosa.jpg');

-- Sales and Offers
INSERT INTO SalesAndOffers (Occasion, Percentage, Image) VALUES ('Independence Day', 10, 'azadisale.jpeg');
INSERT INTO SalesAndOffers (Occasion, Percentage, Image) VALUES ('Eid ul Fitr', 20, 'eidsale.png');

-- Bookings
CALL BookRoom('35202-1111111-1', 3, 'Islamabad', 4);
CALL BookRoom('35202-1111111-1', 8, 'Islamabad', 4);
CALL BookRoom('35202-4444444-1', 9, 'Islamabad', 1);
CALL BookRoom('35202-2222222-0', 3, 'Karachi', 3);
CALL BookRoom('35202-5555555-0', 7, 'Peshawar', 2);

-- Offers
CALL SelectOffer('35202-1111111-1', 2);

-- Orders
CALL PlaceOrder('35202-1111111-1', 5, 2);
CALL PlaceOrder('35202-1111111-1', 3, 1);
CALL PlaceOrder('35202-8433941-2', 7, 3);

-- Payments
-- CALL Paid(2);