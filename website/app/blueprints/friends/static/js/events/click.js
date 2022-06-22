
// types:

// messages
// general
// list
// requests
// blocked
// recent


document.querySelector('#friends-general-btn').addEventListener('click', (e) => {
    toggleFriendsList();
    resetFriendsNotification('general');
});
document.querySelector('#friends-messages-btn').addEventListener('click', (e) => {
    toggleMessagesList();
    resetFriendsNotification('messages');
});
for (let type of ['list', 'requests', 'blocked', 'recent']) {
    document.getElementById(`friends-${type}-btn`).addEventListener('click', () => {
        showFriendsListVariation(type);
        resetFriendsNotification(type);
    });
}
document.querySelectorAll('.friends-list-friend').forEach((el) => el.addEventListener('click', clickUserTagInFriendsList));
document.querySelectorAll('#friends-messages-friends-friends div').forEach((el) => el.addEventListener('click', clickUserTagInMessages));


function clickUserTagInFriendsList(e) {
    openMessagesList();
    closeFriendsList();

    // this is to handle for if the span with the user_tag is clicked
    let userTag = (e.target.firstChild.innerText === undefined) ? e.target.innerText : e.target.firstChild.innerText;

    focusUserTag(userTag);
    resetUserTagNotification(userTagElem);
}

function clickUserTagInMessages(e) {
    let userTagElem = e.target;
    let userTag = userTagElem.dataset.userTag;
    focusUserTag(userTag);
    resetUserTagNotification(userTagElem);
}