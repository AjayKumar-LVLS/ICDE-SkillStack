import unittest
import ICDE_APPCORE
from unittest import mock


class TestIcdeAppCore(unittest.TestCase):
    email = "miranda@gmail.com"
    password = "miranda123"
    DOB = "1992-09-08"
    enrolled_course = "Guide to Entreprenuership"
    not_enrolled_course = "dummy course name"
    profile = {
        "Firstname": "Test_firstname",
        "Lastname": "Test_lastname",
        "Email": "Test_Email",
        "MobileNumber": "Test_0000000000",
        "Password": "Test_#agrslheruhgyweyrgweyrrgyuweyrugwyegwthgrbtgrtre3423",
        "Gender": "Test_Male",
        "Stream": "Test_Stream",
        "DateOfBirth": "Test_1992-09-09",
        "CoursesEnrolled": [],
        "RegistrationDate": "Test_RegistrationDate",
        "Lastloggedintime": "Test_Lastloggedintime",
        "Usagestats": {

        }
    }

    # test to check the VerifyUser function with wrong password
    def test1_VerifyUser(self):
        ret = ICDE_APPCORE.Data_Verification.VerifyUser(self,Email=self.email,
                                                        password="miranda1")
        self.assertEqual(ret, False)

    # test to check the VerifyUser function with wrong email id
    def test2_VerifyUser(self):
        ret = ICDE_APPCORE.Data_Verification.VerifyUser(self,Email="miranda1@gmail.com",
                                                        password=self.password)
        self.assertEqual(ret, False)

    # test to check the VerifyUser function with correct credentials
    def test3_VerifyUser(self):
        ret = ICDE_APPCORE.Data_Verification.VerifyUser(self,self.email, self.password)
        self.assertEqual(ret, True)

    # test to check the VerifySeqQn function with wrong DOB
    def test1_VerifySeqQn(self):
        ret = ICDE_APPCORE.Data_Verification.VerifySeqQn(self,Email=self.email,
                                                         DOB="1992-09-09")
        self.assertEqual(ret, False)

    # test to check the VerifySeqQn function with correct DOB for an existing profile
    def test2_VerifySeqQn(self):
        ret = ICDE_APPCORE.Data_Verification.VerifySeqQn(self,Email=self.email,
                                                         DOB=self.DOB)
        self.assertEqual(ret, True)

    # test to check the check_enrollement function on passing  course which is enrolled before.
    def test1_check_enrollement(self):
        ret = ICDE_APPCORE.IcdeAppCore.check_enrollement(self,self.email,self.enrolled_course)
        self.assertEqual(ret, False)

    # test to check the check_enrollement function on passing  course which is not enrolled before.
    def test2_check_enrollement(self):
        ret = ICDE_APPCORE.IcdeAppCore.check_enrollement(self,self.email,self.not_enrolled_course)
        self.assertEqual(ret, True)

    @mock.patch("ICDE_DataBase.IcdeDataBase.create_profile_db")
    def test1_createProfile(self,mock_create_profile_db):
        mock_create_profile_db.return_value = True
        ret = ICDE_APPCORE.IcdeAppCore.createProfile(self,"firstname","lastname",
              "username","phone_number","password","reentered_password","gender",
                                                     "stream", "date_of_birth")
        self.assertEqual(ret, True)

    @mock.patch("ICDE_DataBase.IcdeDataBase.create_profile_db")
    def test2_createProfile(self,mock_create_profile_db):
        mock_create_profile_db.par = self, self.profile
        mock_create_profile_db.return_value = False
        ret = ICDE_APPCORE.IcdeAppCore.createProfile(self,"firstname","lastname",
              "username","phone_number","password","reentered_password","gender",
                                                     "stream", "date_of_birth")
        self.assertEqual(ret, False)



if __name__ == '__main__':
    unittest.main()
