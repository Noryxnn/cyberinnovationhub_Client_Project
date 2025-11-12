from flask import *
import sqlite3
import datetime

DATABASE = 'moderator_page/DemoRequests.db'

app = Flask(__name__) 

@app.route("/")
def start():
    return render_template("navbarclient.html")

@app.route("/bedtest/<userName>")
def bedtest(userName):  
    idList = []
    itemsList = []
    dateList = []
    typeList = []
    statusList = []

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM DemoRequests WHERE userName = '{userName}'")
    res = cur.fetchall()
    for row in res:
        print(row)
        print("\n")
        idList.append(row[0])
        itemsList.append(row[2])
        dateList.append(row[3])
        typeList.append(row[4])
        statusList.append(row[5])
    conn.commit()
    conn.close()

    return render_template("bedtest.html",len=len(itemsList) ,userName=userName, itemsList=itemsList, dateList=dateList, typeList=typeList, statusList=statusList, idList=idList)

@app.route("/catalog")
def catalog():
    return render_template("catalog_page.html")

@app.route("/aboutus")
def aboutUs():
    return render_template("navbarclient.html")

@app.route("/contactus")
def contactUs():
    return render_template("navbarclient.html")

@app.route("/login")
def login():
    return render_template("navbarclient.html")

@app.route("/save", methods = ['GET', 'POST'])
def saveData():

    if request.method == 'POST':
        userName = request.form.get('userName')
        items = request.form.get('items')
        date = request.form.get('date')
        type = request.form.get('type')
        status = 'pending'

        print(date)

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO DemoRequests('userName', 'items' , 'date', 'type', 'status')VALUES (?,?,?,?,?)",(userName, items, date, type, status) ) # This works! Now time to add dynamic data. All data needs to be recieved from a form. Date in form 09/19/22 13:55:26
        conn.commit()
        conn.close()
    return render_template("catalog_page.html")



# Moderator page needs to display all data from db

@app.route("/history_page/<username>")
def history_page(username):


    idList = []
    itemsList = []
    dateList = []
    typeList = []
    status = 'closed'

    currentDate = datetime.datetime.now()

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM DemoRequests WHERE userName = '{username}'")
    res = cur.fetchall()
    for row in res:
        if row[3] < str(currentDate):
            itemsList.append(row[2])
            dateList.append(row[3])
            typeList.append(row[4])
            idList.append(row[0])
        elif row[5] == 'denied':
            itemsList.append(row[2])
            dateList.append(row[3])
            typeList.append(row[4])
            idList.append(row[0])
    print(dateList)
    conn.commit()
    conn.close()

    return render_template("history_page.html", len=len(dateList) ,username=username, itemsList=itemsList, dateList=dateList, typeList=typeList, idList=idList, status=status)

@app.route("/moderator")
def modPage():
    idList = []
    userNameList = []
    itemsList = []
    dateList = []
    typeList = []

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM DemoRequests WHERE status = 'pending'")
    res = cur.fetchall()
    for row in res: #For each of these a new tile needs to be added on moderator page
        print(row)
        print("\n")
        userNameList.append(row[1])
        itemsList.append(row[2])
        dateList.append(row[3])
        typeList.append(row[4])
        idList.append(row[0])
    print(idList)
    conn.commit()
    conn.close()
    return render_template("moderator_page.html",len=len(userNameList) ,userNameList=userNameList, itemsList=itemsList, dateList=dateList, typeList=typeList, idList=idList)


# I dont want to pass data like this. It needs to retrieve this data from db
# That's why I need the catalog page as when that is submitted all data will be saved to a database

@app.route("/moderator/deny/<bookingID>")
def denyRequest(bookingID):

    idList = []
    userNameList = []
    itemsList = []
    dateList = []
    typeList = []

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(f"UPDATE DemoRequests SET status = 'denied' WHERE bookingID = '{bookingID}'") # if status = denied it shouldn't be displayed onto screen and should send email to user saying their request was denied
    cur.execute("SELECT * FROM DemoRequests WHERE status = 'pending'")
    res = cur.fetchall()
    for row in res:
        print(row)
        print("\n")
        idList.append(row[0])
        userNameList.append(row[1])
        itemsList.append(row[2])
        dateList.append(row[3])
        typeList.append(row[4])
    conn.commit()
    conn.close()
    return render_template("moderator_page.html",len=len(userNameList) ,userNameList=userNameList, itemsList=itemsList, dateList=dateList, typeList=typeList, idList=idList)

@app.route("/moderator/accept/<bookingID>")
def saveInfo(bookingID):
    idList = []
    userNameList = []
    itemsList = []
    dateList = []
    typeList = []

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(f"UPDATE DemoRequests SET status = 'accepted' WHERE bookingID = '{bookingID}'")
    cur.execute("SELECT * FROM DemoRequests WHERE status = 'pending'")
    res = cur.fetchall()
    for row in res:
        print(row)
        print("\n")
        idList.append(row[0])
        userNameList.append(row[1])
        itemsList.append(row[2])
        dateList.append(row[3])
        typeList.append(row[4])
    conn.commit()
    conn.close()
    return render_template("moderator_page.html",len=len(userNameList) ,userNameList=userNameList, itemsList=itemsList, dateList=dateList, typeList=typeList, idList=idList)

@app.route("/clear")
def clear():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM DemoRequests")
    conn.commit()
    conn.close()
    return render_template("navbarclient.html")


if __name__ == "__main__":
    app.run(debug = True)

# Each demo tile created should be created with 5 properties. 
# One of these properties is dynamic and that's the list of chosen items. 
# This should be passed through from user selections