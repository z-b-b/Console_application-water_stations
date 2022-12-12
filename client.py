# זאב בן בסת 

# Visual Studio Code IDE v1.63.2
# Python Interpreter v3.9.7

# צד לקוח

import random, socket, time, webbrowser

id_alarm1_alarm2 = ""

# מחשב
def computer():
    
    print()
    print("You have selected the computer to edit the file randomly!")
    print()
    
    # כתיבת המידע על התחנה בקובץ
    with open("status.txt", "w") as status_file:
        status_file.write(str(random.randint(1, 999)) + "\n" + str(random.randint(0, 1)) + "\n" + str(random.randint(0, 1)))

    id_alarms = ""

    # קריאת המידע על התחנה מהקובץ למשתנה מסוג מחרוזת לשם שליחה לשרת
    with open("status.txt", "r") as status_file:
        for line in status_file:
            id_alarms += line.rstrip("\n") + " "

    return id_alarms

# משתמש
def user():

    print()
    print("You have chosen to edit the file yourself!")
    print()

    with open("status.txt", "w") as status_file:
        # האם הקובץ הצליח להיפתח דרך העורך של מערכת ההפעלה
        try:
            webbrowser.open("status.txt")
        except:
            print("There is an unexpected error! The program ends!")
            quit()
        
        # התוכנית מחכה שהמשתמש יסיים לערוך את הקובץ
        is_finished = ""
        while is_finished != "y":
            # code injection מניעת 
            # input דרך ה
            try:
                is_finished = input("Press y to continue... ")
            except:
                print("There is a break-in! The program ends!")
                quit()

    print()

    with open("status.txt", "r") as status_file:
        id     = status_file.readline()
        alarm1 = status_file.readline()
        alarm2 = status_file.readline()

        flag = True

        # בדיקת נכונות המידע בקובץ
        try:
            if int(id) < 1 or int(id) > 999:
                flag = False

            if int(alarm1) < 0 or int(alarm1) > 1:
                flag = False

            if int(alarm2) < 0 or int(alarm2) > 1:
                flag = False
        except: 
            flag = False

    # אם הקובץ ערוך נכון המידע ישלח לשרת
    if flag == True:
        id_alarms = id.rstrip("\n") + " " + alarm1.rstrip("\n") + " " + alarm2.rstrip("\n")
        
        return id_alarms
   
    # אחרת
    else:
        print("You did not edit the file correctly! try again!")
        print()

        return None

# התוכנית הראשית

print()
print("\033[0;37;41mWater Stations Input:\033[0;37;40m")
print()

# ריצה בלולאה ושליחה הנתונים לשרת בכל דקה
while True:

    # שקע לקוח
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # התחבר לכתובת השרת המקומי
    client_socket.connect(("127.0.0.1", 9090))

    # עריכת הקובץ: בחירה > המחשב מנחש מספרים (הוספה שלי) או
    # המשתמש עורך את הקובץ תוך כדי ריצת התוכנית 
    select = ""
    while select != "c" and select != "u":    
        # code injection מניעת 
        # input דרך ה
        try:
            select = input("Choose who will edit status.txt file Computer(c) or User(u) > ")
        except:
            print("There is a break-in! The program ends!")
            quit()

    if select == "c":
        id_alarm1_alarm2 = computer()
    elif select == "u":
        id_alarm1_alarm2 = user()

    if id_alarm1_alarm2 != None:
        # שליחה מידע לשרת
        client_socket.send(id_alarm1_alarm2.encode())

        # קבלת מידע מהשרת והדפסתו בטרמינל
        data_from_server = client_socket.recv(1024)

        print(data_from_server.decode())
        print()

    # קריאת המידע מהקובץ כל דקה 
    time.sleep(60)