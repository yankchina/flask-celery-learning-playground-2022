import time
# from app import create_app, db, cli
from app import create_app
# from app.models import User, Post, Message, Notification, Task

app = create_app()
# cli.register(app)

@app.shell_context_processor
def make_shell_context():
    pass
    # return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
    #         'Notification': Notification, 'Task': Task}
    # return {'User': User, 'Post': Post, 'Message': Message,
    #         'Notification': Notification, 'Task': Task}
async def poll_task_list():
    i=0
    while True:
        print(i, flush=True)
        time.sleep(1)
        i+=1

if __name__ == "__main__":
    poll_task_list()
    app.run(port=5000, debug=True)