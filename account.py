import csv
import hashlib


def hash_password(pass_hash):
    hash_object = hashlib.sha512(bytes(pass_hash, encoding="utf-8"))
    password = hash_object.hexdigest()
    return password


def start():

    prompt = input('------------------------------------\n'
                        'To login, please type "login"\n'
                        'To create an account, type "create"\n'
                        'Enter choice: ')
    if "lo" in prompt.lower():
        Login()
    elif "cr" in prompt.lower():
        CreateAccount()
        print("\n\nThank You for creating an account")
        Login()
    else:
        print("Invalid entry - Please try again\n")
        start()


class CreateAccount:

    def __init__(self):
        self.user = ""
        self.new_pass = ""
        self.confirm_pass = ""
        self.username = self.create_user()
        self.password = self.create_pass()
        # writes the values of self.username and self.password to .csv file
        with open("account_info.csv", "a", newline="") as csv_file:
            account_writer = csv.writer(csv_file, delimiter=",")
            account_writer.writerow([self.username, self.password])

    def create_user(self):
        while self.user == "":
            self.user = input("Enter new username: ").strip().capitalize()
            if self.user != "":
                # checks .csv file to see if self.user already exists
                with open("account_info.csv", "r") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    for row in csv_reader:
                        if self.user.capitalize() in row:
                            print("Username is already taken\n")
                            self.user = ""
            else:
                print("\nUsername cannot be blank")
        return self.user

    def create_pass(self):
        while (self.new_pass == "") or (self.new_pass != self.confirm_pass):
            self.new_pass = input("Enter new password: ").strip()
            if self.new_pass != "":
                while self.confirm_pass == "":
                    self.confirm_pass = input("Confirm password: ").strip()
                    if self.confirm_pass != "":
                        if self.new_pass == self.confirm_pass:
                            print("Passwords match")
                            # if passwords match, sends self.new_pass to be hashed
                            hashed_pass = hash_password(self.new_pass)
                            self.new_pass = hashed_pass
                        else:
                            print("\nPasswords do not match - Try again")
                            self.confirm_pass = ""
                            self.create_pass()
                        return self.new_pass
                    else:
                        print("\nConfirm password left empty")
            else:
                print("\nPassword cannot be empty")
        return self.new_pass


class Login:

    def __init__(self):
        self.username = ""
        self.password = ""
        self.credentials()

    def credentials(self):
        while self.username == "":
            self.username = input("Enter Username: ")
            if self.username != "":
                while self.password == "":
                    self.password = input("Enter Password: ")
                    if self.password != "":
                        # sends self.password to be hashed and
                        # passes self.username and self.password to be authenticated
                        hashed_pass = hash_password(self.password)
                        self.authenticate(self.username.capitalize(), hashed_pass)
                    else:
                        print("Password is empty")
                    return self.password
            else:
                print("Username is empty")
        return self.username

    @staticmethod
    def authenticate(auth_user, auth_pass):
        username = auth_user
        password = auth_pass
        # checks if username exists, then verifies hash password matches
        with open("account_info.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                if username in row:
                    if row[1] == password:
                        print("You have successfully logged in")
                        return

            print("\nIncorrect username or password\nPlease try again\n")
            Login()


start()
