
document.addEventListener("DOMContentLoaded", function() {
    // socket stuff
    socket.on('friend_request', (data) => {
        let elem = htmlToElement(`<li>${data.user_tag}<span style="float:right"><button>+</button></span></li>`)
        document.getElementById('friends-list-requests').appendChild(
            elem
        )
        elem.querySelector('span > button').addEventListener('click', () => {
            reqAddFriend(data.user_id)
        });
        showFriendsNotification('general');
        showFriendsNotification('requests');
    });
});