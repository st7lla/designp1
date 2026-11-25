import bcrypt


def sign_up():

    while True:
        userid = input("Enter a new userid: ")

        if userid == "" or " " in userid or "," in userid:
            print("Invalid ID - no blanks, spaces or commas")
        elif userid in existing_ids:
            print("ID already taken, try another")
        else:
            break

    while True:
        password = input("Enter a password: ")

        has_upper = False
        has_lower = False
        has_digit = False
        has_symbol = False

        for char in password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True
            elif char in symbols:
                has_symbol = True

        if len(password) >= 6 and has_upper and has_lower and has_digit and has_symbol:
            confirm = input("Re-enter password to confirm: ")

            if confirm == password:
                break
            else:
                print("Passwords do not match")
        else:
            print("Weak password. Your password must have:")
            print("at least 6 characters")
            print("at least one uppercase letter")
            print("at least one lowercase letter")
            print(“at least one digit")
            print("at least one symbol from: + symbols”)


    file = open("users.csv", "a")
    file.write(userid + "," + hash + "\n")
    file.close()

    print("Account created successfully")

