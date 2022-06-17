let friendsListOpen = false;
let messagesListOpen = false;

function toggleFriendsList() {
    if (friendsListOpen) {
        document.getElementById('friends-list').style.display = 'none';
        friendsListOpen = false;
    } else {
        document.getElementById('friends-list').style.display = 'flex';
        friendsListOpen = true;
    }
}
function toggleMessagesList() {
    if (messagesListOpen) {
        document.getElementById('friends-messages-list').style.display = 'none';
        messagesListOpen = false;
    } else {
        document.getElementById('friends-messages-list').style.display = 'flex';
        messagesListOpen = true;
    }
}
function openFriendsList() {
    document.getElementById('friends-list').style.display = 'flex';
    friendsListOpen = true;
}
function openMessagesList() {
    document.getElementById('friends-messages-list').style.display = 'flex';
    messagesListOpen = true;
}
function closeFriendsList() {
    document.getElementById('friends-list').style.display = 'none';
    friendsListOpen = false;
}
function closeMessagesList() {
    document.getElementById('friends-messages-list').style.display = 'none';
    messagesListOpen = false;
}
function showFriendsListVariation(variation) {
    hideAllFriendLists();
    document.getElementById(`friends-list-${variation}`).style.display = 'flex';
}
function hideAllFriendLists() {
    for (let variation of ['list', 'requests', 'blocked', 'recent']) { document.getElementById(`friends-list-${variation}`).style.display = 'none'; }
}
