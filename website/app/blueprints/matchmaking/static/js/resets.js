
function resetAllMatchmaking(data) {
    console.log("resetting all")
    clearQueueTimer();
    clearMatchFound();
}

document.addEventListener("DOMContentLoaded", function() {
    socket.on('reset_all_matchmaking', resetAllMatchmaking);
});