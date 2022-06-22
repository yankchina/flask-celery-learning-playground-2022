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
function showUserTagNotification(userTag, increment=true) {
    console.log('adding');
    let notifDiv = document.querySelector(`[data-user-tag="${userTag}"] > .friends-user-tag-notification-div`);
    if (increment) {notifDiv.innerText = parseInt(notifDiv.innerText) + 1;}
    notifDiv.style.display = "flex";
}
function resetUserTagNotification(userTagElem) {
    let notifDiv = userTagElem.querySelector('span');
    notifDiv.innerText = 0;
    notifDiv.style.display = "none";
}