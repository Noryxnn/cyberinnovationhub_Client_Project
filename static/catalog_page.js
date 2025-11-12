

let active = false;

//For now we shall use test data. This is the basket
// Data needs to be added to DB
// This data needs to get to the serer to be stored in db
var basket = [];

var date = '';
//09/19/22 13:55:26

function selectTrainSation() {
    if (basket.indexOf("Train Station ") === -1) {
        basket.push("Train Station");
    }

    document.getElementById("numberID")
}

function selectTrafficLight() {
    if (basket.indexOf("Traffic Light ") === -1) {
        basket.push("Traffic Light");
    }
}

function selectPowerPlant() {
    if (basket.indexOf("Power Plant ") === -1) {
        basket.push("Power Plant");
    }
}

function selectHospital() {
    if (basket.indexOf("Hospital ") === -1) {
        basket.push("Hospital");
    }
}

function selectPrison() {
    if (basket.indexOf("Prison ") === -1) {
        basket.push("Prison");
    }
}

// function selectGeneral() {
//     if(basket.indexOf("Train Station ") === -1) {
//         basket.push("Train Station");
//     }
//     if(basket.indexOf("Traffic Light ") === -1) {
//         basket.push("Traffic Light");
//     }
//     if(basket.indexOf("Power Plant ") === -1) {
//         basket.push("Power Plant");
//     }
//     if(basket.indexOf("Hospital ") === -1) {
//         basket.push("Hospital");
//     }
//     if(basket.indexOf("Prison ") === -1) {
//         basket.push("Prison");
//     }
// }

function dropDownBasket() {

}

function getItems() {
    var items = basket.toString();

    return items;
}

function getUserName() {
    
    console.log(localStorage.getItem("username"))
    console.log(typeof(localStorage.getItem("username")))
    if (localStorage.getItem("username") === "null") {
        alert("please login to make a booking");
        location.href = "/loginPage";
        localStorage.setItem("comeFrom", "/catalog");
    }
    else {
        var user = localStorage.getItem("username")
        return user;

    }
   
    
}

function getDate() {
    fullDate = document.getElementById("bookingDate").value + ' ' + document.getElementById("bookingTime").value;
    // if(fullDate === '') {
    //     dates = new Date();
    //     month = dates.getMonth() + 1
    //     fullDate = dates.getFullYear() + '-' + month + '-' + dates.getDate();
    // }
    fullDate.toString();
    if (fullDate === ""){
        fullDate == "now"
    }
    return fullDate;
}

function sendData(type) {
    

    var usernameFromLocal = getUserName();
    console.log(usernameFromLocal)
    console.log(typeof(usernameFromLocal))
    if (usernameFromLocal !== undefined){
        console.log(usernameFromLocal)
    location.href = '/save';
    $.post("/save", {
        
        userName: usernameFromLocal,
        items: getItems(),
        date: getDate(),
        type: type,
    })}

}

function getMinDate() {
    dates = new Date();
    month = dates.getMonth() + 1
    document.getElementById("bookingDate").setAttribute("min", dates.getFullYear() + '-' + month + '-' + dates.getDate());
}

function openBasket() {
    document.getElementById("basket").innerHTML = '';
    for (var i = 0; i < basket.length; i++) {
        const element = document.createElement("p");
        const item = document.createTextNode(basket[i]);
        element.appendChild(item);
        document.getElementById("basket").appendChild(element);
    }
}

function clearBasket() {
    document.getElementById("basket").innerHTML = '';
}
// // function displayBasket(i) {
// //     document.getElementById("userBasket").appendChild(i);
// // }

// // function removeBasket() {
// //     for(let i = 0; i<basket.length; i++) {
// //         let textNode = document.createTextNode(basket[i]);
// //         document.getElementById("userBasket").removeChild(textNode);
// //     }
// // }

// function itemDivClickActive(i) {
//     alert("xcfdsgdf");
//     document.getElementById("userBasket").appendChild(i);
// }

// function itemDivClickDeactive(i) {
//     document.getElementById("userBasket").removeChild(i);
// }