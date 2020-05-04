from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from iseeya import create_app, db
sio, app=create_app()
db.create_all(app=app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def runserver(debug=False, use_reloader=False):
    sio.run(app, port=5000, debug=debug, use_reloader=use_reloader)


if __name__ == '__main__':
    manager.run()