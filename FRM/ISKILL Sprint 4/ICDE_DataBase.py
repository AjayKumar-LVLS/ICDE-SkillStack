from pymongo import MongoClient
import bcrypt

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

