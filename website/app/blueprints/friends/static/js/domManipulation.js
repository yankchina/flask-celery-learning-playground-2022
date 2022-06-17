function moveChildToFirstChild(child, parent) {
    parent.removeChild(child);
    parent.insertBefore(child, parent.firstChild);
}

function setMessagesInFriendMessagesDiv(messages, self_id) {
    document.getElementById('friends-messages-user-messages').innerHTML = htmlToElement(getMessageHtml(messages, self_id));
}