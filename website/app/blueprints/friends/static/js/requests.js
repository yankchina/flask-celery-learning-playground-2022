
function reqAddFriend(user_id) {
    let formData = new FormData();
    formData.append('user_id', user_id);
    fetch('/friends/add_friend', {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(json => console.log(json))
    .catch(error => console.warn(error));
}
function reqRemoveFriend(user_id) {
    let formData = new FormData();
    formData.append('user_id', user_id);
    fetch('/friends/remove_friend', {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(json => console.log(json))
    .catch(error => console.warn(error));
}

function reqGetFriendMessages(userTag) {
    let formData = new FormData();
    formData.append('user_tag', userTag);
    fetch('/friends/get_friend_messages', {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(json => console.log(json))
    .catch(error => console.warn(error));
}

function reqSendMessageToFriend(message, userTag) {
    let formData = new FormData();
    formData.append('user_tag', userTag);
    formData.append('message', message);
    fetch('/friends/send_friend_message', {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(json => console.log(json))
    .catch(error => console.warn(error));
}