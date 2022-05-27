function testResponse() {
    $.ajax({
        url: "/test_response",
        success: function (result) {
            console.log(result);
        },
        error: function (request, status, error) {
            console.log(request.responseText);
        },
    });
}

function testGameServerResponse() {
    $.ajax({
        url: "http://127.0.0.1:5001/test_response",
        success: function (result) {
            console.log(result);
        },
        error: function (request, status, error) {
            console.log(request.responseText);
        },
    });
}
function testCreateGame() {
    $.ajax({
        url: "http://127.0.0.1:5001/create_game",
        success: function (result) {
            console.log(result);
        },
        error: function (request, status, error) {
            console.log(request.responseText);
        },
    });

}
function testRequestWebsiteToGameServer() {
    $.ajax({
        url: "/test_request_to_game_server",
        success: function (result) {
            console.log(result);
        },
        error: function (request, status, error) {
            console.log(request.responseText);
        },
    });

}