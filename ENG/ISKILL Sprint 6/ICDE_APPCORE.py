import bcrypt
from pymongo import MongoClient
import datetime
from ICDE_DataBase import IcdeDataBase

cluster = MongoClient("mongodb+srv://somesh:icdeskillstack@cluster0.odqp5.mongodb.net/myFirstDatabase?retryWrites"
                      "=true&w=majority")
db = cluster["ICDE_DataBase"]
collection = db["ICDE_Collection"]

class Data_Verification:
    # Password hashing

    def PwHashing(self, password):
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        return hashed_pw

    # Verify Credentials
    def VerifyUser(self, Email, password):
        # verify user credentials and authenticate user.
        profile = collection.find_one({"Email": Email})
        if profile == None:
            return False
        else:
            Stored_hashedpw = profile["Password"]
            Given_hashedpw = bcrypt.hashpw(password.encode('utf8'), Stored_hashedpw)

            if Given_hashedpw == Stored_hashedpw:
                return True
            else:
                return False

    # Verify Security question
    def VerifySeqQn(self, Email, DOB):
        profile = collection.find_one({"Email": Email})
        if profile["DateOfBirth"] == DOB:
            return True
        else:
            return False


class IcdeAppCore:
    def createProfile(self, firstname, lastname, username, phone_number, password, reentered_password, gender,
                      stream, date_of_birth):
        #global enrolled_courselist
        if gender == 1:
            gender = "Male"
        if gender == 2:
            gender = "Female"

        profile = {
            "Firstname": firstname,
            "Lastname": lastname,
            "Email": username,
            "MobileNumber": phone_number,
            "Password": Data_Verification.PwHashing(self, password),
            "Gender": gender,
            "Stream": stream,
            "DateOfBirth": date_of_birth,
            "CoursesEnrolled": [],
            "RegistrationDate": datetime.datetime.today()
        }
        profile_created = IcdeDataBase.create_profile_db(self, profile)
        return profile_created

    def check_enrollement(self, current_user, course):
        profile = collection.find_one({"Email": current_user})
        if course not in profile["CoursesEnrolled"]:
            return True
        else:
            return False
    def add_course_list(self,stream):
            courses = {
            "_id": "courseranklist",
            'General_courses': {
                'Spark! Articulate and Communicate your skills': [],
                "Essential Soft Skills for Career Success": [],
                "Guide to Entreprenuership": [],
                "Practicing Agility- Lean Start-Up and SCRUM Basics": [],
                "Library Skills & Resources- Maximize Your Graduate Research Potential": []
            },

            'Electrical_courses':
                {
                    "EE1:Electrical Power Engineering Principles": [],
                    "EE2:Power Engineering-Power system Analysis": [],
                    "EE3:Electrical Control & Protection Systems": [],
                    "EE4:Electrical Power Equipment": [],
                    "EE5:Distribution Power Engineering Fundamentals": []
                },
            'Electronics_courses':
                {
                    "EC1:Digital Electronics & Logic Design": [],
                    "EC2:Arduino Programming and Hardware Fundamentals with Hackster": [],
                    "EC3:Industrial Robotics": [],
                    "EC4:Computer architecture and Design": [],
                    "EC5:Functional Hardware Verification": []
                },
            'Computer_courses':
                {
                    "CE1:Learning Python Programming Masterclass": [],
                    "CE2:C Programming for Beginners": [],
                    "CE3:Machine Learning": [],
                    "CE4:Mastering Data Structures and Algorithms": [],
                    "CE5:Ultimate AWS Certified Solutions Architect": []
                },
            'Civil_courses':
                {
                    "CE1:Structual Engineering": [],
                    "CE2:Mastering AUTOCAD": [],
                    "CE3:Architecture": [],
                    "CE4:Soil Testing": [],
                    "CE5:Concrete Technology": []
                },
            'Mechanical_courses':
                {
                    "ME1:Fluid Mechanics": [],
                    "ME2:Applied Thermodynamics": [],
                    "ME3:Heat and Mass Transfer": [],
                    "ME4:Design of Machine Elements": [],
                    "ME5:Dynamics of Machinery": []
                },
        'NonTech_courses':
            {
                "French language": [],
                "English proficiency": [],
                "Communication Skills": [],
                "Softskills": [],
                "Creativity,Innovation": []
            }
        }
        # course_list_created = IcdeDataBase.add_course_user(courses)
        # return course_list_created
        # # p = collection.find_one({"Firstname": profile["Firstname"]})
