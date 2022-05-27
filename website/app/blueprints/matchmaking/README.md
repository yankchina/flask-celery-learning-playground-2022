Installation instructions


1. You must point any asset bundler to this directory. An example:

matchmaking_js = Bundle(
    'blueprints/matchmaking/js/**/*.js',
    filters='jsmin',
    output='dist/matchmaking-js.js')
assets.register('matchmaking-js', matchmaking_js)
matchmaking_js.build(force=True)
