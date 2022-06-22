function getFriendMessageHtml(message) {
    return `<div class="friends-messages-friend-message">${message}</div>`
}

function getSelfMessageHtml(message) {
    return `<div class="friends-messages-self-message">${message}</div>`
}

function getMessagesHtml(messages, self_id) {
    let html = '<div>';
    for (let msg of messages) {
        html += (msg.user_id == self_id) ? getSelfMessageHtml(msg.message) : getFriendMessageHtml(msg.message);
    }
    html+='</div>'
    return html;
}
