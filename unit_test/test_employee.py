import unittest
from employee import Employee

class TestEmployee(unittest.TestCase):

    def setUp(self):
        print("setup")
        self.emp1 = Employee("Emp", "One", 50000)
        self.emp2 = Employee("Emp", "Two", 60000)

    def tearDown(self):
        pass 

    def test_email(self):
        print("test email")
        self.assertEqual(self.emp1.email, "Emp.One@email.com")
        self.assertEqual(self.emp2.email, "Emp.Two@email.com")

        self.emp1.first = "John"
        self.emp2.first = "Jane"

        self.assertEqual(self.emp1.email, "John.One@email.com")
        self.assertEqual(self.emp2.email, "Jane.Two@email.com")

    def test_fullname(self):

        self.assertEqual(self.emp1.fullname, "Emp One")
        self.assertEqual(self.emp2.fullname, "Emp Two")

        self.emp1.first = "John"
        self.emp2.first = "Jane"

        self.assertEqual(self.emp1.fullname, "John One")
        self.assertEqual(self.emp2.fullname, "Jane Two")

    def test_raise(self):

        self.emp1.apply_raise()
        self.emp2.apply_raise()

        self.assertEqual(self.emp1.pay, 52500)
        self.assertEqual(self.emp2.pay, 63000)


if __name__ == "__main__":
    unittest.main()