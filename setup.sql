USE spider;
CREATE TABLE IF NOT EXISTS department (
	Department_ID int,
	Name text,
	Creation text,
	Ranking int,
	Budget_in_Billions real,
	Num_Employees real,
	PRIMARY KEY (Department_ID)
);
INSERT INTO department VALUES(1,'State','1789','1',9.9600000000000008526,30265.999999999999999);
INSERT INTO department VALUES(2,'Treasury','1789','2',11.099999999999999644,115896.99999999999999);
INSERT INTO department VALUES(3,'Defense','1947','3',439.30000000000001135,3000000.0);
INSERT INTO department VALUES(4,'Justice','1870','4',23.399999999999998578,112556.99999999999999);
INSERT INTO department VALUES(5,'Interior','1849','5',10.699999999999999289,71436.000000000000002);
INSERT INTO department VALUES(6,'Agriculture','1889','6',77.599999999999994316,109831.99999999999999);
INSERT INTO department VALUES(7,'Commerce','1903','7',6.2000000000000001776,35999.999999999999999);
INSERT INTO department VALUES(8,'Labor','1913','8',59.700000000000002843,17346.999999999999999);
INSERT INTO department VALUES(9,'Health and Human Services','1953','9',543.20000000000004548,66999.999999999999998);
INSERT INTO department VALUES(10,'Housing and Urban Development','1965','10',46.200000000000002843,10599.999999999999999);
INSERT INTO department VALUES(11,'Transportation','1966','11',58.000000000000000001,58621.999999999999998);
INSERT INTO department VALUES(12,'Energy','1977','12',21.5,116099.99999999999999);
INSERT INTO department VALUES(13,'Education','1979','13',62.799999999999997156,4487.0000000000000001);
INSERT INTO department VALUES(14,'Veterans Affairs','1989','14',73.200000000000002842,234999.99999999999999);
INSERT INTO department VALUES(15,'Homeland Security','2002','15',44.600000000000001422,207999.99999999999999);
CREATE TABLE IF NOT EXISTS head (
	head_ID int,
	name text,
	born_state text,
	age real,
	PRIMARY KEY (head_ID)
);
select * from head;
INSERT INTO head VALUES(1,'Tiger Woods','Alabama',66.999999999999999998);
INSERT INTO head VALUES(2,'Sergio García','California',68.000000000000000001);
INSERT INTO head VALUES(3,'K. J. Choi','Alabama',69.0);
INSERT INTO head VALUES(4,'Dudley Hart','California',51.999999999999999998);
INSERT INTO head VALUES(5,'Jeff Maggert','Delaware',53.000000000000000001);
INSERT INTO head VALUES(6,'Billy Mayfair','California',69.0);
INSERT INTO head VALUES(7,'Stewart Cink','Florida',50.0);
INSERT INTO head VALUES(8,'Nick Faldo','California',55.999999999999999999);
INSERT INTO head VALUES(9,'Pádraig Harrington','Connecticut',43.000000000000000001);
INSERT INTO head VALUES(10,'Franklin Langham','Connecticut',66.999999999999999998);
CREATE TABLE IF NOT EXISTS management (
	department_ID int,
	head_ID int,
	temporary_acting text,
	PRIMARY KEY (Department_ID,head_ID),
	FOREIGN KEY (Department_ID) REFERENCES department(Department_ID),
	FOREIGN KEY (head_ID) REFERENCES head(head_ID)
);
INSERT INTO management VALUES(2,5,'Yes');
INSERT INTO management VALUES(15,4,'Yes');
INSERT INTO management VALUES(2,6,'Yes');
INSERT INTO management VALUES(7,3,'No');
INSERT INTO management VALUES(11,10,'No');

USE spider;

CREATE TABLE city (
City_ID int,
Official_Name text,
Status text,
Area_km_2 real,
Population real,
Census_Ranking text,
PRIMARY KEY (City_ID)
);

CREATE TABLE farm (
Farm_ID int,
Year int,
Total_Horses real,
Working_Horses real,
Total_Cattle real,
Oxen real,
Bulls real,
Cows real,
Pigs real,
Sheep_and_Goats real,
PRIMARY KEY (Farm_ID)
);

CREATE TABLE farm_competition (
Competition_ID int,
Year int,
Theme text,
Host_city_ID int,
Hosts text,
PRIMARY KEY (Competition_ID),
FOREIGN KEY (Host_city_ID) REFERENCES city(City_ID)
);


