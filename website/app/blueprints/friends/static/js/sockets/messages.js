
document.addEventListener("DOMContentLoaded", function() {

    socket.on('friend_message', (data) => {
        console.log(data);
        let userTag = data.user_tag
        let msg = data.message;

        if (!document.querySelector(`[data-user-tag="${userTag}"]`)) {
            addUserTagToMessages(data.user_tag);
        }

        if (messagesListOpen) {
            let focusedFriendTag = getFocusedFriendTagMessages();
            if (focusedFriendTag != userTag) {
                showUserTagNotification(userTag);
            } else { // we are already focused on this friend
                addMessageToFriendMessages(msg, "friend");
            }
        } else {
            showFriendsNotification('messages');
            showUserTagNotification(userTag);
        }
    });
});