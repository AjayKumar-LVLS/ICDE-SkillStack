import tkinter as tk
from tkinter import messagebox
import bcrypt
from ICDE_APPCORE import Data_Verification

# Turn this variable to True if login details were verified with those in DataBase.
login_data_validated = False
PwReset_data_validation = False

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
        elif "@" not in username or ".com" not in username:
            tk.messagebox.showwarning("Error", "Please enter a valid email address")
        # Create another elif condition here to contact with DataBase and validate login credentials.
        elif flag_authorise:
            tk.messagebox.showinfo("Message promt", "Login is succesfull")
            self.show_frame(self.main_frame)
        elif (not flag_authorise):
            tk.messagebox.showwarning("Error", "Wrong Password")
        else:
            tk.messagebox.showwarning("Error", "No account found with this email address, please signup")

    # To validate the details entered by user at registration page
    def signup_data_validation(self, firstname, lastname, username, phone_number, password, reentered_password, gender,
                               stream, date_of_birth):
        pass

    # Verify Security question
    def PwReset_data_validation(self, Email, DOB):
        """user_DOB = users.find({
            "E-mail" : Email
        })[0]["DOB"]"""

        flag_pwreset = self.VerifySeqQn(Email, DOB)

        if flag_pwreset:
            tk.messagebox.showinfo("Message promt", "Password reset is succesfull")
            self.show_frame(self.login_frame)
        else:
            tk.messagebox.showwarning("Error", "DOB not matching")


# To Initialization the main window
class Initialization(tk.Tk):
    def __init__(self):
        super().__init__()

    def setup(self):
        self.title("ICDE - [Skill Stack]")
        self.geometry("800x700")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Creating different frames in application
        self.home_frame = tk.Frame(self)
        self.login_frame = tk.Frame(self)
        self.signup_frame = tk.Frame(self)
        self.passwordReset_frame = tk.Frame(self)
        self.main_frame = tk.Frame(self)


# To validate the input data entered by user
# noinspection PyMethodMayBeStatic
# class DataValidation:


