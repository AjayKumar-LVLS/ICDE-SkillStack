import bcrypt

class Data_Verification:
    # Password hashing
    Email = ""
    Password = ""
    def PwHashing(self,password):
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        return hashed_pw

    # Verify Credentials
    def VerifyUser(self, Email, password):
        # verify user credentials and authenticate user.
        """hashed_pw = users.find({
            "E-mail" : Email
        })[0]["password"]"""
        pw = "ICDEProject"
        Stored_hashedpw = self.PwHashing(pw)
        Given_hashedpw = bcrypt.hashpw(password.encode('utf8'), Stored_hashedpw)

        if Given_hashedpw == Stored_hashedpw:
            return True
        else:
            return False
    # Comparing New pwd and confirm new password
    def confpwd(self,Newpwd,ConfirmPwd):
        # Newpwd="Skillstack"
        New_hashedPw = self.PwHashing(Newpwd)
        New_Confirm_hashedpw = self.PwHashing(ConfirmPwd)
        if Newpwd == ConfirmPwd:
            print("same")
            return True

        else:
            print("Not same")
            return False


    # Verify Security question
    def VerifySeqQn(self, Email, DOB):
        """user_DOB = users.find({
            "E-mail" : Email
        })[0]["DOB"]"""

        user_DOB = "19951028"

        if user_DOB == DOB:
            return True
        else:
            return False
class Pwreset:
    def PwHashing(self,password):
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        return hashed_pw