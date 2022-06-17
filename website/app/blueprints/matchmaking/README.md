Installation instructions


1. You must point any asset bundler to this directory. An example:

matchmaking_js = Bundle(
    'blueprints/matchmaking/js/**/*.js',
    filters='jsmin',
    output='dist/matchmaking-js.js')
assets.register('matchmaking-js', matchmaking_js)
matchmaking_js.build(force=True)


Possible outcomes for a match found:

    1. All users accept match       => all users are redirected to game server
    2. All users decline match      => all users are removed from queue
    3. Any number of users decline  => users who accepted stay in queue and are placed at front of the queue
    4. User leaves site             => If a match is found for that user and they are in queue, then they are registered as a decline


What happens when a party joins a queue:

    We add all members to the queue 