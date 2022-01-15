from pymongo import MongoClient
import bcrypt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

    def update_pw_db(self, email, new_pw):
        collection.find_one({"Email": email})
        collection.update_one({"Email": email},
                              {"$set": {"Password": bcrypt.hashpw(new_pw.encode('utf8'), bcrypt.gensalt())}})

    def add_course_db(self, user, course):
        enrolled_list = collection.find_one({"Email": user})["CoursesEnrolled"]
        enrolled_list.append(course)
        collection.update_one({"Email": user},
                              {"$set": {"CoursesEnrolled": enrolled_list}})

    def drop_course_db(self,user,course):
        enrolled_list = collection.find_one({"Email": user})["CoursesEnrolled"]
        enrolled_list.remove(course)
        collection.update_one({"Email": user},
                              {"$set": {"CoursesEnrolled": enrolled_list}})

    def add_course_user(self, user, stream, course):
        print("Hello")
        print(stream)
        userslist = collection.find_one({"_id": "courseranklist"})[stream][course]
        if user not in userslist:
            userslist.append(user)
        DB_stream = collection.find_one({"_id": "courseranklist"})[stream]
        DB_stream[course] = userslist
        collection.update_one(({"_id": "courseranklist"}), {"$set": {stream: DB_stream}})

    def remove_course_user(self, user, stream, course):
        userslist = collection.find_one({"_id": "courseranklist"})[stream][course]
        if user in userslist:
            userslist.remove(user)
        DB_stream = collection.find_one({"_id": "courseranklist"})[stream]
        DB_stream[course] = userslist
        collection.update_one(({"_id": "courseranklist"}), {"$set": {stream: DB_stream}})

    def collect_user_data(self, user, stream):
        us = collection.find_one({"_id": "courseranklist"})[stream]
        value_list = []
        course_list = []
        for i in us:                            #
            course_list.append(i)
            value_list.append(us[i])
        print(course_list)
        rank_list = []
        for i in value_list:
            rank_list.append(len(i))
        print(rank_list)
        # r_list=[]
        # df = pd.DataFrame({'course_list':[rank_list],'course':['Civil','Comp','elec','electro','mech']})
        # print(df)




        # plt.style.use("fivethirtyeight")

        x = course_list
        y = rank_list
        # x_index = np.arange(len(x))
        plt.barh(x, y)
        # plt.legend()
        plt.show()

    # def plot(self, rank_list, course_list):
    #
    #     x = course_list[]
    #     y = rank_list[]
    #
    #     plt.plot(x, y)
    #
    #     plt.xlabel('x - axis')
    #     plt.ylabel('y - axis')
    #
    #
    #     plt.title('My first graph!')
    #
    #
    #     plt.show()




        # value_list = us['Spark! Articulate and Communicate your skills']
        #
        #
        # print(value_list)
        # print(len(value_list))


        # print(us.get('Spark! Articulate and Communicate your skills', 'Essential Soft Skills for Career Success'))
        # uselist = collection.find_one({"_id": "courseranklist"})[stream][course]
        # print(uselist)
        # print(us)








