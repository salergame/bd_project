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
CREATE TABLE groups(
    groupid serial primary key,
    studentid int,
    FOREIGN KEY (studentid) REFERENCES Students(studentid)
);
CREATE TABLE courses(
    coursid serial primary key,
    groupid int,
    FOREIGN KEY (groupid) REFERENCES groups(groupid) 
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
WHERE Students.StudentID = 12; 

UPDATE students
SET studentid = 12
WHERE studentid = 23;

UPDATE students
SET studentid = 13
WHERE studentid = 24;

UPDATE students
SET studentid = 14
WHERE studentid = 25;

UPDATE students
SET studentid = 15
WHERE studentid = 26;

UPDATE students
SET studentid = 16
WHERE studentid = 27;

UPDATE students
SET studentid = 17
WHERE studentid = 28;

UPDATE students
SET studentid = 18
WHERE studentid = 29;

UPDATE students
SET studentid = 19
WHERE studentid = 30;

UPDATE students
SET studentid = 20
WHERE studentid = 31;

UPDATE students
SET studentid = 21
WHERE studentid = 32;

UPDATE students
SET studentid = 22
WHERE studentid = 33;

UPDATE students
SET studentid = 23
WHERE studentid = 34;

UPDATE students
SET studentid = 24
WHERE studentid = 35;

UPDATE students
SET studentid = 25
WHERE studentid = 36;

UPDATE students
SET studentid = 26
WHERE studentid = 37;

UPDATE students
SET studentid = 27
WHERE studentid = 38;

UPDATE students
SET studentid = 28
WHERE studentid = 39;

UPDATE students
SET studentid = 29
WHERE studentid = 40;

UPDATE students
SET studentid = 30
WHERE studentid = 41;

UPDATE students
SET studentid = 31
WHERE studentid = 42;
-- ALTER TABLE Students
-- ADD COLUMN AccountsID INTEGER,
-- ADD CONSTRAINT fk_students_accounts
--     FOREIGN KEY (AccountsID) 
--     REFERENCES Accounts(AccountsID)
-- 	ON DELETE CASCADE;
SELECT * FROM STUDENTS
SELECT * FROM ACCOUNTS
ALTER SEQUENCE Accounts_accountsid_seq RESTART WITH 1;
SELECT setval('Accounts_accountsid_seq', 58, false);
SELECT setval(pg_get_serial_sequence('accounts', 'accountsid'), (SELECT MAX(accountsid) FROM accounts)+1);
SELECT * FROM classschedule
UPDATE STUDENTS
SET ACCOUNTSID =14
WHERE STUDENTID = 10;
SELECT * FROM GROUPS
ALTER TABLE groups DROP CONSTRAINT groupid;
ALTER TABLE GROUP DROP COLUMN new_column
select * from courses
ALTER TABLE COURSES ADD COLUMN COURS_NUMBER INT

CREATE TABLE groups(
    groupid serial primary key,
    studentid int,
	GROUP_NAME VARCHAR,
    FOREIGN KEY (studentid) REFERENCES Students(studentid)
);
SELECT * FROM RATINGS
SELECT * FROM STUDENTS
SELECT * FROM ITEMS



-- Расписание для группы ПО2209
INSERT INTO ClassSchedule (DayOfWeek, StartTime, EndTime, ItemID, AudienceID, GroupID, LessonNumber) VALUES
('Monday', '08:00', '10:00', 1, 101, 1, 1),
('Monday', '10:00', '12:00', 2, 102, 1, 2),
('Monday', '13:00', '15:00', 3, 103, 1, 3),
('Monday', '15:00', '17:00', 4, 104, 1, 4),
('Wednesday', '14:00', '16:00', 5, 105, 1, 1),
('Wednesday', '16:00', '18:00', 6, 106, 1, 2),
('Wednesday', '18:00', '20:00', 7, 107, 1, 3),
('Wednesday', '20:00', '22:00', 8, 108, 1, 4),
('Friday', '13:00', '15:00', 9, 109, 1, 1),
('Friday', '15:00', '17:00', 10, 110, 1, 2),
('Friday', '17:00', '19:00', 11, 111, 1, 3),
('Friday', '19:00', '21:00', 12, 112, 1, 4),
('Saturday', '15:00', '17:00', 13, 113, 1, 1),
('Saturday', '17:00', '19:00', 14, 114, 1, 2),
('Saturday', '19:00', '21:00', 15, 115, 1, 3),
('Saturday', '21:00', '23:00', 16, 116, 1, 4),
('Sunday', '16:00', '18:00', 17, 117, 1, 1),
('Sunday', '18:00', '20:00', 18, 118, 1, 2),
('Sunday', '20:00', '22:00', 19, 119, 1, 3),
('Sunday', '22:00', '00:00', 20, 120, 1, 4);

-- Расписание для группы ПО2201
INSERT INTO ClassSchedule (DayOfWeek, StartTime, EndTime, ItemID, AudienceID, GroupID, LessonNumber) VALUES
('Monday', '10:00', '12:00', 1, 101, 2, 1),
('Monday', '12:00', '14:00', 2, 102, 2, 2),
('Monday', '14:00', '16:00', 3, 103, 2, 3),
('Monday', '16:00', '18:00', 4, 104, 2, 4),
('Wednesday', '15:00', '17:00', 5, 105, 2, 1),
('Wednesday', '17:00', '19:00', 6, 106, 2, 2),
('Wednesday', '19:00', '21:00', 7, 107, 2, 3),
('Wednesday', '21:00', '23:00', 8, 108, 2, 4),
('Friday', '11:00', '13:00', 9, 109, 2, 1),
('Friday', '13:00', '15:00', 10, 110, 2, 2),
('Friday', '15:00', '17:00', 11, 111, 2, 3),
('Friday', '17:00', '19:00', 12, 112, 2, 4),
('Saturday', '14:00', '16:00', 13, 113, 2, 1),
('Saturday', '16:00', '18:00', 14, 114, 2, 2),
('Saturday', '18:00', '20:00', 15, 115, 2, 3),
('Saturday', '20:00', '22:00', 16, 116, 2, 4),
('Sunday', '17:00', '19:00', 17, 117, 2, 1),
('Sunday', '19:00', '21:00', 18, 118, 2, 2),
('Sunday', '21:00', '23:00', 19, 119, 2, 3),
('Sunday', '23:00', '00:00', 20, 120, 2, 4);

-- Расписание для группы ВТ2203
INSERT INTO ClassSchedule (DayOfWeek, StartTime, EndTime, ItemID, AudienceID, GroupID, LessonNumber) VALUES
('Monday', '13:00', '15:00', 1, 101, 3, 1),
('Monday', '15:00', '17:00', 2, 102, 3, 2),
('Monday', '17:00', '19:00', 3, 103, 3, 3),
('Monday', '19:00', '21:00', 4, 104, 3, 4),
('Wednesday', '11:00', '13:00', 5, 105, 3, 1),
('Wednesday', '13:00', '15:00', 6, 106, 3, 2),
('Wednesday', '15:00', '17:00', 7, 107, 3, 3),
('Wednesday', '17:00', '19:00', 8, 108, 3, 4),
('Friday', '16:00', '18:00', 9, 109, 3, 1),
('Friday', '18:00', '20:00', 10, 110, 3, 2),
('Friday', '20:00', '22:00', 11, 111, 3, 3),
('Friday', '22:00', '00:00', 12, 112, 3, 4),
('Saturday', '09:00', '11:00', 13, 113, 3, 1),
('Saturday', '11:00', '13:00', 14, 114, 3, 2),
('Saturday', '13:00', '15:00', 15, 115, 3, 3),
('Saturday', '15:00', '17:00', 16, 116, 3, 4),
('Sunday', '12:00', '14:00', 17, 117, 3, 1),
('Sunday', '14:00', '16:00', 18, 118, 3, 2),
('Sunday', '16:00', '18:00', 19, 119, 3, 3),
('Sunday', '18:00', '20:00', 20, 120, 3, 4);



