

function focusUserTag(userTag) {
    let userTagElem = document.querySelector(`[data-user-tag="${userTag}"]`);
    if (!userTagElem) {
        userTagElem = addUserTagToMessages(userTag)
        initializeUserTagElem(userTagElem);
    }
    let list = document.getElementById('friends-messages-friends-friends');
    let messages = reqGetFriendMessages(userTag);
    moveChildToFirstChild(userTagElem, list);
    removeActiveFromMessageUserTags();
    addActiveToMessageUserTag(userTagElem);
    friendUserTagSelected = userTag;
}

function getFocusedFriendTagMessages() {
    return document.querySelector(`[data-user-tag].active`);
}