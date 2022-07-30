

document.addEventListener("DOMContentLoaded", function() {
    socket.on('party_invite', (data) => {
        document.getElementById('friends-party-invite-container').appendChild(getPartyInviteHtml(data.user_tag));
    });
    socket.on('party_message', (data) => {
        if (!partyTabOpen) {
            showFriendsNotification('party');
        }
        addMessageToPartyMessages(data.message_dict);
        scrollPartyToBottom();
    });
    socket.on('user_left_party', (data) => {
        addLeftPartyMessage(data.user_tag);
    });
});