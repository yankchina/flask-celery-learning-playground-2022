
function getElemFromUserTag(userTag) {
    return document.querySelector(`[data-user-tag="${userTag.trim()}"]`);
}