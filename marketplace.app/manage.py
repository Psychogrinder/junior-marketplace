from flask_script import Manager
from marketplace import app, db
from flask_migrate import init, migrate, upgrade


manager = Manager(app)


@manager.command
def make_migrations():
    try:
        init()
    except:
        pass
    with app.app_context():
        migrate()
        upgrade()


@manager.command
def init_db():
    init()
    with app.app_context():
        db.configure_mappers()
        db.create_all()
        db.session.commit()


if __name__ == "__main__":
    manager.run()
