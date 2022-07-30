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

function getLeftPartyMessageHtml(userTag) {
    return `<div class="friends-party-message">${userTag} left the party.</div>`
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

function getFriendPartyLeaderHtml(member) {
    return `<div class="friends-party-member"><span class="crown">*</span>${member.user_tag}</div>`
}
function getFriendPartyMemberHtml(member, is_leader=false) {
    return `<div class="friends-party-member">${member.user_tag} ${is_leader ? '<span class="promotion">^</span><span class="kick">X</span>' : ''}</div>`
}
function getFriendPartyMembersHtml(members, leader_id, is_leader) {
    let html = '<div>';
    // strip leader and add first
    for (let m of members) {
        if (m.user_id === leader_id) {
            html += getFriendPartyLeaderHtml(m);
            break;
        }
    }

    for (let m of members) {
        if (m.user_id !== leader_id) {
            html += getFriendPartyMemberHtml(m, is_leader);
        }
    }
    html+='</div>'
    return html;
}
