# זאב בן בסת

# Visual Studio Code IDE v1.63.2
# Python Interpreter v3.9.7

# צד שרת

import datetime, socket, sqlite3

# בסיס הנתונים
connection = sqlite3.connect('data.db')
cursor     = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS station_status (
                  station_id int,
                  last_date text,
                  alarm1 int,
                  alarm2 int,
                  PRIMARY KEY(station_id) )''')

# שקע שרת 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# קשר והקשבה לכתובת ולפורט
server_socket.bind(("127.0.0.1", 9090))
server_socket.listen()

while True:
    
    # קבל חיבורים
    (client_connected, client_address) = server_socket.accept()
    
    print()
    print("Accepted a connection request from %s:%s" % (client_address[0], client_address[1]))
    print()

    # נתונים שהתקבלו מהלקוח והדפסתם בטרמינל
    data_from_client = client_connected.recv(1024)

    print("The client send: Station Number & Alarms Status", data_from_client.decode())
    print()

    STATUS = data_from_client.decode().split()

    last_date  = datetime.datetime.now().strftime('%Y-%M-%d %H:%m')

    # הכנסת הנתונים ושמירתם בבסיס הנתונים
    cursor.execute("INSERT OR REPLACE INTO station_status VALUES (?, ?, ?, ?)", (int(STATUS[0]), last_date, int(STATUS[1]), int(STATUS[2])))

    connection.commit()

    # הדפסת בסיס הנתונים
    print("\033[0;37;41mWater stations database:\033[0;37;40m")

    for row in cursor.execute('SELECT * FROM station_status ORDER BY station_id'):
        print(row)

    # שלח נתונים בחזרה ללקוח
    client_connected.send("The server response: Data successfully received from client! Wait 60 seconds for the next broadcast ..".encode())