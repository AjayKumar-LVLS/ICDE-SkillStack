import tkinter as tk
from tkinter import messagebox
import bcrypt
from ICDE_APPCORE import Data_Verification, IcdeAppCore
from datetime import date
from pymongo import MongoClient
from ICDE_DataBase import IcdeDataBase

# Turn this variable to True if login details were verified with those in DataBase.
login_data_validated = False
PwReset_data_validation = False
global current_user, selected_course, selected_stream

cluster = MongoClient("mongodb+srv://somesh:icdeskillstack@cluster0.odqp5.mongodb.net/myFirstDatabase?retryWrites"
                      "=true&w=majority")
db = cluster["ICDE_DataBase"]
collection = db["ICDE_Collection"]


# Provide functionalities to frames.
# noinspection PyMethodMayBeStatic
class Functionalities(tk.Tk, Data_Verification):
    def __init__(self):
        super().__init__()
        global login_data_validated, PwReset_data_validation
        login_data_validated = False
        PwReset_data_validation = False

    def show_frame(self, frame):
        frame.tkraise()

    def exit_app(self):
        self.destroy()

    def refresh(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # To validate the details entered by user at login page
    def login_data_validation(self, username, password):
        global login_data_validated
        login_data_validated = False

        flag_authorise = self.VerifyUser(username, password)

        if username == "" and password == "":
            tk.messagebox.showwarning("Error", "Input fields can not be empty")
        elif username == "":
            tk.messagebox.showwarning("Error", "Username can not be empty")
        elif password == "":
            tk.messagebox.showwarning("Error", "Password can not be empty")
        elif "@" not in username.lower() or ".com" not in username.lower():
            tk.messagebox.showwarning("Error", "Please enter a valid email address")
        # Create another elif condition here to contact with DataBase and validate login credentials.
        elif flag_authorise:
            tk.messagebox.showinfo("Message prompt", "Login is successful")
            self.show_frame(self.main_frame)
        elif not flag_authorise:
            tk.messagebox.showwarning("Error", "Wrong Password/Email not registered")
        else:
            tk.messagebox.showwarning("Error", "No account found with this email address, please signup")

    # To validate the details entered by user at registration page
    def signup_data_validation(self, firstname, lastname, username, phone_number, password, reentered_password, gender,
                               stream, date_of_birth):
        error_shown = False
        if firstname == "" or lastname == "" or username == "" or phone_number == "" or password == "" or reentered_password == "" or date_of_birth == "" or gender == 0 or stream == "Select your Stream":
            tk.messagebox.showwarning("Error", "Fields can not be empty")
            error_shown = True
        if not error_shown:
            for i in firstname:
                if ord(i) < 65 or ord(i) > 122:
                    if ord(i) == 32:
                        continue
                    else:
                        tk.messagebox.showwarning("Error", "Invalid first name")
                        error_shown = True
                if 90 < ord(i) < 97:
                    tk.messagebox.showwarning("Error", "Invalid first name")
                    error_shown = True
        if not error_shown:
            for i in lastname:
                if ord(i) < 65 or ord(i) > 122:
                    if ord(i) == 32:
                        continue
                    else:
                        tk.messagebox.showwarning("Error", "Invalid last name")
                        error_shown = True
                if 90 < ord(i) < 97:
                    tk.messagebox.showwarning("Error", "Invalid last name")
                    error_shown = True
        if not error_shown:
            if "@" not in username.lower() or ".com" not in username.lower():
                tk.messagebox.showwarning("Error", "Email invalid")
                error_shown = True
        if not error_shown:
            if password != reentered_password:
                tk.messagebox.showwarning("Error", "Passwords not matching")
                error_shown = True
        if not error_shown:
            if len(phone_number) != 10:
                tk.messagebox.showwarning("Error", "Invalid mobile number")
                error_shown = True
        if not error_shown:
            for i in phone_number:
                if ord(i) < 48 or ord(i) > 57:
                    tk.messagebox.showwarning("Error", "Invalid mobile number")
                    error_shown = True
        if not error_shown:
            if len(date_of_birth) != 10:
                tk.messagebox.showwarning("Error", "Invalid DOB")
                error_shown = True
        if not error_shown:
            for i in date_of_birth[0:4]:
                if ord(i) < 48 or ord(i) > 57:
                    tk.messagebox.showwarning("Error", "Invalid DOB")
                    error_shown = True
        if not error_shown:
            for i in date_of_birth[5:7]:
                if ord(i) < 48 or ord(i) > 57:
                    tk.messagebox.showwarning("Error", "Invalid DOB")
                    error_shown = True
        if not error_shown:
            for i in date_of_birth[8:10]:
                if ord(i) < 48 or ord(i) > 57:
                    tk.messagebox.showwarning("Error", "Invalid DOB")
                    error_shown = True
        if not error_shown:
            if (int(date_of_birth[0:4]) > date.today().year) or (int(date_of_birth[5:7]) > 12) or (
                    int(date_of_birth[8:10]) > 31):
                tk.messagebox.showwarning("Error", "Invalid DOB")
                error_shown = True
        if not error_shown:
            profile_created = IcdeAppCore.createProfile(self, firstname, lastname, username, phone_number, password,
                                                        reentered_password, gender,
                                                        stream, date_of_birth)
            if profile_created:
                tk.messagebox.showinfo("Message", "SignUp Success, please login.")
                self.show_frame(self.home_frame)
            else:
                tk.messagebox.showwarning("Error", "Email id already registered!")

    # Verify Security question
    def PwReset_data_validation(self, Email, DOB, new_pw, con_new_pw):
        error_shown = False
        if Email == "" or DOB == "" or new_pw == "" or con_new_pw == "":
            tk.messagebox.showwarning("Error", "Input fields can not be empty")
            error_shown = True
        if not error_shown:
            if new_pw != con_new_pw:
                tk.messagebox.showwarning("Error", "Passwords not matching")
                error_shown = True
        if not error_shown:
            if len(DOB) != 10:
                tk.messagebox.showwarning("Error", "Invalid DOB")
                error_shown = True
        if not error_shown:
            for i in DOB[0:4]:
                if ord(i) < 48 or ord(i) > 57:
                    tk.messagebox.showwarning("Error", "Invalid DOB")
                    error_shown = True
        if not error_shown:
            for i in DOB[5:7]:
                if ord(i) < 48 or ord(i) > 57:
                    tk.messagebox.showwarning("Error", "Invalid DOB")
                    error_shown = True
        if not error_shown:
            for i in DOB[8:10]:
                if ord(i) < 48 or ord(i) > 57:
                    tk.messagebox.showwarning("Error", "Invalid DOB")
                    error_shown = True
        if not error_shown:
            if (int(DOB[0:4]) > date.today().year) or (int(DOB[5:7]) > 12) or (
                    int(DOB[8:10]) > 31):
                tk.messagebox.showwarning("Error", "Invalid DOB")
                error_shown = True
        if not error_shown:
            if collection.find_one({"Email": Email}) is None:
                tk.messagebox.showwarning("Error", "No account associated with this Email address")
            else:
                flag_pwreset = Data_Verification.VerifySeqQn(self, Email, DOB)
                if flag_pwreset:
                    IcdeDataBase.update_pw_db(self, Email, new_pw)
                    tk.messagebox.showinfo("Message prompt", "Password reset is successful")
                    self.show_frame(self.login_frame)
                else:
                    tk.messagebox.showwarning("Error", "Security check failed, try again!")

    def enroll(self, user, course):
        not_enrolled = IcdeAppCore.check_enrollement(self, user, course)
        if not_enrolled:
            IcdeDataBase.add_course_db(self, user, course)
            tk.messagebox.showinfo("Message prompt", "Course enrolled succesfully")
        else:
            tk.messagebox.showwarning("Error", "Course already enrolled!")

    def drop(self, user, course):
        not_enrolled = IcdeAppCore.check_enrollement(self, user, course)
        if not_enrolled:
            tk.messagebox.showwarning("Error", "You have not enrolled to this course!")
        else:
            IcdeDataBase.drop_course_db(self, user, course)
            tk.messagebox.showinfo("Message prompt", "Course dropped from your course cart")

    def logCourse(self, course):
        global selected_course
        selected_course = course
        print(selected_course)

    def loguser(self, user):
        global current_user
        current_user = user
        print(current_user)

    def logStream(self, stream):
        global selected_stream
        selected_stream = stream
        print(selected_stream)


# To Initialization the main window
class Initialization(tk.Tk):
    def __init__(self):
        super().__init__()

    window_title = "ICDE - [Skill Stack]"
    window_size = "800x700"

    def setup(self):
        self.title(self.window_title)
        self.geometry(self.window_size)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Creating different frames in application
        self.home_frame = tk.Frame(self)
        self.login_frame = tk.Frame(self)
        self.signup_frame = tk.Frame(self)
        self.passwordReset_frame = tk.Frame(self)
        self.main_frame = tk.Frame(self)
        self.enroll_drop_frame = tk.Frame(self)
        self.tec_course_page = tk.Frame(self)
        self.gen_course_select_frame = tk.Frame(self)
        self.tec_course_select_frame = tk.Frame(self)
        self.nontec_course_select_frame = tk.Frame(self)
        self.elec_course_select_frame = tk.Frame(self)
        self.electro_course_select_frame = tk.Frame(self)
        self.comp_course_select_frame = tk.Frame(self)
        self.civil_course_select_frame = tk.Frame(self)
        self.mech_course_select_frame = tk.Frame(self)


# To validate the input data entered by user
# noinspection PyMethodMayBeStatic
# class DataValidation:


# This is the main class
# noinspection SpellCheckingInspection
class ICDEUser(Initialization, Functionalities):
    def __init__(self):
        super().__init__()
        super().setup()

        # global current_user, selected_course

        # Inserting widgets in different frames
        # home_frame widgets starts here
        def homepage():
            tk.Label(self.home_frame, text="ICDE - [Skill Stack]", width=100, font="bold, 30", bg="SkyBlue1",
                     fg="DodgerBlue4",
                     height=2).pack()

            tk.Label(self.home_frame, text="", height=2).pack()
            tk.Label(self.home_frame, text="Please choose from the following", font="helvetica, 18").pack()

            tk.Label(self.home_frame, text="", height=3).pack()
            tk.Button(self.home_frame, text="Sign-Up", width=30, bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.refresh(self.signup_frame), registrationpage(),
                                       self.show_frame(self.signup_frame)]).pack()

            tk.Label(self.home_frame, text="", height=1).pack()
            tk.Button(self.home_frame, text="Sign-In", width=30, bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.refresh(self.login_frame), loginpage(),
                                       self.show_frame(self.login_frame)]).pack()

            # tk.Label(self.home_frame, text="", height=1).pack()
            # tk.Button(self.home_frame, text="Exit", width=30, bg="black", fg="white", font="helvetica, 12",
            #           command=lambda: [self.exit_app()]).pack()

        # self.signup_frame widgets starts here
        # noinspection PyUnusedLocal
        def registrationpage():
            self.refresh(self.signup_frame)
            tk.Label(self.signup_frame, text="Please Enter Registration Details", width=100,
                     font=("Papyrus", 20, "bold"),
                     bg="SkyBlue1", fg="DodgerBlue4",
                     height=2).pack()
            tk.Label(self.signup_frame, text="First Name", width=20, font=("bold", 12)).place(x=80, y=100)
            firstname_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12))
            firstname_entry.place(x=240, y=100)
            tk.Label(self.signup_frame, text="Last Name", width=20, font=("bold", 12)).place(x=80, y=150)
            lastname_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12))
            lastname_entry.place(x=240, y=150)
            tk.Label(self.signup_frame, text="Email", width=20, font=("bold", 12)).place(x=68, y=200)
            email_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12))
            email_entry.place(x=240, y=200)
            tk.Label(self.signup_frame, text="Password", width=20, font=("bold", 12)).place(x=80, y=250)
            passowrd_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12), show='*')
            passowrd_entry.place(x=240, y=250)
            # Password hashing
            hashed_pw = lambda: [self.PwHashing(passowrd_entry.get())]

            tk.Label(self.signup_frame, text="Re-enter Password", width=20, font=("bold", 12)).place(x=50, y=300)
            repassowrd_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12), show='*')
            repassowrd_entry.place(x=240, y=300)
            tk.Label(self.signup_frame, text="Mobile Number", width=20, font=("bold", 12)).place(x=50, y=350)
            phone_number = tk.Entry(self.signup_frame, width=25, font=("bold", 12))
            phone_number.place(x=240, y=350)
            tk.Label(self.signup_frame, text="Date of birth (YYYY-MM-DD)", width=25, font=("bold", 12)).place(x=5,
                                                                                                              y=400)
            date_of_birth = tk.Entry(self.signup_frame, width=25, font=("bold", 12))
            date_of_birth.place(x=240, y=400)
            label_4 = tk.Label(self.signup_frame, text="Gender", width=20, font=("bold", 12))
            label_4.place(x=70, y=450)

            gen_var = tk.IntVar()
            tk.Radiobutton(self.signup_frame, text="Male", variable=gen_var, value=1, font=("bold", 12)).place(x=235,
                                                                                                               y=450)
            tk.Radiobutton(self.signup_frame, text="Female", variable=gen_var, value=2, font=("bold", 12)).place(x=310,
                                                                                                                 y=450)

            tk.Label(self.signup_frame, text="Stream", width=20, font=("bold", 12)).place(x=70, y=500)

            # Add more branches here to appear in the dropdown list in signup page
            list_of_streams = ['Electrical Engineering', 'Computer Engineering', 'Electronics Engineering',
                               'Mechanical Engineering', 'Civil Engineering']

            stream = tk.StringVar()
            stream_list = tk.OptionMenu(self.signup_frame, stream, *list_of_streams)
            stream_list.config(width=20, font=("bold", 12))
            stream.set('Select your Stream')
            stream_list.place(x=240, y=500)
            #
            tk.Button(self.signup_frame, text='Submit', width=20, bg="SteelBlue2", fg='white', font=("bold", 12),
                      command=lambda: [
                          self.signup_data_validation(firstname_entry.get(), lastname_entry.get(), email_entry.get(),
                                                      phone_number.get(), passowrd_entry.get(), repassowrd_entry.get(),
                                                      gen_var.get(), stream.get(), date_of_birth.get())]).place(x=180,
                                                                                                                y=550)
            tk.Button(self.signup_frame, text="Back to Home page", width=20, bg="SteelBlue3", fg='white',
                      font=("bold", 12),
                      command=lambda: self.show_frame(self.home_frame)).place(x=180, y=600)

        # Login_frame widgets starts here
        def loginpage():
            self.refresh(self.login_frame)
            tk.Label(self.login_frame, text="Please Enter Login Credetails", width=100, font=("Papyrus", 30, "bold"),
                     bg="SkyBlue1", fg="DodgerBlue4",
                     height=2).pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Label(self.login_frame, text="Username", font=("Cooper Black", 12)).pack()
            username_entry = tk.Entry(self.login_frame, textvariable="username", width=40, font="helvetica, 12")
            username_entry.pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Label(self.login_frame, text="Password", font=("Cooper Black", 12)).pack()
            password_entry = tk.Entry(self.login_frame, textvariable="password", width=40, font="helvetica, 12",
                                      show='*')
            password_entry.pack()

            # Enable this to do not autofill password for returning users
            password_entry.delete(0, 'end')

            tk.Label(self.login_frame, text="").pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Button(self.login_frame, text="Login", width=30, height=1, bg="SteelBlue1", font=("Cooper Black", 12),
                      command=lambda: [self.login_data_validation(username_entry.get(), password_entry.get()),
                                       self.loguser(username_entry.get())]).pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Button(self.login_frame, text="Forgot Password", width=30, height=1, bg="SteelBlue2",
                      font=("Cooper Black", 12),
                      command=lambda: [self.refresh(self.passwordReset_frame), passwordResetFrame(),
                                       self.show_frame(self.passwordReset_frame)]).pack()
            tk.Label(self.login_frame, text="").pack()

            tk.Button(self.login_frame, text="Back to Home page", width=30, bg="Steelblue3", font=("Cooper Black", 12),
                      command=lambda: [self.show_frame(self.home_frame)]).pack()

        # self.passwordReset_frame widgets start here
        def passwordResetFrame():
            self.refresh(self.passwordReset_frame)
            tk.Label(self.passwordReset_frame, text="Password Reset Page", font="helvetica, 20").place(x=300, y=40)
            tk.Label(self.passwordReset_frame, text="").pack()
            tk.Label(self.passwordReset_frame, text="E-mail", font="helvetica, 10").place(x=60, y=160)
            Email_entry = tk.Entry(self.passwordReset_frame, width=40, font=("bold", 12))
            Email_entry.place(x=270, y=160)
            tk.Label(self.passwordReset_frame, text="Enter your D.O.B (YYYY-MM-DD)", font="helvetica, 10").place(x=60,
                                                                                                                 y=220)
            DOB_entry = tk.Entry(self.passwordReset_frame, width=40, font=("bold", 12))
            DOB_entry.place(x=270, y=220)
            tk.Label(self.passwordReset_frame, text="New Password", font="helvetica, 10").place(x=60, y=280)
            New_Password = tk.Entry(self.passwordReset_frame, width=40, font=("bold", 12), show='*')
            New_Password.place(x=270, y=280)
            hashed_pw = lambda: [self.PwHashing(New_Password.get())]

            tk.Label(self.passwordReset_frame, text="Confirm Password", font="helvetica, 10").place(x=60, y=340)
            Confirm_password = tk.Entry(self.passwordReset_frame, width=40, font=("bold", 12), show='*')
            Confirm_password.place(x=270, y=340)
            self.PwReset = tk.Button(self.passwordReset_frame, text='Submit', width=20, bg="black", fg='white',
                                     font=("bold", 12),
                                     command=lambda: [self.PwReset_data_validation(Email_entry.get(), DOB_entry.get(),
                                                                                   New_Password.get(),
                                                                                   Confirm_password.get())])
            self.PwReset.place(x=240, y=450)
            self.back_button = tk.Button(self.passwordReset_frame, text='Go Back', width=20, bg="black", fg='white',
                                         font=("bold", 12),
                                         command=lambda: [self.show_frame(self.login_frame)])
            self.back_button.place(x=240, y=500)

        def AppMainPage():
            self.refresh(self.main_frame)
            Stream = ["General_courses", "Technical Courses", "NonTech_courses"]
            tk.Label(self.main_frame, text="Application Main Page", width=100, font=("TrebuchetMS", 30, "bold"),
                     bg="SkyBlue1", fg="DodgerBlue4",
                     height=2).pack()
            tk.Label(self.main_frame, text="").pack()
            tk.Button(self.main_frame, text=Stream[0], width=30, bg="pale turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.gen_course_select_frame),self.logStream(Stream[0])]).place(x=270, y=120)
            tk.Button(self.main_frame, text=Stream[1], width=30, bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.tec_course_page)]).place(x=270, y=160)
            tk.Button(self.main_frame, text=Stream[2], width=30, bg="dark turquoise",
                      font="helvetica, 12",
                      command=lambda: [self.show_frame(self.nontec_course_select_frame),self.logStream(Stream[2])]).place(x=270, y=200)

        # Creating Enrollment and Drop Page
        def EnrollmentPage():
            global current_user, selected_course
            tk.Label(self.enroll_drop_frame, text="Enrollment / Drop Page", width=100, font="bold, 30", bg="SkyBlue1",
                     fg="DodgerBlue4",
                     height=2).pack()
            tk.Label(self.enroll_drop_frame, text="").pack()
            tk.Button(self.enroll_drop_frame, text="Enroll", width=30, bg="yellow green", font="helvetica, 12",
                      command=lambda: [self.enroll(current_user, selected_course), IcdeDataBase.add_course_user(self, current_user, selected_stream, selected_course)]).place(x=270, y=120)
            tk.Button(self.enroll_drop_frame, text="Drop", width=30, bg="indian red", font="helvetica, 12",
                      command=lambda: [self.drop(current_user, selected_course),IcdeDataBase.remove_course_user(self, current_user, selected_stream, selected_course)]).place(x=270, y=160)
            tk.Button(self.enroll_drop_frame, text="<-- Back", width=10, bg="light blue", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.main_frame)]).place(x=330, y=200)

        def Teccoursepage():
            tk.Label(self.tec_course_page, text="Technical Course Branches", width=100, font="bold, 30", bg="SkyBlue1",
                     fg="DodgerBlue4",
                     height=2).pack()
            Stream = ["Electrical Engineering", "Electronics Engineering", "Computer Engineering", "Civil Engineering",
                      "Mechanical Engineering", ]
            tk.Button(self.tec_course_page, text=Stream[0], width=30, bg="SteelBlue1",
                      font="Trebuchet, 12",
                      command=lambda: [self.show_frame(self.tec_course_page),
                                       self.show_frame(self.elec_course_select_frame), self.logStream(Stream[0])]).place(x=270, y=120)
            tk.Button(self.tec_course_page, text=Stream[1], width=30, bg="SteelBlue2",
                      font="helvetica, 12", command=lambda: [self.show_frame(self.tec_course_page),
                                                             self.show_frame(self.electro_course_select_frame), self.logStream(Stream[1])]).place(
                x=270, y=160)
            tk.Button(self.tec_course_page, text=Stream[2], width=30, bg="SteelBlue3",
                      font="helvetica, 12", command=lambda: [self.show_frame(self.tec_course_page),
                                                             self.show_frame(self.comp_course_select_frame), self.logStream(Stream[2])]).place(
                x=270, y=200)
            tk.Button(self.tec_course_page, text=Stream[3], width=30, bg="SteelBlue3",
                      font="helvetica, 12", command=lambda: [self.show_frame(self.tec_course_page),
                                                             self.show_frame(self.civil_course_select_frame), self.logStream(Stream[3])]).place(
                x=270, y=240)
            tk.Button(self.tec_course_page, text=Stream[4], width=30, bg="SteelBlue3",
                      font="helvetica, 12", command=lambda: [self.show_frame(self.tec_course_page),
                                                             self.show_frame(self.mech_course_select_frame), self.logStream(Stream[4])]).place(
                x=270, y=280)
            tk.Button(self.tec_course_page, text="<-- Back", width=10, bg="light blue", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.main_frame)]).place(x=350, y=380)

        def Courseselection():
            global selected_course,selected_stream,current_user

            # Displaying General Workshops
            tk.Label(self.gen_course_select_frame, text="General_courses", width=100, font="bold, 30", bg="SkyBlue1",
                     fg="DodgerBlue4",
                     height=2).pack()

            General_courses = ["Spark! Articulate and Communicate your skills",
                               "Essential Soft Skills for Career Success",
                               "Guide to Entreprenuership",
                               "Practicing Agility- Lean Start-Up and SCRUM Basics",
                               "Library Skills & Resources- Maximize Your Graduate Research Potential",
                            ]

            tk.Button(self.gen_course_select_frame, text=General_courses[0], width=80,
                      bg="SteelBlue1", font="helvetica, 12", command=lambda: [self.show_frame(self.enroll_drop_frame),
                                                                              self.logCourse(
                                                                                  General_courses[0])]).place(x=270,
                                                                                                              y=120)

            tk.Button(self.gen_course_select_frame, text=General_courses[1], width=80,
                      bg="SteelBlue2", font="helvetica, 12", command=lambda: [self.show_frame(self.enroll_drop_frame),
                                                                              self.logCourse(
                                                                                  General_courses[1])]).place(x=270,
                                                                                                              y=160)

            tk.Button(self.gen_course_select_frame, text=General_courses[2], width=80, bg="SteelBlue3",
                      font="helvetica, 12", command=lambda: [self.show_frame(self.enroll_drop_frame),
                                                             self.logCourse(General_courses[2])]).place(x=270, y=200)

            tk.Button(self.gen_course_select_frame, text=General_courses[3], width=80, bg="SteelBlue4",
                      font="helvetica, 12", command=lambda: [self.show_frame(self.enroll_drop_frame),
                                                             self.logCourse(General_courses[3])]).place(x=270, y=240)

            tk.Button(self.gen_course_select_frame, text=General_courses[4], width=80, bg="DodgerBlue4",
                      font="helvetica, 12", command=lambda: [self.show_frame(self.enroll_drop_frame),
                                                             self.logCourse(General_courses[4])]).place(x=270, y=280)

            tk.Button(self.gen_course_select_frame, text="<-- Back", width=10, bg="light blue", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.main_frame)]).place(x=550, y=400)
            tk.Button(self.gen_course_select_frame, text= "Course analysis", width=80,
                      bg="SteelBlue1", font="helvetica, 12",command = lambda :[IcdeDataBase.collect_user_data(self, current_user, selected_stream)]).place(x=270,y=340)

            # ***********************************************************************************************************************************
            # Displaying Technical courses
            # Electrical Engineering
            Electrical_courses = ["EE1:Electrical Power Engineering Principles",
                                  "EE2:Power Engineering-Power system Analysis",
                                  "EE3:Electrical Control & Protection Systems",
                                  "EE4:Electrical Power Equipment",
                                  "EE5:Distribution Power Engineering Fundamentals"]

            tk.Label(self.elec_course_select_frame, text="Electrical Engineering Courses", width=100,
                     font="bold, 30", bg="SkyBlue1", fg="DodgerBlue4", height=2).pack()
            tk.Button(self.elec_course_select_frame, text=Electrical_courses[0], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electrical_courses[0])]).place(x=270, y=120)

            tk.Button(self.elec_course_select_frame, text=Electrical_courses[1], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electrical_courses[1])]).place(x=270, y=160)

            tk.Button(self.elec_course_select_frame, text=Electrical_courses[2], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electrical_courses[2])]).place(x=270, y=200)

            tk.Button(self.elec_course_select_frame, text=Electrical_courses[3],
                      width=80, bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electrical_courses[3])]).place(x=270, y=240)

            tk.Button(self.elec_course_select_frame, text=Electrical_courses[4], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electrical_courses[4])]).place(x=270, y=280)

            tk.Button(self.elec_course_select_frame, text="<-- Back", width=10, bg="light blue", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.tec_course_page)]).place(x=550, y=400)
            tk.Button(self.elec_course_select_frame, text="Course analysis", width=80,
                      bg="SteelBlue1", font="helvetica, 12",
                      command=lambda: [IcdeDataBase.collect_user_data(self, current_user, selected_stream)]).place( x=270, y=340)

            # Electronics Engineering
            Electronics_courses = ["EC1:Digital Electronics & Logic Design",
                                   "EC2:Arduino Programming and Hardware Fundamentals with Hackster",
                                   "EC3:Industrial Robotics",
                                   "EC4:Computer architecture and Design",
                                   "EC5:Functional Hardware Verification"]

            tk.Label(self.electro_course_select_frame, text="Electronics Engineering Courses", width=100,
                     font="bold, 30", bg="SkyBlue1", fg="DodgerBlue4", height=2).pack()

            tk.Button(self.electro_course_select_frame, text=Electronics_courses[0], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electronics_courses[0])]).place(x=270, y=120)

            tk.Button(self.electro_course_select_frame, text=Electronics_courses[1], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electronics_courses[1])]).place(x=270, y=160)

            tk.Button(self.electro_course_select_frame, text=Electronics_courses[2], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electronics_courses[2])]).place(x=270, y=200)

            tk.Button(self.electro_course_select_frame, text=Electronics_courses[3], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electronics_courses[3])]).place(x=270, y=240)

            tk.Button(self.electro_course_select_frame, text=Electronics_courses[4], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Electronics_courses[4])]).place(x=270, y=280)

            tk.Button(self.electro_course_select_frame, text="<-- Back", width=10, bg="light blue",
                      font="helvetica, 12",
                      command=lambda: [self.show_frame(self.tec_course_page)]).place(x=550, y=400)
            tk.Button(self.electro_course_select_frame, text="Course analysis", width=80,
                      bg="SteelBlue1", font="helvetica, 12",
                      command=lambda: [IcdeDataBase.collect_user_data(self, current_user, selected_stream)]).place(x=270, y=340)

            # Computer Engineering
            Computer_courses = ["CE1:Learning Python Programming Masterclass",
                                "CE2:C Programming for Beginners",
                                "CE3:Machine Learning",
                                "CE4:Mastering Data Structures and Algorithms",
                                "CE5:Ultimate AWS Certified Solutions Architect"]

            tk.Label(self.comp_course_select_frame, text="Computer Engineering Courses", width=100, font="bold, 30",
                     bg="SkyBlue1",
                     fg="DodgerBlue4",
                     height=2).pack()

            tk.Button(self.comp_course_select_frame, text=Computer_courses[0], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Computer_courses[0])]).place(x=270, y=120)

            tk.Button(self.comp_course_select_frame, text=Computer_courses[1], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Computer_courses[1])]).place(x=270, y=160)

            tk.Button(self.comp_course_select_frame, text=Computer_courses[2], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Computer_courses[2])]).place(x=270, y=200)

            tk.Button(self.comp_course_select_frame, text=Computer_courses[3], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Computer_courses[3])]).place(x=270, y=240)

            tk.Button(self.comp_course_select_frame, text=Computer_courses[4], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Computer_courses[4])]).place(x=270, y=280)

            tk.Button(self.comp_course_select_frame, text="<-- Back", width=10, bg="light blue", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.tec_course_page)]).place(x=550, y=400)
            tk.Button(self.comp_course_select_frame, text="Course analysis", width=80,
                      bg="SteelBlue1", font="helvetica, 12",
                      command=lambda: [IcdeDataBase.collect_user_data(self, current_user, selected_stream)]).place(x=270, y=340)

            # Civil Engineering
            Civil_courses = ["CE1:Structural Engineering",
                             "CE2:Mastering AUTOCAD",
                             "CE3:Architecture",
                             "CE4:Soil Testing",
                             "CE5:Concrete Technology"]

            tk.Label(self.civil_course_select_frame, text="Civil Engineering Courses", width=100, font="bold, 30",
                     bg="SkyBlue1",
                     fg="DodgerBlue4",
                     height=2).pack()

            tk.Button(self.civil_course_select_frame, text=Civil_courses[0], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Civil_courses[0])]).place(x=270, y=120)

            tk.Button(self.civil_course_select_frame, text=Civil_courses[1], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Civil_courses[1])]).place(x=270, y=160)

            tk.Button(self.civil_course_select_frame, text=Civil_courses[2], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Civil_courses[2])]).place(x=270, y=200)

            tk.Button(self.civil_course_select_frame, text=Civil_courses[3], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Civil_courses[3])]).place(x=270, y=240)

            tk.Button(self.civil_course_select_frame, text=Civil_courses[4], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Civil_courses[4])]).place(x=270, y=280)

            tk.Button(self.civil_course_select_frame, text="<-- Back", width=10, bg="light blue", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.tec_course_page)]).place(x=550, y=400)
            tk.Button(self.civil_course_select_frame, text="Course analysis", width=80,
                      bg="SteelBlue1", font="helvetica, 12",
                      command=lambda: [IcdeDataBase.collect_user_data(self, current_user, selected_stream)]).place( x=270, y=340)

            # Mechanical Engineering
            Mechanical_courses = ["ME1:Fluid Mechanics",
                                  "ME2:Applied Thermodynamics",
                                  "ME3:Heat and Mass Transfer",
                                  "ME4:Design of Machine Elements",
                                  "ME5:Dynamics of Machinery"]

            tk.Label(self.mech_course_select_frame, text="Mechanical Engineering Courses", width=100, font="bold, 30",
                     bg="SkyBlue1",
                     fg="DodgerBlue4",
                     height=2).pack()

            tk.Button(self.mech_course_select_frame, text=Mechanical_courses[0], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Mechanical_courses[0])]).place(x=270, y=120)

            tk.Button(self.mech_course_select_frame, text=Mechanical_courses[1], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Mechanical_courses[1])]).place(x=270, y=160)

            tk.Button(self.mech_course_select_frame, text=Mechanical_courses[2], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Mechanical_courses[2])]).place(x=270, y=200)

            tk.Button(self.mech_course_select_frame, text=Mechanical_courses[3], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Mechanical_courses[3])]).place(x=270, y=240)

            tk.Button(self.mech_course_select_frame, text=Mechanical_courses[4], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(Mechanical_courses[4])]).place(x=270, y=280)

            tk.Button(self.mech_course_select_frame, text="<-- Back", width=10, bg="light blue", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.tec_course_page)]).place(x=550, y=400)
            tk.Button(self.mech_course_select_frame, text="Course analysis", width=80,
                      bg="SteelBlue1", font="helvetica, 12",
                      command=lambda: [IcdeDataBase.collect_user_data(self, current_user, selected_stream)]).place(x=270, y=340)

            # ***********************************************************************************************************************************

            # Displaying Non-Technical Workshops
            NonTech_courses = ["French language",
                               "English proficiency",
                               "Communication Skills",
                               "Softskills",
                               "Creativity,Innovation"]
            tk.Label(self.nontec_course_select_frame, text="NonTech_courses", width=100, font="bold, 30",
                     bg="SkyBlue1", fg="DodgerBlue4", height=2).pack()

            tk.Button(self.nontec_course_select_frame, text=NonTech_courses[0], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(NonTech_courses[0])]).place(x=270, y=120)

            tk.Button(self.nontec_course_select_frame, text=NonTech_courses[1], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(NonTech_courses[1])]).place(x=270, y=160)

            tk.Button(self.nontec_course_select_frame, text=NonTech_courses[2], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(NonTech_courses[2])]).place(x=270, y=200)

            tk.Button(self.nontec_course_select_frame, text=NonTech_courses[3], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(NonTech_courses[3])]).place(x=270, y=240)

            tk.Button(self.nontec_course_select_frame, text=NonTech_courses[4], width=80,
                      bg="medium turquoise", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.enroll_drop_frame),
                                       self.logCourse(NonTech_courses[4])]).place(x=270, y=280)

            tk.Button(self.nontec_course_select_frame, text="<-- Back", width=10, bg="light blue", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.main_frame)]).place(x=550, y=400)
            tk.Button(self.nontec_course_select_frame, text="Course analysis", width=80,
                      bg="SteelBlue1", font="helvetica, 12",
                      command=lambda: [IcdeDataBase.collect_user_data(self, current_user, selected_stream)]).place(x=270, y=340)

        homepage()
        registrationpage()
        loginpage()
        passwordResetFrame()
        AppMainPage()
        Courseselection()
        EnrollmentPage()
        Teccoursepage()
        for frame in (self.home_frame, self.login_frame, self.signup_frame, self.passwordReset_frame, self.main_frame,
                      self.gen_course_select_frame,
                      self.tec_course_select_frame, self.nontec_course_select_frame, self.enroll_drop_frame,
                      self.tec_course_page, self.elec_course_select_frame,
                      self.electro_course_select_frame, self.comp_course_select_frame, self.civil_course_select_frame,
                      self.mech_course_select_frame):
            frame.grid(row=0, column=0, sticky="nsew")
        super().show_frame(self.home_frame)


root = ICDEUser()
root.mainloop()
