class User:
    def __init__(self, name, pin, password):
        self._name = name
        self._pin = pin
        self._password = password

    def get_name(self):
        return self._name

    def get_pin(self):
        return self._pin

    def get_password(self):
        return self._password

    def change_name(self, name):
        self._name = name

    def change_pin(self, pin):
        self._pin = pin

    def change_password(self, password):
        self._password = password


class BankUser(User):
    def __init__(self, name, pin, password):
        super().__init__(name, pin, password)
        self._balance = 0.00

    def get_balance(self):
        return self._balance

    def show_balance(self):
        print(
            f"{self.get_name()} has an account balance of ${float(self.get_balance()):0,.2f}")

    def change_balance(self, balance):
        self._balance = balance

    def withdraw(self, amount):
        self._balance -= amount

    def deposit(self, amount):
        self._balance += amount

    def transfer_money(self, amount,user):
        print(f"You are transfering ${float(amount):0,.2f} to {user.get_name()}\nAuthentication Required")
        if self.get_pin() != input("Enter your PIN: "):
            print("Invalid PIN. Transaction Canceled")
        else: 
            print("Transfer Authorized")
            self.withdraw(amount)
            user.deposit(amount)
            print(f"Transfering ${float(amount):0,.2f} to {user.get_name()} ")

    def request_money(self,amount,user):
        print(f"You are requesting ${float(amount):0,.2f} from {user.get_name()}\nUser authentication is required")
        if user.get_pin() != input(f"Enter {user.get_name()}'s PIN: "):
            print("Invalid PIN. Transaction Canceled")
        else: 
            if self.get_password() != input("Enter your password: "):
                 print("Invalid password. Transaction Canceled")
            else: 
                print("Request Authorized")
                user.withdraw(amount)
                self.deposit(amount)




""" Driver Code for Task 1 """
test_user = User("Jose task 1", "0101", "password123")
print(f"{test_user.get_name()} , {test_user.get_pin()} , {test_user.get_password()}")

""" Driver Code for Task 2 """
test_user2 = User("Jose Santi", "0101", "password123")
print(f"{test_user2.get_name()} , {test_user2.get_pin()} , {test_user2.get_password()}")
test_user2.change_name("Jose Santiago")
test_user2.change_pin("1234")
test_user2.change_password("passwordChanged")
print(f"{test_user2.get_name()} , {test_user2.get_pin()} , {test_user2.get_password()}")

""" Driver Code for Task 3"""
test_user3 = BankUser("Jose Manuel", "0101", "password123")
print(f"{test_user3.get_name()} , {test_user3.get_pin()} , {test_user3.get_password()} , {test_user3.get_balance()}")

""" Driver Code for Task 4"""
test_user4 = BankUser("Jose Echevarria", "3434", "password123")
test_user4.show_balance()
test_user4.deposit(4500)
test_user4.show_balance()
test_user4.withdraw(2000)
test_user4.show_balance()



""" Driver Code for Task 5"""

test_user5 = BankUser("Jose Mani Santiago", "1234", "password123456")
test_user6 = BankUser("Gokul", "5678", "password123")
test_user6.deposit(5000)
test_user6.show_balance()
test_user5.show_balance()
test_user6.transfer_money(500,test_user5)
test_user6.show_balance()
test_user5.show_balance()
if(test_user5.get_balance() == 500 and test_user6.get_balance() == 4500):
    test_user6.request_money(500,test_user5)
    test_user6.show_balance()
    test_user5.show_balance()
