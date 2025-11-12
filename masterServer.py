from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
from flask_cors import CORS
import bcrypt, sqlite3, json, requests
import datetime


app = Flask(__name__)
CORS(app)
headers = {
    'accept': 'application/json',
    'api_key' : '1d0139b7c028fb569567a2e5915bf3e6bbbbd9059815da402b43173e2e49089d'
}



@app.route("/yes", methods=(['GET','POST']))
def hello_world():
    """if request.method == 'POST':
        return """""
    return render_template("Loginpage.html")

@app.route("/historyPageRender", methods=(['GET','POST']))
def literally():
    return render_template("historyPage.html")

@app.route("/historyPage", methods=(['POST']))
def getDataFromAPI():
    deviceWanted = request.json
    deviceHistory = []
    for devices in deviceWanted:
        url = f'https://csil-api.onrender.com/device/history/{devices}?limit=10&date_sort=false'
        try:
            switch_req = requests.get(url, headers=headers)
            switch_hs = json.loads(switch_req.content)
            deviceHistory.append(switch_hs)
        except Exception as err:
            print(f"error: {err}")
    return make_response(jsonify(deviceHistory), 200)



@app.route("/loginPage", methods=(['GET','POST']))  
def loginPage():
    return render_template("Loginpage.html")

@app.route("/backendVerification", methods=(['POST']))
def handle_variants():
    credentials = request.json
    username = credentials[0]
    password = credentials[1]
    email = credentials[2]
    variant = credentials[3]
    if variant == 1:    
        if compareWithDatabase(username, password, "admin"):
            print("YIPPEE admin")
            try:
                return make_response(jsonify({"permissionGranted":1}), 200)
            except Exception as err:
                print(f"Error: {err}")
                return make_response(jsonify({"error": str(err)}), 500)
        
        elif compareWithDatabase(username, password, "user"):
            print("YIPPEE user")
            try:
                return make_response(jsonify({"permissionGranted":2}), 200)
            except Exception as err:
                print(f"Error: {err}")
                return make_response(jsonify({"error": str(err)}), 500)
        print("NOPE")
        return make_response(jsonify({"permissionGranted":3}), 200)
    elif variant == 2:
        conn = sqlite3.connect("credentialDatabase.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO userCredentials ('username', 'password', 'email') VALUES (?,?,?)" ,(username,hashAndSalt(password),email))
        conn.commit()
        conn.close()
        return make_response(jsonify({"permissionGranted":4}), 200)

@app.route("/admin")
def whatever():
    security = """
<script>
    fetch('/verifyIsAdmin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ securityValue: localStorage.getItem("security") }),
        redirect: 'follow'
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    })
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
</script>
    """
    return security

@app.route("/verifyIsAdmin", methods=['POST'])
def verifyIsAdmin():
    data = request.get_json()
    securityType = data.get('securityValue', None)
    print(securityType)
    if securityType == "admin":
        return render_template("adminPage.html")
    else:
        return redirect(url_for("loginPage"))
        
@app.route("/adminDashoard")
def adminDashboard():
    return("ADMIN")    

def hashAndSalt(credential):
    password = credential.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed

def verifyHashing(credential,hashed_password):
    if isinstance(credential, str):
        credential = credential.encode("utf-8")
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(credential, hashed_password)

def compareWithDatabase(username,password, loginType):
    conn = sqlite3.connect("credentialDatabase.db")
    cur = conn.cursor()
    if loginType == "admin":
        cur.execute("SELECT * FROM adminCredentials")
    elif loginType == "user":
        cur.execute("SELECT * FROM userCredentials")
    res = cur.fetchall()
    for credential in res:
        if username in credential[0]:
            if verifyHashing(password, credential[1]): 
                validLogin = True
                print(username,password)
                return validLogin
    validLogin = False        
    return validLogin


DATABASE = 'DemoRequests.db'

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/bookingHistory")
def bookingHistoryLoad():
    return render_template("bookingPageLoad.html")

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
    debug = True
    app.run(debug=True)