CREATE TABLE competition_record (
Competition_ID int,
Farm_ID int,
ranks int,
PRIMARY KEY (Competition_ID,Farm_ID),
FOREIGN KEY (Competition_ID) REFERENCES farm_competition(Competition_ID),
FOREIGN KEY (Farm_ID) REFERENCES farm(Farm_ID)
);



INSERT INTO  city VALUES (1,"Grand Falls/Grand-Sault","Town","18.06","5706","636 of 5008");
INSERT INTO  city VALUES (2,"Perth-Andover","Village","8.89","1778","1442 of 5,008");
INSERT INTO  city VALUES (3,"Plaster Rock","Village","3.09","1135","1936 of 5,008");
INSERT INTO  city VALUES (4,"Drummond","Village","8.91","775","2418 of 5008");
INSERT INTO  city VALUES (5,"Aroostook","Village","2.24","351","3460 of 5008");


INSERT INTO  farm VALUES (1,"1927","5056.5","3900.1","8374.5","805.5","31.6","3852.1","4412.4","7956.3");
INSERT INTO  farm VALUES (2,"1928","5486.9","4090.5","8604.8","895.3","32.8","3987.0","6962.9","8112.2");
INSERT INTO  farm VALUES (3,"1929","5607.5","4198.8","7611.0","593.7","26.9","3873.0","4161.2","7030.8");
INSERT INTO  farm VALUES (4,"1930","5308.2","3721.6","6274.1","254.8","49.6","3471.6","3171.8","4533.4");
INSERT INTO  farm VALUES (5,"1931","4781.3","3593.7","6189.5","113.8","40.0","3377.0","3373.3","3364.8");


INSERT INTO  farm_competition VALUES (1,"2013","Carnival M is back!",1,"Miley Cyrus Jared Leto and Karen Mok");
INSERT INTO  farm_competition VALUES (2,"2006","Codehunters",2,"Leehom Wang and Kelly Rowland");
INSERT INTO  farm_competition VALUES (3,"2005","MTV Asia Aid",3,"Alicia Keys");
INSERT INTO  farm_competition VALUES (4,"2004","Valentine's Day",4,"Vanness Wu and Michelle Branch");



INSERT INTO  competition_record VALUES (1,8,1);
INSERT INTO  competition_record VALUES (1,2,2);
INSERT INTO  competition_record VALUES (1,3,3);
INSERT INTO  competition_record VALUES (2,1,3);
INSERT INTO  competition_record VALUES (2,4,1);
INSERT INTO  competition_record VALUES (2,3,2);


use spider;
CREATE TABLE Addresses (
address_id INTEGER NOT NULL,
line_1 VARCHAR(80),
line_2 VARCHAR(80),
city VARCHAR(50),
zip_postcode CHAR(20),
state_province_county VARCHAR(50),
country VARCHAR(50),
PRIMARY KEY (address_id)
);

INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (5, '0900 Roderick Oval
New Albina, WA 19200-7914', 'Suite 096', 'Linnealand', '862', 'Montana', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (9, '966 Dach Ports Apt. 322
Lake Harmonyhaven, VA 65235', 'Apt. 163', 'South Minnie', '716', 'Texas', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (29, '28550 Broderick Underpass Suite 667
Zakaryhaven, WY 22945-1534', 'Apt. 419', 'North Trystanborough', '112', 'Vermont', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (30, '83706 Ana Trafficway Apt. 992
West Jarret, MI 01112', 'Apt. 884', 'Lake Kaley', '431', 'Washington', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (43, '69165 Beatty Station
Haleighstad, MS 55164', 'Suite 333', 'Stephaniemouth', '559', 'Massachusetts', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (45, '242 Pacocha Streets
East Isabellashire, ND 03506', 'Suite 370', 'O''Connellview', '514', 'NewMexico', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (55, '801 Modesto Island Suite 306
Lacyville, VT 34059', 'Suite 764', 'New Alta', '176', 'Mississippi', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (63, '0177 Fisher Dam
Berniershire, KS 00038-7574', 'Apt. 903', 'South Keenan', '613', 'Michigan', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (68, '09471 Hickle Light
Port Maxime, NJ 91550-5409', 'Suite 903', 'Hannahside', '354', 'Connecticut', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (73, '67831 Lavonne Lodge
Olsontown, DC 20894', 'Apt. 756', 'Alizeshire', '687', 'NewMexico', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (82, '228 Fahey Land
Baileymouth, FL 06297-5606', 'Suite 087', 'South Naomibury', '079', 'Ohio', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (88, '1770 Adriel Ramp Apt. 397
West Ashlynnchester, UT 91968', 'Apt. 617', 'East Tavaresburgh', '179', 'SouthDakota', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (92, '8760 Eldon Squares Suite 260
Marquisestad, GA 38537', 'Apt. 435', 'Lake Devon', '244', 'SouthDakota', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (94, '8263 Abbott Crossing Apt. 066
Oberbrunnerbury, LA 67451', 'Apt. 626', 'Boyleshire', '536', 'Kansas', 'USA');
INSERT INTO Addresses (`address_id`, `line_1`, `line_2`, `city`, `zip_postcode`, `state_province_county`, `country`) VALUES (99, '521 Paucek Field
North Oscartown, WI 31527', 'Apt. 849', 'Terencetown', '979', 'Michigan', 'USA');

CREATE TABLE People (
person_id INTEGER NOT NULL,
first_name VARCHAR(255),
middle_name VARCHAR(255),
last_name VARCHAR(255),
cell_mobile_number VARCHAR(40),
email_address VARCHAR(40),
login_name VARCHAR(40),
password VARCHAR(40),
PRIMARY KEY (person_id)
);
INSERT INTO People (`person_id`, `first_name`, `middle_name`, `last_name`, `cell_mobile_number`, `email_address`, `login_name`, `password`) VALUES (111, 'Shannon', 'Elissa', 'Senger', '01955267735', 'javier.trantow@example.net', 'pgub', '5e4ff49a61b3544da3ad7dc7e2cf28847564c64c');
INSERT INTO People (`person_id`, `first_name`, `middle_name`, `last_name`, `cell_mobile_number`, `email_address`, `login_name`, `password`) VALUES (131, 'Dariana', 'Hayley', 'Bednar', '(262)347-9364x516', 'leila14@example.net', 'zops', 'b20b6a9f24aadeda70d54e410c3219f61fb063fb');
INSERT INTO People (`person_id`, `first_name`, `middle_name`, `last_name`, `cell_mobile_number`, `email_address`, `login_name`, `password`) VALUES (121, 'Virginie', 'Jasmin', 'Hartmann', '(508)319-2970x043', 'boyer.lonie@example.com', 'bkkv', 'b063331ea8116befaa7b84c59c6a22200f5f8caa');
INSERT INTO People (`person_id`, `first_name`, `middle_name`, `last_name`, `cell_mobile_number`, `email_address`, `login_name`, `password`) VALUES (141, 'Verna', 'Arielle', 'Grant', '1-372-548-7538x314', 'adele.gibson@example.net', 'uuol', '7be9c03d5467d563555c51ebb3eb78e7f90832ec');
INSERT INTO People (`person_id`, `first_name`, `middle_name`, `last_name`, `cell_mobile_number`, `email_address`, `login_name`, `password`) VALUES (151, 'Hoyt', 'Mercedes', 'Wintheiser', '1-603-110-0647', 'stanley.monahan@example.org', 'bnto', 'c55795df86182959094b83e27900f7cf44ced570');
INSERT INTO People (`person_id`, `first_name`, `middle_name`, `last_name`, `cell_mobile_number`, `email_address`, `login_name`, `password`) VALUES (161, 'Mayra', 'Haley', 'Hartmann', '724-681-4161x51632', 'terry.kuhlman@example.org', 'rzxu', 'ecae473cb54601e01457078ac0cdf4a1ced837bb');
INSERT INTO People (`person_id`, `first_name`, `middle_name`, `last_name`, `cell_mobile_number`, `email_address`, `login_name`, `password`) VALUES (171, 'Lizeth', 'Bell', 'Bartoletti', '812.228.0645x91481', 'celestine11@example.net', 'mkou', '76a93d1d3b7becc932d203beac61d064bd54e947');
INSERT INTO People (`person_id`, `first_name`, `middle_name`, `last_name`, `cell_mobile_number`, `email_address`, `login_name`, `password`) VALUES (181, 'Nova', 'Amiya', 'Feest', '766-272-9964', 'oreynolds@example.com', 'qrwl', '7dce9b688636ee212294c257dd2f6b85c7f65f2e');

CREATE TABLE Students (
student_id INTEGER NOT NULL,
student_details VARCHAR(255),
PRIMARY KEY (student_id),
FOREIGN KEY (student_id) REFERENCES People (person_id)
);
INSERT INTO Students (`student_id`,`student_details`) VALUES  (111,'Marry');
INSERT INTO Students (`student_id`,`student_details`) VALUES  (121,'Martin');
INSERT INTO Students (`student_id`,`student_details`) VALUES  (131,'Barry');
INSERT INTO Students (`student_id`,`student_details`) VALUES  (141,'Nikhil');
INSERT INTO Students (`student_id`,`student_details`) VALUES  (151,'John');
INSERT INTO Students (`student_id`,`student_details`) VALUES  (161,'Sarah');
INSERT INTO Students (`student_id`,`student_details`) VALUES  (171,'Joe');
INSERT INTO Students (`student_id`,`student_details`) VALUES  (181,'Nancy');

CREATE TABLE Courses (
course_id INTEGER NOT NULL,
course_name VARCHAR(120),
course_description VARCHAR(255),
other_details VARCHAR(255),
PRIMARY KEY (course_id)
);
INSERT INTO Courses (`course_id`, `course_name`, `course_description`) VALUES ('301', 'statistics', 'statistics');
INSERT INTO Courses (`course_id`, `course_name`, `course_description`) VALUES ('302', 'English', 'English');
INSERT INTO Courses (`course_id`, `course_name`, `course_description`) VALUES ('303', 'French', 'French');
INSERT INTO Courses (`course_id`, `course_name`, `course_description`) VALUES ('304', 'database', 'database');
INSERT INTO Courses (`course_id`, `course_name`, `course_description`) VALUES ('305', 'data structure', 'data structure');
INSERT INTO Courses (`course_id`, `course_name`, `course_description`) VALUES ('306', 'Art history', 'Art history');

CREATE TABLE People_Addresses (
person_address_id INTEGER NOT NULL,
person_id INTEGER NOT NULL,
address_id INTEGER NOT NULL,
date_from DATETIME,
date_to DATETIME,
PRIMARY KEY (person_address_id),
FOREIGN KEY (person_id) REFERENCES People (person_id),
FOREIGN KEY (address_id) REFERENCES Addresses (address_id)
);
INSERT INTO People_Addresses (`person_address_id`, `person_id`, `address_id`, `date_from`, `date_to`) VALUES (122, 111, 9, '2012-09-26 13:21:00', '2018-03-21 09:46:30');
INSERT INTO People_Addresses (`person_address_id`, `person_id`, `address_id`, `date_from`, `date_to`) VALUES (257, 121, 5, '2008-07-31 02:17:25', '2018-03-09 02:11:12');
INSERT INTO People_Addresses (`person_address_id`, `person_id`, `address_id`, `date_from`, `date_to`) VALUES (269, 131, 88, '2008-05-26 20:43:41', '2018-03-11 20:26:41');
INSERT INTO People_Addresses (`person_address_id`, `person_id`, `address_id`, `date_from`, `date_to`) VALUES (276, 141, 99, '2014-05-10 00:32:31', '2018-03-08 06:16:47');
INSERT INTO People_Addresses (`person_address_id`, `person_id`, `address_id`, `date_from`, `date_to`) VALUES (281, 151, 92, '2010-11-26 05:21:12', '2018-03-12 21:10:02');
INSERT INTO People_Addresses (`person_address_id`, `person_id`, `address_id`, `date_from`, `date_to`) VALUES (340, 161, 45, '2017-05-01 17:32:26', '2018-03-09 08:45:06');
INSERT INTO People_Addresses (`person_address_id`, `person_id`, `address_id`, `date_from`, `date_to`) VALUES (363, 171, 55, '2015-05-24 16:14:12', '2018-02-23 22:44:18');
INSERT INTO People_Addresses (`person_address_id`, `person_id`, `address_id`, `date_from`, `date_to`) VALUES (396, 181, 82, '2013-12-26 16:57:01', '2018-03-03 16:06:17');

CREATE TABLE Student_Course_Registrations (
student_id INTEGER NOT NULL,
course_id INTEGER NOT NULL,
registration_date DATETIME NOT NULL,
FOREIGN KEY (student_id) REFERENCES Students (student_id),
FOREIGN KEY (course_id) REFERENCES Courses (course_id)
);

INSERT INTO Student_Course_Registrations (`student_id`,`course_id`,`registration_date`) VALUES (111,'301','2008-11-04 10:35:13');
INSERT INTO Student_Course_Registrations (`student_id`,`course_id`,`registration_date`) VALUES (121,'301','2008-10-04 10:35:13');
INSERT INTO Student_Course_Registrations (`student_id`,`course_id`,`registration_date`) VALUES (121,'303','2008-11-14 10:35:13');
INSERT INTO Student_Course_Registrations (`student_id`,`course_id`,`registration_date`) VALUES (131,'303','2008-11-05 10:35:13');
INSERT INTO Student_Course_Registrations (`student_id`,`course_id`,`registration_date`) VALUES (141,'302','2008-11-06 10:35:13');
INSERT INTO Student_Course_Registrations (`student_id`,`course_id`,`registration_date`) VALUES (151,'305','2008-11-07 10:35:13');
INSERT INTO Student_Course_Registrations (`student_id`,`course_id`,`registration_date`) VALUES (161,'302','2008-11-07 10:35:13');
INSERT INTO Student_Course_Registrations (`student_id`,`course_id`,`registration_date`) VALUES (171,'301','2008-11-07 10:35:13');
INSERT INTO Student_Course_Registrations (`student_id`,`course_id`,`registration_date`) VALUES (141,'301','2008-11-08 10:35:13');


CREATE TABLE Student_Course_Attendance (
student_id INTEGER NOT NULL,
course_id INTEGER NOT NULL,
date_of_attendance DATETIME NOT NULL,
PRIMARY KEY (student_id, course_id),
FOREIGN KEY (student_id, course_id) REFERENCES Student_Course_Registrations (student_id,course_id)
);

INSERT INTO Student_Course_Attendance (`student_id`,`course_id`,`date_of_attendance`) VALUES (111,'301','2008-11-04 10:35:13');
INSERT INTO Student_Course_Attendance (`student_id`,`course_id`,`date_of_attendance`) VALUES (121,'301','2012-04-09 11:44:34');
INSERT INTO Student_Course_Attendance (`student_id`,`course_id`,`date_of_attendance`) VALUES (121,'303','2014-04-09 11:44:34');
INSERT INTO Student_Course_Attendance (`student_id`,`course_id`,`date_of_attendance`) VALUES (141,'302','2013-04-09 11:44:34');
INSERT INTO Student_Course_Attendance (`student_id`,`course_id`,`date_of_attendance`) VALUES (171,'301','2015-04-09 11:44:34');
INSERT INTO Student_Course_Attendance (`student_id`,`course_id`,`date_of_attendance`) VALUES (161,'302','2014-01-09 11:44:34');
INSERT INTO Student_Course_Attendance (`student_id`,`course_id`,`date_of_attendance`) VALUES (151,'305','2012-05-09 11:44:34');
INSERT INTO Student_Course_Attendance (`student_id`,`course_id`,`date_of_attendance`) VALUES (141,'301','2012-09-09 11:44:34');


CREATE TABLE Candidates (
candidate_id INTEGER NOT NULL ,
candidate_details VARCHAR(255),
PRIMARY KEY (candidate_id),
FOREIGN KEY (candidate_id) REFERENCES People (person_id)
);

CREATE TABLE Candidate_Assessments (
candidate_id INTEGER NOT NULL,
qualification CHAR(15) NOT NULL,
assessment_date DATETIME NOT NULL,
asessment_outcome_code CHAR(15) NOT NULL,
PRIMARY KEY (candidate_id, qualification),
FOREIGN KEY (candidate_id) REFERENCES Candidates (candidate_id)
);
INSERT INTO Candidates (`candidate_id`,`candidate_details`) VALUES  (111,'Jane');
INSERT INTO Candidates (`candidate_id`,`candidate_details`) VALUES  (121,'Robert');
INSERT INTO Candidates (`candidate_id`,`candidate_details`) VALUES  (131,'Alex');
INSERT INTO Candidates (`candidate_id`,`candidate_details`) VALUES  (141,'Tao');
INSERT INTO Candidates (`candidate_id`,`candidate_details`) VALUES  (151,'Jack');
INSERT INTO Candidates (`candidate_id`,`candidate_details`) VALUES  (161,'Leo');
INSERT INTO Candidates (`candidate_id`,`candidate_details`) VALUES  (171,'Robin');
INSERT INTO Candidates (`candidate_id`,`candidate_details`) VALUES  (181,'Cindy');


INSERT INTO Candidate_Assessments (`candidate_id`,`qualification`,`assessment_date`,`asessment_outcome_code`) VALUES (111,'A','2010-04-07 11:44:34','Pass');
INSERT INTO Candidate_Assessments (`candidate_id`,`qualification`,`assessment_date`,`asessment_outcome_code`) VALUES (121,'B','2010-04-17 11:44:34','Pass');
INSERT INTO Candidate_Assessments (`candidate_id`,`qualification`,`assessment_date`,`asessment_outcome_code`) VALUES (131,'D','2010-04-05 11:44:34','Fail');
INSERT INTO Candidate_Assessments (`candidate_id`,`qualification`,`assessment_date`,`asessment_outcome_code`) VALUES (141,'C','2010-04-06 11:44:34','Pass');
INSERT INTO Candidate_Assessments (`candidate_id`,`qualification`,`assessment_date`,`asessment_outcome_code`) VALUES (151,'B','2010-04-09 11:44:34','Pass');
