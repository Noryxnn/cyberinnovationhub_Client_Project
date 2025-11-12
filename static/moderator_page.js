function denyRequest(bookingID) {
    location.href = '/moderator/deny/'+bookingID;
}

// on accept we need to send this data to the bookings page... Therefor all data needs to be sent here then to server then to the other page
// I have a better way. Each item should have and accepted/denied property, if property is set to accepted then display.
// I can send ingo to url in pyton this can update database 

function acceptRequest(bookingID) {
    location.href = '/moderator/accept/'+bookingID;
}   