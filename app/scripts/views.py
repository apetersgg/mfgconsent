from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import scripts
from .. models import Follow, User, Role, Permission, Post, Comment
from .. import db

import ipdb

@scripts.route('/build_users_and_posts', methods=['GET'])
def build_users_and_posts():

    print ''
    print 'Delete Posts'
    posts_deleted = Post.query.delete()
    print '    number of rows deleted: %s' % posts_deleted

    print ''
    print 'Delete Comments'
    comments_deleted = Comment.query.delete()
    print '    number of rows deleted: %s' % comments_deleted

    print ''
    print 'Delete Follows'
    follows_deleted = Follow.query.delete()
    print '    number of rows deleted: %s' % follows_deleted

    print ''
    print 'Delete Users'
    users_deleted = User.query.delete()
    print '    number of rows deleted: %s' % users_deleted

    print ''
    print 'Check for current users'

    users = User.query.all()
    if users:
        for user in users:
            print '    username: %s' % user.username
    else:
        print '    No users'

    print ''
    print 'Build 4 individual users:'
    if not User.query.filter_by(username='transreductionist').first():
        user1 = User(email='transreductionist@gmail.com',
                     username='transreductionist',
                     password='Password',
                     role_id=1,
                     confirmed=True,
                     name='Aaron Peters',
                     location='Arlington',
                     about_me='Trying to get an App online.')
        db.session.add(user1)
        print '    user1: %s' % user1
    else:
        print '    user1 already exists'

    if not User.query.filter_by(username='dradpeters').first():
        user2 = User(email='soarbuildingbridges@gmail.com',
                     username='dradpeters',
                     password='Password',
                     role_id=1,
                     confirmed=True,
                     name='Dr Peters',
                     location='Arlington',
                     about_me='Working towards NLP solution.')
        db.session.add(user2)
        print '    user2: %s' % user2
    else:
        print '    user2 already exists'

    if not User.query.filter_by(username='apeters').first():
        user3 = User(email='apeters@ggoutfitters.com',
                     username='apeters',
                     password='Password',
                     role_id=1,
                     confirmed=True,
                     name='GG Peters',
                     location='Arlington',
                     about_me='Practicing Flask with Miguel Grinberg.')
        db.session.add(user3)
        print '    user3: %s' % user3
    else:
        print '    user3 already exists'

    if not User.query.filter_by(username='comcastpete').first():
        user4 = User(email='transreductionist@comcast.net',
                     username='comcastpete',
                     password='Password',
                     role_id=1,
                     confirmed=True,
                     name='Comcast Peters',
                     location='Arlington',
                     about_me='Heroku and API work.')
        db.session.add(user4)
        print '    user4: %s' % user4
    else:
        print '    user4 already exists'
    print ''

    db.session.commit()

    print 'generate fake users'
    print ''
    User.generate_fake(100)

    print 'generate fake posts'
    print ''
    Post.generate_fake(100)

    db.session.commit()
