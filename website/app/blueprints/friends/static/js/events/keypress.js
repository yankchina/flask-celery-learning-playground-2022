



document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('send-friend-message-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === 'NumpadEnter') {

            // convert this to an async function and await the result. If successful, then run addMessageToFriendMessages
            reqSendMessageToFriend(e.target.value, friendUserTagSelected);

            addMessageToFriendMessages(e.target.value, "self");
            scrollMessagesToBottom();
            clearInput(e.target);
        }
    });

    document.getElementById('send-party-message-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === 'NumpadEnter') {
            // send message to party

            scrollPartyToBottom();
            clearInput(e.target);
        }
    });
});