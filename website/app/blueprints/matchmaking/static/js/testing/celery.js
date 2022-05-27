function testCelery() {
    $.ajax({
        url: `/test_task`,
        success: function (result) {
            console.log(result);
        },
        error: function (request, status, error) {
            console.log(request.responseText);
        },
    });
}