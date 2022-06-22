function moveChildToFirstChild(child, parent) {
    parent.removeChild(child);
    parent.insertBefore(child, parent.firstChild);
}

function setMessagesInFriendMessagesDiv(messages, self_id) {
    document.getElementById('friends-messages-user-messages').innerHTML = htmlToElement(getMessagesHtml(messages, self_id));
}

function addMessageToFriendMessages(message, type="self") {
    // type options: ['self', 'friend']
    document.querySelector('#friends-messages-user-messages > div').appendChild(
        (type == "self") ? getSelfMessageHtml(message) : getFriendMessageHtml(message)
    )
}

function addUserTagToMessages(userTag) {
    let list = document.getElementById('friends-messages-friends-friends');
    let userTagElem = htmlToElement(`
        <div data-user-tag="${userTag}">
            ${userTag}
            <span class="friends-user-tag-notification-div">0</span>
        </div>`
    );
    list.insertBefore(userTagElem, list.firstChild);
    userTagElem.addEventListener('click', clickUserTagInMessages);
    return userTagElem;
}