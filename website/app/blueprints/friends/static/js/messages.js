

function getMessageHtml(messages, self_id) {
    let html = '<div>';
    for (let msg of messages) {
        html += `<div class="${msg.user_id == self_id ? 'friends-messages-friend-message' : 'friends-messages-self-message'}">
${msg.message}
</div>`
    }
    html+='</div>'
    return html;
}
