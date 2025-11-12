function viewHistory() {
    console.log(localStorage.getItem("username"))
    if (localStorage.getItem("username") === "null" || localStorage.getItem("username") === null){
        alert("Please log in to view your history page")
        localStorage.setItem("comeFrom", "/history_page")
        location.href = "loginPage"
        
    }
    else{
        location.href = '/history_page/'+localStorage.getItem("username");
    }
}
function viewBookings() {
    if (localStorage.getItem("username") === "null" || localStorage.getItem("username") === null){
        alert("Please log in to view your bookings page")
        localStorage.setItem("comeFrom", "/bedtest")
        location.href = "loginPage"
        
    }
    else{
        location.href = '/bedtest/'+localStorage.getItem("username");
    }
}
