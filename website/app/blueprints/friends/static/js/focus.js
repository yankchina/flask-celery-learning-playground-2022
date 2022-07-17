

async function focusUserTag(userTag) {
    let userTagElem = getElemFromUserTag(userTag);
    if (!userTagElem) {
        userTagElem = addUserTagToMessages(userTag)
        initializeUserTagElem(userTagElem);
    }
    let list = document.getElementById('friends-messages-friends-friends');

    let messages = await reqGetFriendMessages(userTag);
    setMessagesInFriendMessagesDiv(messages);

    moveChildToFirstChild(userTagElem, list);
    removeActiveFromMessageUserTags();
    addActiveToMessageUserTag(userTagElem);
    friendUserTagSelected = userTag;
    scrollMessagesToBottom('auto');
}

async function focusParty() {
    let list = document.getElementById('friends-party-friends-friends');
    let messages = await reqGetFriendPartyMessages();
    if (messages === "not in party") {
        setNotInPartyInPartyDiv();
        return;
    }
    setMessagesInFriendPartyDiv(messages);
    scrollPartyToBottom('auto');
}

function getFocusedFriendTagMessages() {
    return document.querySelector(`[data-user-tag].active`).dataset.userTag;
}