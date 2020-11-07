from flask_script import Manager

from web_app.app import create_app

app = create_app()
app.app_context().push()

manager = Manager(app)


if __name__ == "__main__":
    manager.run()
