
function focusUserTagMessages(userTag) {
    let list = document.getElementById('friends-messages-friends-friends');
    let userTagElem = document.querySelector(`[data-user-tag="${userTag}"]`);
    if (!userTagElem) {
        // create one
        userTagElem = htmlToElement(`
            <div data-user-tag="${userTag}">
                ${userTag}
            </div>`
        );
        list.insertBefore(userTagElem, list.firstChild);
        userTagElem.addEventListener('click', clickUserTagInMessages);
    }
    userTagElem.click();
    // unsetAllMessagesUserTagActive();
    // setMessagesUserTagActive(userTag);
}