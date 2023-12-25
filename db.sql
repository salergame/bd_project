-- Создаем таблицы заново с типами данных SERIAL
CREATE TABLE Faculties (
    FacultyID SERIAL PRIMARY KEY,
    FacultyName VARCHAR(255)
);

CREATE TABLE Audience (
    AudienceID SERIAL PRIMARY KEY,
    AudienceNumber INT
);

CREATE TABLE Students (
    StudentID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Surname VARCHAR(255),
    DateOfBirth DATE,
    FacultyID INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculties(FacultyID)
);

CREATE TABLE Dorms (
    DormitoryID SERIAL PRIMARY KEY,
    HostelName VARCHAR(255),
    Address VARCHAR(255)
);

CREATE TABLE Teachers (
    TeacherID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Surname VARCHAR(255),
    FacultyID INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculties(FacultyID)
);

CREATE TABLE Items (
    ItemID SERIAL PRIMARY KEY,
    ItemName VARCHAR(255),
    FacultyID INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculties(FacultyID)
);

CREATE TABLE Ratings (
    RatingID SERIAL PRIMARY KEY,
    Grade INT,
    StudentID INT,
    ItemID INT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE ClassSchedule (
    ScheduleID SERIAL PRIMARY KEY,
    DayOfWeek VARCHAR(255),
    StartTime TIME,
    EndTime TIME,
    ItemID INT,
    AudienceID INT,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
    FOREIGN KEY (AudienceID) REFERENCES Audience(AudienceID)
);

CREATE TABLE Exams (
    ExamID SERIAL PRIMARY KEY,
    ExamDate DATE,
    ItemID INT,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE Tests (
    TestID SERIAL PRIMARY KEY,
    TestDate DATE,
    ItemID INT,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE Library (
    BookID SERIAL PRIMARY KEY,
    BookTitle VARCHAR(255),
    Author VARCHAR(255),
    FacultyID INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculties(FacultyID)
);

CREATE TABLE RegistrationOfCourses (
    RegistrationID SERIAL PRIMARY KEY,
    StudentID INT,
    ItemID INT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE ApplicationForDormitory (
    ApplicationID SERIAL PRIMARY KEY,
    StudentID INT,
    DormitoryID INT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (DormitoryID) REFERENCES Dorms(DormitoryID)
);

CREATE TABLE EventsOnCampus (
    EventID SERIAL PRIMARY KEY,
    EventName VARCHAR(255),
    EventDate DATE
);

CREATE TABLE Accounts (
    AccountsID SERIAL PRIMARY KEY,
    Login VARCHAR(255),
    Password VARCHAR(255),
    Role VARCHAR(255),
    Access VARCHAR(255)
);

CREATE TABLE Admin (
    AdminID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Surname VARCHAR(255),
    AccountsID INT,
    FOREIGN KEY (AccountsID) REFERENCES Accounts(AccountsID)
);
SELECT * FROM Faculties;

SELECT * FROM Audience;

SELECT * FROM Students;

SELECT * FROM Dorms;

SELECT * FROM Teachers;

SELECT * FROM Items;

SELECT * FROM Ratings;

SELECT * FROM ClassSchedule;

SELECT * FROM Exams;

SELECT * FROM Tests;

SELECT * FROM Library;

SELECT * FROM RegistrationOfCourses;

SELECT * FROM ApplicationForDormitory;

SELECT * FROM EventsOnCampus;

SELECT * FROM Accounts;

SELECT * FROM Admin;

INSERT INTO Accounts(AccountsID,Login,Password,Role,Access) VALUES
(1,'salergame07','Sanzh1942','Админ'),
(3,'kkk_1001','kk_101','Учитель'),
(4,'Random','ran','Студент'),
(2,'Elzhaskekmam','maika123','Админ');
INSERT INTO Admin(AdminID,Name,Surname) VALUES
(1,'Sanzhar','Sagadibek'),
(2,'Elzhas','Mamraev');
INSERT INTO teachers(teacherID,Name,Surname) VALUES
(1,'Kamron','Tulaboev');
INSERT INTO students(studentID,Name,Surname) VALUES
(1,'First','Firstss');

SELECT Password FROM Accounts;



SELECT * FROM Items
SELECT * FROM Faculties
SELECT Students.name, Ratings.grade FROM Students LEFT JOIN Ratings ON Students.studentid = Ratings.studentid; 
SELECT * FROM admin

SELECT * FROM ACCOUNTS
SELECT * FROM students
SELECT * FROM Teachers



UPDATE Students
SET AccountsID = (SELECT AccountsID FROM Accounts WHERE Role = 'Студент' LIMIT 1);


)
WHERE AccountsID IS NULL;








SELECT Teachers.name , Items.itemname
FROM Teachers
LEFT JOIN Items 
ON Teachers.teacherid = Items.itemid

SELECT  Accounts.login,Teachers.name 
FROM accounts 
INNER JOIN Teachers
ON Accounts.AccountsID=Teachers.accountsid

SELECT * FROM Ratings
ALTER TABLE Accounts DROP COLUMN access
ALTER TABLE students RENAME COLUMN studentaccountid TO AccountID;
SELECT Students.Name, Items.ItemName, Ratings.Grade
FROM Students
LEFT JOIN Ratings ON Students.StudentID = Ratings.StudentID
LEFT JOIN Items ON Ratings.ItemID = Items.ItemID
WHERE Students.StudentID = 12; -- Замените 1 на ID нужного вам студента