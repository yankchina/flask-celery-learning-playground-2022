

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
    let [members, messages, leader_id, is_leader] = await reqGetFriendPartyDetails();
    if (messages === "not in party") {
        setNotInPartyInPartyDiv();
        return;
    }
    setMembersInFriendPartyDiv(members, leader_id, is_leader);
    setMessagesInFriendPartyDiv(messages);
    scrollPartyToBottom('auto');
}

function getFocusedFriendTagMessages() {
    return document.querySelector(`[data-user-tag].active`).dataset.userTag;
}