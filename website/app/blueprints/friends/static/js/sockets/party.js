

document.addEventListener("DOMContentLoaded", function() {
    socket.on('party_invite', (data) => {
        document.getElementById('friends-party-invite-container').appendChild(getPartyInviteHtml(data.user_tag));
    });
});