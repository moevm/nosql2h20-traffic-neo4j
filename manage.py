from flask_script import Manager

from web_app.app import create_app
from web_app.db import connect

app = create_app()
app.app_context().push()

manager = Manager(app)
connect.connect(url='bolt://neo4j:testpass@localhost:7687')


if __name__ == "__main__":
    manager.run()
