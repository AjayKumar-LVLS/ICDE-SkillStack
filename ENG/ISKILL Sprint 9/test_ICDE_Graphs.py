import unittest
import ICDE_Graphs
import ICDE_DataBase
from pymongo import MongoClient
import random


cluster = MongoClient("mongodb+srv://somesh:icdeskillstack@cluster0.odqp5.mongodb.net/myFirstDatabase?retryWrites"
                      "=true&w=majority")
db = cluster["ICDE_DataBase"]
collection = db["ICDE_Collection"]


class TestICDE_Graphs(unittest.TestCase):
    def test_plot_courses_db(self):
        streams = ["Electrical Engineering", "Electronics Engineering", "Computer Engineering", "Civil Engineering",
                   "Mechanical Engineering"]
        stream = streams[random.randint(0, 4)]
        obj = ICDE_DataBase.IcdeDataBase()
        user = " "
        data = obj.collect_courses_data(user, stream, gtest=True)
        df = data[0]
        stream = data[1]
        obj1 = ICDE_Graphs.Graphs()
        test_result = obj1.plot_course_ranks(df, stream, test=True)
        self.assertEqual(test_result, True)

    def test_plot_usage_stats(self):
        name = " "
        streams = ["Electrical Engineering", "Electronics Engineering", "Computer Engineering", "Civil Engineering",
                   "Mechanical Engineering"]
        stream = streams[random.randint(0, 4)]
        obj = ICDE_DataBase.IcdeDataBase()
        user = " "
        data = obj.collect_courses_data(user, stream, gtest=True)
        df = data[0]
        obj1 = ICDE_Graphs.Graphs()
        test_result = ICDE_Graphs.Graphs.plot_usage_stats(obj1, df, name, test=True)
        self.assertEqual(test_result, True)


if __name__ == '__main__':
    unittest.main()
