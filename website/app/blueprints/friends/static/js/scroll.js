
function scrollMessagesToBottom(behavior='smooth') {
    document.querySelector('#friends-messages-user-messages').scrollTo({
        top: 999999,
        left: 100,
        behavior: behavior
    });
}
function scrollPartyToBottom(behavior='smooth') {
    document.querySelector('#friends-party-user-messages').scrollTo({
        top: 999999,
        left: 100,
        behavior: behavior
    });
}