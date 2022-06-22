



document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('send-friend-message-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' || e.key === 'NumpadEnter') {
            reqSendMessageToFriend(e.target.value, friendUserTagSelected);
        }
    });
});