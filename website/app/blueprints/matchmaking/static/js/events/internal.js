
document.addEventListener("DOMContentLoaded", function() {
    socket.on('ping_find_match', (data) => {
        if (!checkingTaskStatus) {
            checkingTaskStatus = setInterval(() => {
                checkFindMatchTaskStatus(data.location);
            }, 1000);
        }
    })
});

function checkFindMatchTaskStatus(url) {
    return fetch(url, { mode: "no-cors", })
    .then(res => res.json())
    .then(json => {
        if (json.task_status == 'SUCCESS') {
            clearInterval(checkingTaskStatus);
            checkingTaskStatus = undefined;
        }
    })
    .catch(error => console.warn(error));
}