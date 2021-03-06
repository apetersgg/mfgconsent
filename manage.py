#!/usr/bin/env python

import os
from app import create_app, db
from app.models import User, Role, Follow, Post, Comment

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand

from app.scripts.views import build_users_and_posts

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

server = Server(host='192.168.75.1', port=8080)

@manager.command
def deploy():
    from flask.ext.migrate import upgrade
    from app.models import Role, User
    upgrade()
    Role.insert_roles()
    User.add_self_follows()

@manager.command
def run_scripts():
    build_users_and_posts()


@manager.command
def test():
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
