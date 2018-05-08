import sqlite3
import os
from time import sleep

# Function to check if connected to the database.
def connectDB():
    try:
        con = sqlite3.connect('Users.db')
        # print("Connected  to db !!")
        return con
    except sqlite3.Error as err:
        print("There is a problem with connection: [{}]").format(err)

# Function to check if value is integer.
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# c = con.cursor()

# # ans = c.execute("CREATE TABLE IF NOT EXISTS users(fname VARCHAR , lname VARCHAR, age INT);")
# # sql = "INSERT INTO users VALUES ('Abdalla', 'Diab', '26')"
# sql = "SELECT * FROM users"
# ans = c.execute(sql)

# # if(ans):
# #     print("Data is inserted !!")
# for row in ans:
#     print(row)

# con.commit()
# con.close()


# Show menu.
menu = True


######################################
##### START APPLICATION ##############
######################################
while(menu):
    choice = input("""\
    What do you want to do:
    1-Show users.
    2-Add user.
    3-Edit user.
    4-Delete User.
    5-Exit.
    \n Your choice: """)

    # Check if not a number was entered
    if(not RepresentsInt(choice)):
        os.system("cls")
        menu = False
        print("Wrong input start application again")
        exit()
        
    # Parse choice as an integer not a string.
    choice = int(choice)
        

#################################
######## SHOW USERS #############
#################################
    if(choice == 1):
        con = connectDB()
        c = con.cursor()

        try:
            sql1 = "SELECT * FROM users"
            check = c.execute(sql1)
            dataFound = True
            users = c.fetchall()
    
            while(dataFound):
                
                if(len(users) > 0):
                    os.system("cls")
                    
                    print("List of users..\n")
                    print("\n\n#ID\t\tFirstName\t\tLastName\t\tSalary")
                    for user in users:
                        print("{}\t\t{}\t\t\t{}\t\t\t{}\t".format(user[0], user[1], user[2], user[3]))
                        print("-"*78)
                    
                    print("\ncancel or c to return back")
                    exit = input("# ")
                    if(exit == "cancel" or "c"):
                        con.close()
                        os.system("cls")
                        dataFound = False
                    

                else:
                    print("\n [No data found]")
                    con.close()
                    sleep(8)
                    os.system("cls")
                    dataFound = False

        except sqlite3.Error as err:
            print("There is a problem with the database: [{}]".format(err))
    
#################################
########## ADD USER #############
#################################
    elif(choice == 2):
        con = connectDB()
        c = con.cursor()
        try:
            while(True):
                os.system('cls')
                print(" - [c] command to cancel the editing\n")
                fname = input("Enter first name: ")

                # To cancel adding.
                if(fname[0:2] == "c"):
                    con.close()
                    os.system("cls")
                    break

                lname = input("Enter last name: ")

                salary = float(input("Enter salary: "))

                sql2 = "INSERT INTO users(fname, lname, salary) VALUES('{}', '{}', {})".format(fname.lower(), lname.lower(), float(salary))
                check = c.execute(sql2)
                con.commit()
                addUser = True

                while(addUser):
                    if(check):
                        print("\nAdded successfully !!")
                        sleep(1)
                        os.system('cls')
                        addUser = False


        except sqlite3.Error as err:
            print("There is a problem with the database: [{}]".format(err)) 
        
###################################
########## EDIT USER ##############
###################################
    elif(choice == 3):
        editing = True
        
        while(editing):
                
            os.system("cls")
            print(" - HOW TO USE => # [edit] [fname] or [lname]")
            print(" - [c] command to cancel the editing")

            userInput2 = input("# ")

            if(userInput2 == "cancel" or userInput2 == "c"):
                editing = False
                os.system("cls")
                break
            
            else:
                con = connectDB()
                c = con.cursor()
                try:
                    command1 = userInput2[0:4] # Substring just for fun.
                    command2 = userInput2[5:10] # Substring the column name.

                    # To return back.
                    if(command1[0:2] == "c"):
                        editing = False

                    # This condition to edit salary.
                    if(command2 == "salar"):
                        userInput3 = input("Whats his last name: ")
                        userInput4 = input("Whats the new value: ")
                    
                        sql3 = "UPDATE users SET salary = {} WHERE lname = '{}'".format(float(userInput4), userInput3)
                        check = c.execute(sql3)
                        con.commit()

                        if(check):
                            print("Edited Successfully !!")
                            sleep(1)
                            con.close()
                            os.system('cls')
                            editing = False

                    else:
                        # Security condition.
                        if(command1 == "edit" and (command2 == "fname" or command2 == "lname")):
                            userInput3 = input("Whats his {}: ".format(command2))
                            userInput4 = input("Whats {} new value: ".format(command2))
                            
                            sql3 = "UPDATE users SET {} = '{}' WHERE {} = '{}'".format(command2, userInput4.lower(), command2, userInput3)
                            check = c.execute(sql3)
                            con.commit()

                            if(check):
                                print("Edited Successfully !!")
                                sleep(1)
                                con.close()
                                os.system('cls')
                                editing = False
                        else:
                            os.system("cls")
                            print("Wrong command, try again !")
                            sleep(1)
                            os.system("cls")
                            break

                except sqlite3.Error as err:
                    print("There is a problem with the database: [{}]".format(err))

#################################
####### DELETE USER #############
#################################
    elif(choice == 4):
        os.system("cls")
        con = connectDB()
        c = con.cursor()

        print("HOW TO DELETE => # delete [userid]")
        # delete 5
        userInput5 = input("# ")
        command3 = userInput5[0:6]
        command4 = userInput5[7:]

        while(True):

            if(command3[0:2] == "c"):
                os.system("cls")
                break

            if(command3 == "delete" and RepresentsInt(command4)):
                
                sql4 = "DELETE FROM users WHERE user_id = {}".format(command4)
                isFinished = c.execute(sql4)
                con.commit()

                if(isFinished):
                    print("User is delete successfully !!")
                    sleep(1)
                    con.close()
                    os.system('cls')
                    break


            else:
                os.system("cls")
                print("Wrong command, try again !")
                sleep(1)
                os.system("cls")
                break
    

        
    elif(choice == 5):
        menu = False

        # Check if connection is closed or not to close it.
        if(not connectDB().close()):
            connectDB().close()

        print("bye :)")
        exit()
    
    else:
        os.system("cls")
        print("Wrong command, try again !")
        break