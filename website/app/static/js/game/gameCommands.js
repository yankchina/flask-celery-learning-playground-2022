
function addToScore() {
    console.log(gameSocket);
    gameSocket.emit('add_to_score', {'he': 'test', 'there': 't2'})
}