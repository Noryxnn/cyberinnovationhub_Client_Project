from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
from flask_cors import CORS
import bcrypt, sqlite3, json, requests


app = Flask(__name__)
CORS(app)
headers = {
    'accept': 'application/json',
    'api_key' : '1d0139b7c028fb569567a2e5915bf3e6bbbbd9059815da402b43173e2e49089d'
}



@app.route("/", methods=(['GET','POST']))
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
        conn = sqlite3.connect("loginPage/credentialDatabase.db")
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





if __name__ == "__main__":
    debug = True
    app.run(debug=True)