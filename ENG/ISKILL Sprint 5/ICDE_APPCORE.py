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

