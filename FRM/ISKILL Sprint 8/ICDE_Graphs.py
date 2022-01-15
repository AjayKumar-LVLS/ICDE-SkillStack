import matplotlib.pyplot as plt
import random
import numpy as np
import tkinter
from tkinter import messagebox


class Graphs():
    # This method will plot the course rankings
    def plot_course_ranks(self, df, stream):
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
        plt.bar(courses, ranks_courses, width=0.5, color=colors)
        plt.yticks(np.arange(0, (2 + max(ranks_courses)), 1))
        for a, b in zip(courses, ranks_courses):
            plt.text(a, b, str(b), fontsize=15)
        plt.show()

    # This method will plot the usage stasts
    def plot_usage_stats(self, df, name):
        dates = df.columns.values.tolist()
        df_time = df.values.tolist()
        time_spent = df_time[0]
        plt.xlabel("Date", fontsize=15)
        plt.ylabel("Time spent in minutes", fontsize=15)
        title = str(name) + "'s usage stats"
        plt.title(title, fontsize=18)
        colors_lib = ["blue", "green", "red", "orange", "yellow", "purple", "lavender", "cyan"]
        colors = []
        for i in dates:
            k = random.randint(0, 7)
            colors.append(colors_lib[k])
        if len(dates) < 2:
            tkinter.messagebox.showwarning("Error", "No sufficient data!")
        else:
            plt.bar(dates, time_spent, width=0.5, color=colors)
            plt.plot(dates, time_spent)
            plt.yticks(np.arange(0, (5 + max(time_spent)), 10))
            for a, b in zip(dates, time_spent):
                plt.text(a, b, str(b), fontsize=15)
            plt.show()