# This is the main class
# noinspection SpellCheckingInspection
class Icde(Initialization, Functionalities):
    def __init__(self):
        super().__init__()
        super().setup()

        # Inserting widgets in different frames
        # home_frame widgets starts here
        def homepage():
            tk.Label(self.home_frame, text="ICDE - [Skill Stack]", width=100, font="bold, 30", bg="black", fg="white",
                     height=2).pack()

            tk.Label(self.home_frame, text="", height=2).pack()
            tk.Label(self.home_frame, text="Please choose from the following", font="helvetica, 18").pack()

            tk.Label(self.home_frame, text="", height=3).pack()
            tk.Button(self.home_frame, text="Sign-Up", width=30, bg="lightgrey", font="helvetica, 12",
                      command=lambda: [self.refresh(self.signup_frame), registrationpage(),
                                       self.show_frame(self.signup_frame)]).pack()

            tk.Label(self.home_frame, text="", height=1).pack()
            tk.Button(self.home_frame, text="Sign-In", width=30, bg="lightgrey", font="helvetica, 12",
                      command=lambda: [self.refresh(self.login_frame), loginpage(), self.show_frame(self.login_frame)]).pack()

            # tk.Label(self.home_frame, text="", height=1).pack()
            # tk.Button(self.home_frame, text="Exit", width=30, bg="black", fg="white", font="helvetica, 12",
            #           command=lambda: [self.exit_app()]).pack()

        # self.signup_frame widgets starts here
        # noinspection PyUnusedLocal
        def registrationpage():
            self.refresh(self.signup_frame)
            tk.Label(self.signup_frame, text="ICDE - [Skill Stack] SignUp", width=25, font=("bold", 24)).place(x=30, y=20)
            tk.Label(self.signup_frame, text="First Name", width=20, font=("bold", 12)).place(x=80, y=100)
            firstname_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12)).place(x=240, y=100)
            tk.Label(self.signup_frame, text="Last Name", width=20, font=("bold", 12)).place(x=80, y=150)
            lastname_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12)).place(x=240, y=150)
            tk.Label(self.signup_frame, text="Email", width=20, font=("bold", 12)).place(x=68, y=200)
            email_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12)).place(x=240, y=200)
            tk.Label(self.signup_frame, text="Password", width=20, font=("bold", 12)).place(x=80, y=250)
            passowrd_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12), show='*').place(x=240, y=250)
            # Password hashing
            hashed_pw = lambda: [self.PwHashing(passowrd_entry.get())]

            tk.Label(self.signup_frame, text="Re-enter Password", width=20, font=("bold", 12)).place(x=50, y=300)
            repassowrd_entry = tk.Entry(self.signup_frame, width=25, font=("bold", 12), show='*').place(x=240, y=300)
            tk.Label(self.signup_frame, text="Mobile Number", width=20, font=("bold", 12)).place(x=50, y=350)
            phone_number = tk.Entry(self.signup_frame, width=25, font=("bold", 12)).place(x=240, y=350)
            tk.Label(self.signup_frame, text="Date of birth (YYYY-MM-DD)", width=25, font=("bold", 12)).place(x=5, y=400)
            date_of_birth = tk.Entry(self.signup_frame, width=25, font=("bold", 12)).place(x=240, y=400)
            label_4 = tk.Label(self.signup_frame, text="Gender", width=20, font=("bold", 12))
            label_4.place(x=70, y=450)

            gen_var = tk.IntVar()
            tk.Radiobutton(self.signup_frame, text="Male", variable=gen_var, value=1, font=("bold", 12)).place(x=235, y=450)
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
            tk.Button(self.signup_frame, text='Submit', width=20, bg="black", fg='white', font=("bold", 12)).place(x=180,
                                                                                                              y=550)
            tk.Button(self.signup_frame, text="Back to Home page", width=20, bg="black", fg='white', font=("bold", 12),
                      command=lambda: self.show_frame(self.home_frame)).place(x=180, y=600)

        # Login_frame widgets starts here
        def loginpage():
            self.refresh(self.login_frame)
            tk.Label(self.login_frame, text="Please enter login details", font="helvetica, 16").pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Label(self.login_frame, text="Username", font="helvetica, 12").pack()
            username_entry = tk.Entry(self.login_frame, textvariable="username", width=40, font="helvetica, 12")
            username_entry.pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Label(self.login_frame, text="Password", font="helvetica, 12").pack()
            password_entry = tk.Entry(self.login_frame, textvariable="password", width=40, font="helvetica, 12", show='*')
            password_entry.pack()

            # Enable this to do not autofill user id for returning users
            # username_entry.delete(0, 'end')

            # Enable this to do not autofill password for returning users
            password_entry.delete(0, 'end')

            tk.Label(self.login_frame, text="").pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Button(self.login_frame, text="Forgot Password", width=30, height=1, bg="lightgrey", font="helvetica, 12",
                      command=lambda: [self.refresh(self.passwordReset_frame), passwordResetFrame(),
                                       self.show_frame(self.passwordReset_frame)]).pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Button(self.login_frame, text="Login", width=30, height=1, bg="lightgrey", font="helvetica, 12",
                      command=lambda: [self.login_data_validation(username_entry.get(), password_entry.get())]).pack()
            tk.Label(self.login_frame, text="").pack()
            tk.Button(self.login_frame, text="Back to Home page", width=30, bg="lightgrey", font="helvetica, 12",
                      command=lambda: [self.show_frame(self.home_frame)]).pack()

        # self.passwordReset_frame widgets start here
        def passwordResetFrame():
            self.refresh(self.passwordReset_frame)
            tk.Label(self.passwordReset_frame, text="Password Reset Page", font="helvetica, 20").place(x=300, y=40)
            tk.Label(self.passwordReset_frame, text="").pack()
            tk.Label(self.passwordReset_frame, text="E-mail", font="helvetica, 10").place(x=60, y=160)
            Email_entry = tk.Entry(self.passwordReset_frame, width=40, font=("bold", 12))
            Email_entry.place(x=270, y=160)
            tk.Label(self.passwordReset_frame, text="Enter your D.O.B (YYYY-MM-DD)", font="helvetica, 10").place(x=60, y=220)
            DOB_entry = tk.Entry(self.passwordReset_frame, width=40, font=("bold", 12))
            DOB_entry.place(x=270, y=220)
            tk.Label(self.passwordReset_frame, text="New Password", font="helvetica, 10").place(x=60, y=280)
            New_Password = tk.Entry(self.passwordReset_frame, width=40, font=("bold", 12))
            New_Password.place(x=270, y=280)
            tk.Label(self.passwordReset_frame, text="Confirm Password", font="helvetica, 10").place(x=60, y=340)
            Confirm_password = tk.Entry(self.passwordReset_frame, width=40, font=("bold", 12))
            Confirm_password.place(x=270, y=340)
            self.PwReset = tk.Button(self.passwordReset_frame, text='Submit', width=20, bg="black", fg='white',
                                     font=("bold", 12),
                                     command=lambda: [self.PwReset_data_validation(Email_entry.get(), DOB_entry.get())])
            self.PwReset.place(x=240, y=450)

        def AppMainPage():
            self.refresh(self.main_frame)
            tk.Label(self.main_frame, text="Application main page", font="helvetica, 16").pack()
            tk.Label(self.main_frame, text="").pack()

        homepage()
        registrationpage()
        loginpage()
        passwordResetFrame()
        AppMainPage()
        for frame in (self.home_frame, self.login_frame, self.signup_frame, self.passwordReset_frame, self.main_frame):
            frame.grid(row=0, column=0, sticky="nsew")
        super().show_frame(self.home_frame)


root = Icde()
root.mainloop()
