function clearInput(elem) {
    elem.value = '';
}

function moveChildToFirstChild(child, parent) {
    parent.removeChild(child);
    parent.insertBefore(child, parent.firstChild);
}

function setMessagesInFriendMessagesDiv(messages) {
    let elem = document.getElementById('friends-messages-user-messages')
    elem.innerHTML = '';
    elem.appendChild(htmlToElement(getFriendMessagesHtml(messages)));
}
function setMembersInFriendPartyDiv(members, leader_id, is_leader) {
    let elem = document.getElementById('friends-party-friends-members');
    elem.innerHTML = '';
    elem.appendChild(htmlToElement(getFriendPartyMembersHtml(members, leader_id, is_leader)));
}
function setMessagesInFriendPartyDiv(messages) {
    let elem = document.getElementById('friends-party-user-messages');
    elem.innerHTML = '';
    elem.appendChild(htmlToElement(getFriendPartyMessagesHtml(messages)));
}
function setNotInPartyInPartyDiv() {
    let elem = document.getElementById('friends-party-user-messages');
    elem.innerHTML = 'Not in party.';
}

function addMessageToFriendMessages(message, type="self") {
    // type options: ['self', 'friend']
    document.querySelector('#friends-messages-user-messages > div').appendChild(
        (type == "self") ? htmlToElement(getSelfMessageHtml(message)) : htmlToElement(getFriendMessageHtml(message))
    )
}
function addMessageToPartyMessages(messageDict) {
    let elem = document.getElementById('friends-party-user-messages');
    elem.appendChild(htmlToElement(getFriendPartyMessageHtml(messageDict)));
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