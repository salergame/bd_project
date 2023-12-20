CREATE TABLE Faculties (
    FacultyID INT PRIMARY KEY,
    FacultyName VARCHAR(255)
);
CREATE TABLE Audience (
    AudienceID INT PRIMARY KEY,
    AudienceNumber INT
);
CREATE TABLE Students (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(255),
    Surname VARCHAR(255),
    DateOfBirth DATE,
    FacultyID INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculties(FacultyID)
);
CREATE TABLE Dorms (
    DormitoryID INT PRIMARY KEY,
    HostelName VARCHAR(255),
    Address VARCHAR(255)
);
CREATE TABLE Teachers (
    TeacherID INT PRIMARY KEY,
    Name VARCHAR(255),
    Surname VARCHAR(255),
    FacultyID INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculties(FacultyID)
);

CREATE TABLE Items (
    ItemID INT PRIMARY KEY,
    ItemName VARCHAR(255),
    FacultyID INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculties(FacultyID)
);

CREATE TABLE Ratings (
    RatingID INT PRIMARY KEY,
    Grade INT,
    StudentID INT,
    ItemID INT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE ClassSchedule (
    ScheduleID INT PRIMARY KEY,
    DayOfWeek VARCHAR(255),
    StartTime TIME,
    EndTime TIME,
    ItemID INT,
    AudienceID INT,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
    FOREIGN KEY (AudienceID) REFERENCES Audience(AudienceID)
);



CREATE TABLE Exams (
    ExamID INT PRIMARY KEY,
    ExamDate DATE,
    ItemID INT,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE Tests (
    TestID INT PRIMARY KEY,
    TestDate DATE,
    ItemID INT,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE Library (
    BookID INT PRIMARY KEY,
    BookTitle VARCHAR(255),
    Author VARCHAR(255),
    FacultyID INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculties(FacultyID)
);

CREATE TABLE RegistrationOfCourses (
    RegistrationID INT PRIMARY KEY,
    StudentID INT,
    ItemID INT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE ApplicationForDormitory (
    ApplicationID INT PRIMARY KEY,
    StudentID INT,
    DormitoryID INT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (DormitoryID) REFERENCES Dorms(DormitoryID)
);



CREATE TABLE EventsOnCampus (
    EventID INT PRIMARY KEY,
    EventName VARCHAR(255),
    EventDate DATE
);

CREATE TABLE Accounts (
    AccountsID INT PRIMARY KEY,
    Login VARCHAR(255),
    Password VARCHAR(255),
    Role VARCHAR(255),
    Access VARCHAR(255)
);

CREATE TABLE Admin (
    AdminID INT PRIMARY KEY,
    Name VARCHAR(255),
    Surname VARCHAR(255),
    AccountsID INT,
    FOREIGN KEY (AccountsID) REFERENCES Accounts(AccountsID)
);

INSERT INTO Accounts(AccountsID,Login,Password,Role,Access) VALUES
(1,'salergame07','Sanzh1942','Админ','admin_True'),
(3,'kkk_1001','kk_101','Учитель','admin_False'),
(4,'Random','ran','Студент','admin_False'),
(2,'Elzhaskekmam','maika123','Админ','admin_True');
INSERT INTO Admin(AdminID,Name,Surname) VALUES
(1,'Sanzhar','Sagadibek'),
(2,'Elzhas','Mamraev');
INSERT INTO teachers(teacherID,Name,Surname) VALUES
(1,'Kamron','Tulaboev');
INSERT INTO students(studentID,Name,Surname) VALUES
(1,'First','Firstss');

SELECT Password FROM Accounts;