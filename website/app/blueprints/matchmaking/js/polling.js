// long polling if user has joined queue and we havent received a return value from our join_match task

//

/*
So the flow basically goes:

    1. User clicks find match button
    2. This immediately adds the user to the player cache
    3. Create a socket connection to the server and then initialize our redis user_id state with the socket id
    4. Trigger a task in the task queue and return back the task_id to the user
    5. Start polling that task id to check for if match was found.
    6. If match is never found, then simply update their redis state to confirm that polling has ceased, ( and actually cease polling of course )
    7. If match is found before we even finish our polling then kill polling and call connection to game server
*/



let pollMatchmakingInterval = setInterval(() => {
    fetch(
        '/poll_matchmaking' + '?' + new URLSearchParams({
            foo: 'value',
            bar: 2
        }),
        {
            mode: "no-cors",
        }
    )
    .then(res => res.json())
    .then(json => console.log(json))
    .catch(error => console.warn(error));
}, 500);

function acknowledgePollResult(params) {
    // sends notification to backend that we have, in fact received an update on our poll status
    // and I think the insinuation here is that we did not find a match result
    // if we did find a match result, then we would just call the function which sends match found notification
    // to each user found
}
