function testRedis() {
    $.ajax({
        url: `/test_redis`,
        success: function (result) {
            console.log(result);
        },
        error: function (request, status, error) {
            console.log(request.responseText);
        },
    });
}
function checkRedisQueue() {
    $.ajax({
        url: `/check_redis_queue`,
        success: function (result) {
            console.log(result.queue);
        },
        error: function (request, status, error) {
            console.log(request.responseText);
        },
    });
}