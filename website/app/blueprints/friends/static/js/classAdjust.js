

function setMessagesUserTagActive(userTag) {
    userTagElem = document.querySelector(`[data-user-tag="${userTag}"]`).classList.add('active');
}
function addActiveToMessageUserTag(elem) {
    elem.classList.add('active');
}
function removeActiveFromMessageUserTags() {
    document.querySelectorAll('#friends-messages-friends-friends div').forEach((el) => el.classList.remove('active'));
}