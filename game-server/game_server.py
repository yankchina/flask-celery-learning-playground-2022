from app import create_app

from app import create_app
from app.blueprints.game_two.models.game import Game

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return { 'Game': Game }

if __name__ == "__main__":
    app.run(port=5001, debug=True)