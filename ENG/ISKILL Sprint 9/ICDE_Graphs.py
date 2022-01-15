import matplotlib.pyplot as plt
import random
import numpy as np
import tkinter
from tkinter import messagebox


class Graphs():
    # This method will plot the course rankings
    def plot_course_ranks(self, df, stream, test=False):
        courses = df.columns.values.tolist()
        df_ranks = df.values.tolist()
        ranks_courses = df_ranks[0]
        plt.xlabel("Courses", fontsize=15)
        plt.ylabel("Number of students enrolled", fontsize=15)
        title = str(stream) + " courses analysis"
        plt.title(title)
        colors_lib = ["blue", "green", "red", "orange", "yellow", "purple", "lavender", "cyan"]
        colors = []
        while 1 < 2:
            k = random.randint(0, 7)
            if colors_lib[k] not in colors:
                colors.append(colors_lib[k])
            if len(colors) == len(courses):
                break
        if not test:
            plt.bar(courses, ranks_courses, width=0.5, color=colors)
            plt.yticks(np.arange(0, (200 + max(ranks_courses)), 100))
            for a, b in zip(courses, ranks_courses):
                plt.text(a, b, str(b), fontsize=15)
            plt.show()
        if test:
            return True

    # This method will plot the usage stasts
    def plot_usage_stats(self, df, name, test = False):
        dates = df.columns.values.tolist()
        x = len(df.columns)
        df_time = df.values.tolist()
        time_spent = df_time[0]
        plt.xlabel("Date", fontsize=15)
        plt.ylabel("Time spent in minutes", fontsize=15)
        title = str(name) + "'s  last 7 days usage stats"
        plt.title(title, fontsize=18)
        colors_lib = ["blue", "green", "red", "orange", "yellow", "purple", "lavender", "cyan"]
        colors = []
        last_seven_dates = []
        last_seven_usage = []
        if len(dates) > 7:
            dates.reverse()
            time_spent.reverse()
            for i in dates:
                last_seven_dates.append(i)
                last_seven_usage.append(time_spent[dates.index(i)])
                if dates.index(i) == 6:
                    break
        else:
            last_seven_dates = dates
            last_seven_usage = time_spent
        last_seven_dates.reverse()
        last_seven_usage.reverse()
        for i in last_seven_dates:
            k = random.randint(0, 7)
            colors.append(colors_lib[k])
        if len(last_seven_dates) < 2:
            tkinter.messagebox.showwarning("Error", "No sufficient data!")
        if not test:
            plt.bar(last_seven_dates, last_seven_usage, width=0.5, color=colors)
            plt.plot(last_seven_dates, last_seven_usage)
            plt.yticks(np.arange(0, (5 + max(last_seven_usage)), 10))
            for a, b in zip(last_seven_dates, last_seven_usage):
                plt.text(a, b, str(b), fontsize=15)
            if len(last_seven_dates) > 1:
                plt.show()
        if test:
            return True