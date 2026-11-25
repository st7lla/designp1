import bcrypt


def authenticate():

        while True:
            userid = input("Enter your userid:")

            if userid not in userids:
                print("User ID not found")
                choice = input("Create a new account? (y/n): ")
                if choice.lower() == "y":
                    sign_up()
                    break
                continue

            hash = hashes[userids.index(userid)]
            attempts = 0

            while attempts < 3:
                password = input("Enter your password: ")

                if bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8')):
                    print("Login successful. Welcome, " + userid + "!")
                    return userid

                attempts = attempts + 1
                if attempts < 3:
                    print("Incorrect password. " + str(3 - attempts) + " tries left")

            print("Too many failed attempts. Re-enter ID")

