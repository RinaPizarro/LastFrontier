import sql_server as s

def main():
    print("Let's connect to the LastFrontier database.")
    while True:
        user_host = input("Enter host: ")
        user_name = input("Enter username: ")
        user_password = input("Enter password: ")

        status, message = s.connection(
            username=user_name,
            password=user_password,
            host=user_host)

        if status == False:
            print(message)
            print("Let's try that again. ")
            continue
        else:
            print(message)
            return # stop the program

if __name__ == "__main__":
    main()