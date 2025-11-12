
function credentialValidation(variant) {
    var validInput = false;
    if (variant === 1) {
        var username = document.forms.credentialsEnter.username.value.trim()
        var password = document.forms.credentialsEnter.password.value.trim()
    }
    if (variant === 2) {
        var username = document.forms.createAccount.username2.value.trim()
        var password = document.forms.createAccount.password2.value.trim()
        var email = document.forms.createAccount.email.value.trim()
        var validInput = false;
        var badInputs = ["=", "<", ">", "*", "|", "'", "%", "^", "&", "(", ")", "-", "+", "]", "}", "[", "{", ":", ";", "?", "/", "\"", "SELECT", "FROM", "WHERE", "CREATE", "RETRIEVE", "UPDATE", "DELETE", "CREATE", "GROUP BY", " ", "HAVING", "INNER", "JOIN", "LEFT", "OUTER", "RIGHT", "FULL", "AS", "DISTINCT", "LIKE", "AND", "OR", "TABLE"]

        while (!validInput) {
            if (email.length > 2 && email.length <= 50) {
                var usedBadInputs = []
                var containsValidLetters = true
                for (const substring of badInputs) {
                    if (email.includes(substring)) {
                        var containsValidLetters = false
                        usedBadInputs.push(substring)
                    }
                }
                var validInput = containsValidLetters
                if (!validInput) {
                    if (email.length > 2 && password.length <= 50) {
                        email = prompt("email cannot contain " + usedBadInputs.toString())
                    }
                }
            }
            else {
                email = prompt("Please enter an email between 5 and 25 characters long")
            }
        }
    }
    var badInputs = ["=", "<", ">", "*", "|", "'", "%", "^", "&", "(", ")", "-", "+", "]", "}", "[", "{", ":", ";", "@", ".", "?", "/", "\"", "SELECT", "FROM", "WHERE", "CREATE", "RETRIEVE", "UPDATE", "DELETE", "CREATE", "GROUP BY", " ", "HAVING", "INNER", "JOIN", "LEFT", "OUTER", "RIGHT", "FULL", "AS", "DISTINCT", "LIKE", "AND", "OR", "TABLE"]

    while (!validInput) {
        if (username.length > 2 && username.length <= 25) {
            var usedBadInputs = []
            var containsValidLetters = true
            for (const substring of badInputs) {
                if (username.includes(substring)) {
                    var containsValidLetters = false
                    usedBadInputs.push(substring)
                }
            }
            var validInput = containsValidLetters
            if (!validInput) {
                if (username.length > 2 && username.length <= 25) {
                    username = prompt("Username cannot contain " + usedBadInputs.toString())
                }
            }
        }
        else {
            username = prompt("Please enter a username between 5 and 25 characters long")
        }

    }
    var validInput = false;
    while (!validInput) {
        if (password.length > 2 && password.length <= 25) {
            var usedBadInputs = []
            var containsValidLetters = true
            for (const substring of badInputs) {
                if (password.includes(substring)) {
                    var containsValidLetters = false
                    usedBadInputs.push(substring)
                }
            }
            var validInput = containsValidLetters
            if (!validInput) {
                if (password.length > 2 && password.length <= 25) {
                    password = prompt("Password cannot contain " + usedBadInputs.toString())
                }
            }
        }
        else {
            password = prompt("Please enter a password between 5 and 25 characters long")
        }
    }

    sendDataToServerForLogin([username, password, email, variant])


}



function sendDataToServerForLogin(credentials) {
    event.preventDefault()
    const backendUrl = 'http://127.0.0.1:5000'
    fetch(`${backendUrl}/backendVerification`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status} - ${response.statusText}`);
            }

            return response.json();
        })
        .then(data => {
            console.log("Received data from the server:", data);
            if (data.permissionGranted === 1) {
                window.location.href = '/moderator';
                localStorage.setItem("username", credentials[0])
                localStorage.setItem("security", "admin")
            }
            else if (data.permissionGranted === 2) {
                if (localStorage.getItem("comeFrom") == null){
                    window.location.href = '/home';
                }
                else{
                    localStorage.setItem("username", credentials[0])
                    localStorage.setItem("security", "user")
                    console.log(localStorage.getItem("comeFrom"))
                    if (localStorage.getItem("comeFrom") === "/history_page" || localStorage.getItem("comeFrom") === "/bedtest"){
                        console.log("1")
                        console.log(`${localStorage.getItem("comeFrom")}${localStorage.getItem("username")}`)
                        window.location.href = `${localStorage.getItem("comeFrom")}/${localStorage.getItem("username")}`
                        return
                    }
                    else{window.location.href = localStorage.getItem("comeFrom")}
                }
                
            }
            else if (data.permissionGranted === 3) {
                window.location.href = '/';
                alert("incorrect username or password please try again")
                console.log('incorrect username/password combo');
            }
            else if (data.permissionGranted === 4) {
                window.location.href = '/';
                alert("successfully created new login details")
                console.log('added user to database');
            } else {
                console.log('Login failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function openForm() {
    document.getElementById("myForm").style.display = "block";
}
function openCloseForm() {
    if (document.getElementById("myForm").style.display === "none") {
        document.getElementById("myForm").style.display = "block";
    } else {
        document.getElementById("myForm").style.display = "none";
    }
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}
function interesting() {
    localStorage.getItem("security")
}
function showPassword() {
    var x = document.getElementById("password")
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password"
    }
}

function logout(){
    localStorage.setItem("username", null)
    localStorage.setItem("comeFrom", "/")
    console.log("gee whizz")
}