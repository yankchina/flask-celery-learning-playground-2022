let checkingTaskStatus;

function joinMatchmaking() {
    $.ajax({
        url: `/join_matchmaking`,
        success: function (result) {
            showNotification(result);
            if (result.success) {
                startQueueTimer(1);

                if (!checkingTaskStatus) {
                    checkingTaskStatus = setInterval(() => {
                        checkFindMatchTaskStatus(result.location);
                    }, 1000);
                }
            }
        },
        error: function (request, status, error) {
            console.log(request.responseText);
        },
    });
}
