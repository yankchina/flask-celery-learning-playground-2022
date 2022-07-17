let friendsListOpen = false;
let messagesListOpen = false;
let partyListOpen = false;

function toggleFriendsList() { (friendsListOpen) ? closeFriendsList() : openFriendsList(); }
function toggleMessagesList() { (messagesListOpen) ? closeMessagesList() : openMessagesList(); }
function togglePartyList() { (partyListOpen) ? closePartyList() : openPartyList(); }

function openFriendsList() {
    document.getElementById('friends-list').style.display = 'flex';
    friendsListOpen = true;
}
function openMessagesList() {
    document.getElementById('friends-messages-list').style.display = 'flex';
    messagesListOpen = true;
    scrollMessagesToBottom();
}
function closeFriendsList() {
    document.getElementById('friends-list').style.display = 'none';
    friendsListOpen = false;
}
function closeMessagesList() {
    document.getElementById('friends-messages-list').style.display = 'none';
    messagesListOpen = false;
}
function openPartyList() {
    document.getElementById('friends-party-list').style.display = 'flex';
    focusParty();
    partyListOpen = true;
    scrollPartyToBottom();
}
function closePartyList() {
    document.getElementById('friends-party-list').style.display = 'none';
    partyListOpen = false;
}
function showFriendsListVariation(variation) {
    hideAllFriendLists();
    document.getElementById(`friends-list-${variation}`).style.display = 'flex';
}
function hideAllFriendLists() {
    for (let variation of ['list', 'requests', 'blocked', 'recent']) { document.getElementById(`friends-list-${variation}`).style.display = 'none'; }
}
