from pymongo import MongoClient
import bcrypt
import datetime
import pandas as pd
from ICDE_Graphs import Graphs
import pytz

cluster = MongoClient("mongodb+srv://somesh:icdeskillstack@cluster0.odqp5.mongodb.net/myFirstDatabase?retryWrites"
                      "=true&w=majority")
db = cluster["ICDE_DataBase"]
collection = db["ICDE_Collection"]


class IcdeDataBase:
    def create_profile_db(self, profile):

        if collection.find_one({"Email": profile["Email"]}) is not None:
            return False
        else:
            collection.insert_one(profile)
            return True

    def update_pw_db(self, email, new_pw, test=False):
        collection.find_one({"Email": email})
        collection.update_one({"Email": email},
                              {"$set": {"Password": bcrypt.hashpw(new_pw.encode('utf8'), bcrypt.gensalt())}})
        if test:
            return True

    def add_course_db(self, user, course, test=False):
        enrolled_list = collection.find_one({"Email": user})["CoursesEnrolled"]
        enrolled_list.append(course)
        collection.update_one({"Email": user},
                              {"$set": {"CoursesEnrolled": enrolled_list}})
        if test:
            return True

    def drop_course_db(self, user, course, test=False):
        enrolled_list = collection.find_one({"Email": user})["CoursesEnrolled"]
        enrolled_list.remove(course)
        collection.update_one({"Email": user},
                              {"$set": {"CoursesEnrolled": enrolled_list}})
        if test:
            return True

    def add_course_user(self, user, stream, course, test=False):
        userslist = collection.find_one({"_id": "courseranklist"})[stream][course]
        if user not in userslist:
            userslist.append(user)
        DB_stream = collection.find_one({"_id": "courseranklist"})[stream]
        DB_stream[course] = userslist
        collection.update_one(({"_id": "courseranklist"}), {"$set": {stream: DB_stream}})
        if test:
            return True

    def remove_course_user(self, user, stream, course, test=False):
        userslist = collection.find_one({"_id": "courseranklist"})[stream][course]
        if user in userslist:
            userslist.remove(user)
        DB_stream = collection.find_one({"_id": "courseranklist"})[stream]
        DB_stream[course] = userslist
        collection.update_one(({"_id": "courseranklist"}), {"$set": {stream: DB_stream}})
        if test:
            return True

    # this method updates last logged in time in Database
    def update_lastloggedin_time(self, user, test=False):
        time_zome = pytz.timezone("America/Toronto")
        now = datetime.datetime.now(time_zome)
        moment = now.strftime("%Y-%B-%d  %H:%M:%S")
        collection.update_one(({"Email": user}), {"$set": {"Lastloggedintime": moment}})
        if test:
            return True

    # this method updates the usage time of user in Database
    def update_usagetime(self, user, start_time, end_time, test=False):
        now = datetime.datetime.now()
        today = now.strftime("%Y-%B-%d")
        user_stats = collection.find_one({"Email": user})["Usagestats"]
        if today not in user_stats:
            user_stats[today] = int(((end_time - start_time) / 60) + 1)
        if today in user_stats:
            prev_time = user_stats[today]
            new_time = prev_time + int(((end_time - start_time) / 60) + 1)
            user_stats[today] = new_time
        collection.update_one(({"Email": user}), {"$set": {"Usagestats": user_stats}})
        if test:
            return True

    def collect_courses_data(self, user, stream, test=False):
        us = collection.find_one({"_id": "courseranklist"})[stream]
        value_list = []
        course_list = []
        for i in us:
            course_list.append(i)
            value_list.append(us[i])
        rank_list = []
        for i in value_list:
            rank_list.append(len(i))
        k = [rank_list]
        df = pd.DataFrame(k, columns=course_list)
        obj = Graphs()
        if not test:
            Graphs.plot_course_ranks(obj, df, stream)
        if test:
            return True

    # This method will collect usage stats from database
    def collect_usage_stats(self, user, test=False):
        usage = collection.find_one({"Email": user})["Usagestats"]
        dates = []
        time_spent = []
        for i in usage:
            dates.append(i)
            time_spent.append(usage[i])
        k = [time_spent]
        df = pd.DataFrame(k, columns=dates)
        obj = Graphs()
        if not test:
            Graphs.plot_usage_stats(obj, df, collection.find_one({"Email": user})["Firstname"])
        if test:
            return True
