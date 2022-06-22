
document.addEventListener("DOMContentLoaded", function() {
    // socket stuff
    socket.on('friend_request', (data) => {
        document.getElementById('friends-list-requests').appendChild(
            htmlToElement(`<li>${data.user_tag}<span style="float:right"><button onclick="reqAddFriend(${data.user_tag})"></span></li>`)
        )
        showFriendsNotification('general');
        showFriendsNotification('requests');
    });
});