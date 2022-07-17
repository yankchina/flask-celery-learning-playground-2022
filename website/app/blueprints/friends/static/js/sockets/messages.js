
document.addEventListener("DOMContentLoaded", function() {

    socket.on('friend_message', (data) => {
        console.log(data);
        let userTag = data.user_tag
        let msg = data.message;

        if (!getElemFromUserTag(userTag)) {
            addUserTagToMessages(data.user_tag);
        }

        if (messagesListOpen) {
            let focusedFriendTag = getFocusedFriendTagMessages();
            if (focusedFriendTag != userTag) {
                showUserTagNotification(userTag);
            } else { // we are already focused on this friend
                addMessageToFriendMessages(msg, "friend");
                scrollMessagesToBottom();
            }
        } else {
            showFriendsNotification('messages');
            showUserTagNotification(userTag);
            let focusedFriendTag = getFocusedFriendTagMessages();
            if (focusedFriendTag != userTag) {
                showUserTagNotification(userTag);
            } else { // we are already focused on this friend
                addMessageToFriendMessages(msg, "friend");
            }
        }
    });
});