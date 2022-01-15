import tkinter as tk
from tkinter import messagebox

# Turn this variable to True if login details were verified with those in DataBase.
login_data_validated = False


# Provide functionalities to frames.
# noinspection PyMethodMayBeStatic
class Functionalities(tk.Tk):
    def show_frame(self, frame):
        frame.tkraise()

    def exit_app(self):
        self.destroy()

    def refresh(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()


# To Initialization the main window
class Initialization(tk.Tk):
    def __init__(self):
        super().__init__()

    def setup(self):
        self.title("ICDE - [Skill Stack]")
        self.geometry("800x700")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


# To validate the input data entered by user
# noinspection PyMethodMayBeStatic
class DataValidation:
    def __init__(self):
        global login_data_validated
        login_data_validated = False

    # To validate the details entered by user at login page
    def login_data_validation(self, username, password):
        global login_data_validated
        login_data_validated = False
        if username == "" and password == "":
            tk.messagebox.showwarning("Error", "Input fields can not be empty")
        elif username == "":
            tk.messagebox.showwarning("Error", "Username can not be empty")
        elif password == "":
            tk.messagebox.showwarning("Error", "Password can not be empty")
        elif "@" not in username or ".com" not in username:
            tk.messagebox.showwarning("Error", "Please enter a valid email address")
        # Create another elif condition here to contact with DataBase and validate login credentials.
        else:
            tk.messagebox.showwarning("Error", "No account found with this email address, please signup")

    # To validate the details entered by user at registration page
    def signup_data_validation(self, firstname, lastname, username, phone_number, password, reentered_password, gender,
                               stream, date_of_birth):
        pass


# This is the main class
# noinspection SpellCheckingInspection
class Icde(Initialization, Functionalities, DataValidation):
    def __init__(self):
        super().__init__()
        super().setup()
        DataValidation.__init__(self)

        # Creating different frames in application
        main_frame = tk.Frame(self)
        login_frame = tk.Frame(self)
        signup_frame = tk.Frame(self)

        # Inserting widgets in different frames
        # Main_frame widgets starts here
        def homepage():
            tk.Label(main_frame, text="ICDE - [Skill Stack]", width=100, font="bold, 30", bg="black", fg="white",
                     height=2).pack()

            tk.Label(main_frame, text="", height=2).pack()
            tk.Label(main_frame, text="Please choose from the following", font="helvetica, 18").pack()

            tk.Label(main_frame, text="", height=3).pack()
            tk.Button(main_frame, text="Sign-Up", width=30, bg="lightgrey", font="helvetica, 12",
                      command=lambda: [self.refresh(signup_frame), registrationpage(), self.show_frame(signup_frame)]).pack()

            tk.Label(main_frame, text="", height=1).pack()
            tk.Button(main_frame, text="Sign-In", width=30, bg="lightgrey", font="helvetica, 12",
                      command=lambda: [self.refresh(login_frame), loginpage(), self.show_frame(login_frame)]).pack()

            # tk.Label(main_frame, text="", height=1).pack()
            # tk.Button(main_frame, text="Exit", width=30, bg="black", fg="white", font="helvetica, 12",
            #           command=lambda: [self.exit_app()]).pack()

        # signup_frame widgets starts here
        # noinspection PyUnusedLocal
        def registrationpage():
            self.refresh(signup_frame)
            tk.Label(signup_frame, text="ICDE - [Skill Stack] SignUp", width=25, font=("bold", 30)).place(x=30, y=40)
            tk.Label(signup_frame, text="First Name", width=20, font=("bold", 12)).place(x=80, y=130)
            firstname_entry = tk.Entry(signup_frame, width=25, font=("bold", 12)).place(x=240, y=130)
            tk.Label(signup_frame, text="Last Name", width=20, font=("bold", 12)).place(x=80, y=180)
            lastname_entry = tk.Entry(signup_frame, width=25, font=("bold", 12)).place(x=240, y=180)
            tk.Label(signup_frame, text="Email", width=20, font=("bold", 12)).place(x=68, y=230)
            email_entry = tk.Entry(signup_frame, width=25, font=("bold", 12)).place(x=240, y=230)
            tk.Label(signup_frame, text="Password", width=20, font=("bold", 12)).place(x=80, y=280)
            passowrd_entry = tk.Entry(signup_frame, width=25, font=("bold", 12), show='*').place(x=240, y=280)
            tk.Label(signup_frame, text="Re-enter Password", width=20, font=("bold", 12)).place(x=50, y=330)
            repassowrd_entry = tk.Entry(signup_frame, width=25, font=("bold", 12), show='*').place(x=240, y=330)
            tk.Label(signup_frame, text="Mobile Number", width=20, font=("bold", 12)).place(x=50, y=380)
            phone_number = tk.Entry(signup_frame, width=25, font=("bold", 12)).place(x=240, y=380)
            tk.Label(signup_frame, text="Date of birth (YYYY-MM-DD)", width=25, font=("bold", 12)).place(x=5, y=430)
            date_of_birth = tk.Entry(signup_frame, width=25, font=("bold", 12)).place(x=240, y=430)
            label_4 = tk.Label(signup_frame, text="Gender", width=20, font=("bold", 12))
            label_4.place(x=70, y=480)

            gen_var = tk.IntVar()
            tk.Radiobutton(signup_frame, text="Male", variable=gen_var, value=1, font=("bold", 12)).place(x=235, y=480)
            tk.Radiobutton(signup_frame, text="Female", variable=gen_var, value=2, font=("bold", 12)).place(x=310,
                                                                                                            y=480)

            tk.Label(signup_frame, text="Stream", width=20, font=("bold", 12)).place(x=70, y=530)

            # Add more branches here to appear in the dropdown list in signup page
            list_of_streams = ['Electrical Engineering', 'Computer Engineering', 'Electronics Engineering',
                               'Mechanical Engineering', 'Civil Engineering']

            stream = tk.StringVar()
            stream_list = tk.OptionMenu(signup_frame, stream, *list_of_streams)
            stream_list.config(width=20, font=("bold", 12))
            stream.set('Select your Stream')
            stream_list.place(x=240, y=530)
            #
            tk.Button(signup_frame, text='Submit', width=20, bg="black", fg='white', font=("bold", 12)).place(x=180,
                                                                                                              y=600)
            tk.Button(signup_frame, text="Back to Home page", width=20, bg="black", fg='white', font=("bold", 12),
                      command=lambda: self.show_frame(main_frame)).place(x=180, y=650)

        # Login_frame widgets starts here
        def loginpage():
            self.refresh(login_frame)
            tk.Label(login_frame, text="Please enter login details", font="helvetica, 16").pack()
            tk.Label(login_frame, text="").pack()
            tk.Label(login_frame, text="Username", font="helvetica, 12").pack()
            username_entry = tk.Entry(login_frame, textvariable="username", width=40, font="helvetica, 12")
            username_entry.pack()
            tk.Label(login_frame, text="").pack()
            tk.Label(login_frame, text="Password", font="helvetica, 12").pack()
            password_entry = tk.Entry(login_frame, textvariable="password", width=40, font="helvetica, 12", show='*')
            password_entry.pack()

            # Enable this to do not autofill user id for returning users
            # username_entry.delete(0, 'end')

            # Enable this to do not autofill password for returning users
            password_entry.delete(0, 'end')

            tk.Label(login_frame, text="").pack()
            tk.Label(login_frame, text="").pack()
            tk.Label(login_frame, text="").pack()
            tk.Button(login_frame, text="Forgot Password", width=30, height=1, bg="lightgrey",
                      font="helvetica, 12").pack()
            tk.Label(login_frame, text="").pack()
            tk.Button(login_frame, text="Login", width=30, height=1, bg="lightgrey", font="helvetica, 12",
                      command=lambda: [self.login_data_validation(username_entry.get(), password_entry.get())]).pack()
            tk.Label(login_frame, text="").pack()
            tk.Button(login_frame, text="Back to Home page", width=30, bg="lightgrey", font="helvetica, 12",
                      command=lambda: [self.show_frame(main_frame)]).pack()

        homepage()
        registrationpage()
        loginpage()
        for frame in (main_frame, login_frame, signup_frame):
            frame.grid(row=0, column=0, sticky="nsew")
        super().show_frame(main_frame)


root = Icde()
root.mainloop()
