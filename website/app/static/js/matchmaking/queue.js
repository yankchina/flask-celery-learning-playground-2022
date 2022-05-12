let queueTimerInterval;

function startQueueTimer(timeInQueue) {
    let outerDiv = document.getElementById('queue-timer');
    outerDiv.style.display = 'block';
    let div = document.getElementById('queue-timer-count');
    div.innerText = timeInQueue;
    queueTimerInterval = setInterval(() => {
        div.innerText = parseInt(div.innerText) + 1;
    }, 1000);
}

function endQueueTimer() {
    let outerDiv = document.getElementById('queue-timer');
    outerDiv.style.display = 'none';
    clearInterval(queueTimerInterval);
}