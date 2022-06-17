// types:

// messages
// general
// list
// requests
// blocked
// recent

function showFriendsNotification(type="", increment=true) {
    let notifDiv = document.getElementById(`friends-${type}-notification-div`);
    if (increment) {notifDiv.innerText = parseInt(notifDiv.innerText) + 1;}
    notifDiv.style.display = "flex";
}
function resetFriendsNotification(type="") {
    let notifDiv = document.getElementById(`friends-${type}-notification-div`);
    notifDiv.innerText = 0;
    notifDiv.style.display = "none";
}