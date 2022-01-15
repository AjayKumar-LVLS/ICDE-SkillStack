import unittest
import ICDE_DataBase
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://somesh:icdeskillstack@cluster0.odqp5.mongodb.net/myFirstDatabase?retryWrites"
                      "=true&w=majority")
db = cluster["ICDE_DataBase"]
collection = db["ICDE_Collection"]


class TestICDE_DataBase(unittest.TestCase):
    profile = {
        "Firstname": "Test_firstname",
        "Lastname": "Test_lastname",
        "Email": "Test_Email",
        "MobileNumber": "Test_0000000000",
        "Password": "Test_#agrslheruhgyweyrgweyrrgyuweyrugwyegwthgrbtgrtre3423",
        "Gender": "Test_Male",
        "Stream": "Test_Stream",
        "DateOfBirth": "Test_1992-09-09",
        "CoursesEnrolled": [],
        "RegistrationDate": "Test_RegistrationDate",
        "Lastloggedintime": "Test_Lastloggedintime",
        "Usagestats": {

        }
    }
    obj = ICDE_DataBase.IcdeDataBase()

    def test1_create_profile_db(self):
        profile_created = ICDE_DataBase.IcdeDataBase.create_profile_db(self.obj, self.profile)
        collection.delete_one({"Email": "Test_Email"})
        self.assertEqual(profile_created, True)

    def test2_create_profile_db(self):
        ICDE_DataBase.IcdeDataBase.create_profile_db(self.obj, self.profile)
        profile_not_created = ICDE_DataBase.IcdeDataBase.create_profile_db(self.obj, self.profile)
        collection.delete_one({"Email": "Test_Email"})
        self.assertEqual(profile_not_created, False)

    def test_update_pw_db(self):
        profile_created = ICDE_DataBase.IcdeDataBase.create_profile_db(self.obj, self.profile)
        password_updated = False
        if profile_created:
            password_updated = ICDE_DataBase.IcdeDataBase.update_pw_db(self.obj, email="Test_Email",
                                                                       new_pw="new_password", test=True)
            collection.delete_one({"Email": "Test_Email"})
        self.assertEqual(password_updated, True)

    def test_add_course_db(self):
        profile_created = ICDE_DataBase.IcdeDataBase.create_profile_db(self.obj, self.profile)
        course_added = False
        if profile_created:
            course_added = ICDE_DataBase.IcdeDataBase.add_course_db(self.obj, user="Test_Email", course="Test_course",
                                                                    test=True)
            collection.delete_one({"Email": "Test_Email"})
        self.assertEqual(course_added, True)

    def test_drop_course_db(self):
        profile_created = ICDE_DataBase.IcdeDataBase.create_profile_db(self.obj, self.profile)
        course_dropped = False
        if profile_created:
            ICDE_DataBase.IcdeDataBase.add_course_db(self.obj, user="Test_Email", course="Test_course",
                                                                      test=True)
            course_dropped = ICDE_DataBase.IcdeDataBase.drop_course_db(self.obj, user="Test_Email",
                                                                       course="Test_course",
                                                                       test=True)
            collection.delete_one({"Email": "Test_Email"})
        self.assertEqual(course_dropped, True)

    def test_add_course_user(self):
        user_added = False
        user_added = ICDE_DataBase.IcdeDataBase.add_course_user(self.obj, user="Test_Email", stream="Civil Engineering", course="CE4:Soil Testing", test=True)
        if user_added:
            rank_data = collection.find_one({"_id": "courseranklist"})["Civil Engineering"]["CE4:Soil Testing"]
            rank_data.remove("Test_Email")
            updated_rank_data = rank_data
            DB_stream = collection.find_one({"_id": "courseranklist"})["Civil Engineering"]
            DB_stream["CE4:Soil Testing"] = updated_rank_data
            collection.update_one(({"_id": "courseranklist"}), {"$set": {"Civil Engineering": DB_stream}})
        self.assertEqual(user_added, True)

    def test_remove_course_user(self):
        user_removed = False
        user_added = ICDE_DataBase.IcdeDataBase.add_course_user(self.obj, user="Test_Email", stream="Civil Engineering",
                                                                course="CE4:Soil Testing", test=True)
        if user_added:
            user_removed = ICDE_DataBase.IcdeDataBase.remove_course_user(self.obj, user="Test_Email", stream="Civil Engineering",
                                                                course="CE4:Soil Testing", test=True)
        self.assertEqual(user_removed, True)

    def test_update_lastloggedin_time(self):
        profile_created = ICDE_DataBase.IcdeDataBase.create_profile_db(self.obj, self.profile)
        last_loggedintime_updated = False
        if profile_created:
            last_loggedintime_updated = ICDE_DataBase.IcdeDataBase.update_lastloggedin_time(self.obj, user="Test_Email", test=True)
            collection.delete_one({"Email": "Test_Email"})
        self.assertEqual(last_loggedintime_updated, True)

    def test_update_usagetime(self):
        profile_created = ICDE_DataBase.IcdeDataBase.create_profile_db(self.obj, self.profile)
        usage_time_updated = False
        if profile_created:
            usage_time_updated = ICDE_DataBase.IcdeDataBase.update_usagetime(self.obj, user="Test_Email",start_time=2, end_time=4, test=True)
            collection.delete_one({"Email": "Test_Email"})
        self.assertEqual(usage_time_updated, True)

    def test_collect_courses_data(self):
        course_data_collected = ICDE_DataBase.IcdeDataBase.collect_courses_data(self.obj, user="Test_Email", stream="General_courses", test=True)
        self.assertEqual(course_data_collected, True)

    def test_collect_usage_stats(self):
        profile_created = ICDE_DataBase.IcdeDataBase.create_profile_db(self.obj, self.profile)
        usage_stats_collected = False
        if profile_created:
            usage_stats_collected = ICDE_DataBase.IcdeDataBase.collect_usage_stats(self.obj, user="Test_Email",test=True)
            collection.delete_one({"Email": "Test_Email"})
        self.assertEqual(usage_stats_collected, True)



