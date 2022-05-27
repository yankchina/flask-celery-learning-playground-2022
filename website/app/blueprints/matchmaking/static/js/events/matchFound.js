
document.addEventListener("DOMContentLoaded", function() {
    let key;

    socket.on('match_found', handleMatchFoundEmit);
    socket.on('clear_match_found', clearMatchFound);

    function handleMatchFoundEmit(data) {
        key = data['key'];
        document.querySelector('#match-found-notification').style.background = 'rgb(125, 125, 199)';
        document.querySelector('#match-found-notification').style.display = "flex";
    }
    function acceptMatch() {
        socket.emit('match_found_choice', {'key': key, 'choice': 'accept'});
        document.querySelector('#match-found-notification').style.background = 'green';
    }
    function declineMatch() {
        socket.emit('match_found_choice', {'choice': 'decline'});
        document.querySelector('#match-found-notification').style.background = 'red';
    }
    document.querySelector('#accept-match-found-btn').addEventListener('click', acceptMatch );
    document.querySelector('#decline-match-found-btn').addEventListener('click', declineMatch );
});
function clearMatchFound() {
    key = null;
    hideMatchFound();
}
function hideMatchFound() {
    document.querySelector('#match-found-notification').style.display = "none";
}