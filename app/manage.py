from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from settings import app, db
from app_models import DIDNumber


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
    db.create_all()
