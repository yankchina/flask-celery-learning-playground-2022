function getFriendMessageHtml(message) {
    return `<div class="friends-messages-friend-message">${message}</div>`
}

function getSelfMessageHtml(message) {
    return `<div class="friends-messages-self-message">${message}</div>`
}

function getFriendMessagesHtml(messages) {
    let html = '<div>';
    for (let msg of messages) {
        html += (msg.who == 'self') ? getSelfMessageHtml(msg.message) : getFriendMessageHtml(msg.message);
    }
    html+='</div>'
    return html;
}

function getFriendPartyMessageHtml(msg) {
    return `<div class="friends-party-message">${msg.user_tag}:&ensp;${msg.message}</div>`
}

function getFriendPartyMessagesHtml(messages) {
    let html = '<div>';
    for (let msg of messages) {
        html += getFriendPartyMessageHtml(msg);
    }
    html+='</div>'
    return html;
}
