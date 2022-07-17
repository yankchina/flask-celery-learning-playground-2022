let hasPulledPartyMessages = false;


function pullPartyMessages() {
    if (!hasPulledPartyMessages) {
        hasPulledPartyMessages = true;
        reqGetFriendPartyMessages();
    }
}

function sendPartyInvite(userId) {
    reqSendPartyInvite(userId);

}

function getPartyInviteHtml(userTag) {
    let htmlString = `<div class="friends-party-invite" data-party-invite-user-tag=${userTag}>
        <h6>Party Invite</h6>
        <h4>${userTag}</h4>
        <div>
            <button onclick="acceptPartyInvite('${userTag}')">Accept</button>
            <button onclick="declinePartyInvite('${userTag}')">Decline</button>
        </div>
    </div>`.replace(/>\s+</g, "><"); // replace removes whitespace between tags
    return htmlToElement(htmlString);
}

function removePartyInvite(userTag) {
    document.querySelector(`[data-party-invite-user-tag="${userTag}"]`).remove();
}

function acceptPartyInvite(userTag) {
    reqAcceptPartyInvite(userTag);
    removePartyInvite(userTag);
}

function declinePartyInvite(userTag) {
    reqDeclinePartyInvite(userTag);
    removePartyInvite(userTag);
}

// function getFriendMessageHtml(message) {
//     return `<div class="friends-messages-friend-message">${message}</div>`
// }

// function getSelfMessageHtml(message) {
//     return `<div class="friends-messages-self-message">${message}</div>`
// }

// function getFriendMessagesHtml(messages) {
//     let html = '<div>';
//     for (let msg of messages) {
//         html += (msg.who == 'self') ? getSelfMessageHtml(msg.message) : getFriendMessageHtml(msg.message);
//     }
//     html+='</div>'
//     return html;
// }
