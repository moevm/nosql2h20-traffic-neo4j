from flask_script import Manager
from neomodel import config

from web_app.app import create_app

config.DATABASE_URL = 'bolt://neo4j:testpass@neo4j:7687'

app = create_app()
app.app_context().push()
manager = Manager(app)


if __name__ == "__main__":
    manager.run()
