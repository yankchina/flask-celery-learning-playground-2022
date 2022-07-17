
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

async function reqGetFriendMessages(userTag) {
    let formData = new FormData();
    formData.append('user_tag', userTag);
    const res = await fetch('/friends/get_friend_messages', {
        method: "POST",
        body: formData
    })
    const result = await res.json();
    const messages = await result.messages;
    return messages;
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

async function reqGetFriendPartyMessages() {
    const res = await fetch('/friends/get_party_messages', {
        method: "GET",
    })
    const result = await res.json();
    console.log(result);
    const messages = await result.messages;
    return messages;
}

async function reqSendPartyInvite(userId) {
    let formData = new FormData();
    formData.append('user_id', userId);
    const res = await fetch('/friends/send_party_invite', {
        method: "POST",
        body: formData
    })
    const result = await res.json();
    console.log(result);
}

async function reqDeclinePartyInvite(userTag) {
    let formData = new FormData();
    formData.append('user_tag', userTag);
    const res = await fetch('/friends/decline_party_invite', {
        method: "POST",
        body: formData
    })
    const result = await res.json();
    console.log(result);
}

async function reqAcceptPartyInvite(userTag) {
    let formData = new FormData();
    formData.append('user_tag', userTag);
    const res = await fetch('/friends/accept_party_invite', {
        method: "POST",
        body: formData
    })
    const result = await res.json();
    console.log(result);
}