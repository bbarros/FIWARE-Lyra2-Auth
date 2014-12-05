# -*- coding: utf-8 -*-

"""
    Eve Demo
    ~~~~~~~~

    A demostration of a simple API powered by Eve REST API.

    The live demo is available at eve-demo.herokuapp.com. Please keep in mind
    that the it is running on Heroku's free tier using a free MongoHQ
    sandbox, which means that the first request to the service will probably
    be slow. The database gets a reset every now and then.

    :copyright: (c) 2014 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os
import random
import string
import subprocess
from eve import Eve

if __name__ == '__main__':
    # Heroku support: bind to PORT if defined, otherwise default to 5000.
    if 'PORT' in os.environ:
        port = int(os.environ.get('PORT'))
        # use '0.0.0.0' to ensure your REST API is reachable from all your
        # network (and not only your computer).
        host = '0.0.0.0'
    else:
        port = 5000
        host = '127.0.0.1'

    lyra2dir = "/home/bbarros/Code/Lyra2-FIWARE/bin/"

    def pre_insert_callback(item):
            item[0]['lyra2salt'] = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
            print 'Lyra2 salt: "%s"' % item[0]['lyra2salt']

            cmd =  lyra2dir + "Lyra2" +" "+ item[0]['username'] +" "+ item[0]['password'] +" "+ item[0]['lyra2salt'] +" "
            cmd += item[0]['lyra2klen'] +" "+ item[0]['lyra2tcost'] +" "+ item[0]['lyra2nrows']
            print 'Lyra2 cmd: "%s"' % cmd

            password_hash = subprocess.check_output(cmd, shell=True).strip()
            item[0]['password'] = password_hash
            print 'Lyra2 output: "%s"' % password_hash

    def pre_update_callback(item, original):
            new_password = False

            if not item.get('username'):
                item['username'] = original['username']
            if not item.get('password'):
                item['password'] = original['password']
                new_password = True
            if not item.get('lyra2klen'):
                item['lyra2klen'] = original['lyra2klen']
                new_password = True
            if not item.get('lyra2tcost'):
                item['lyra2tcost'] = original['lyra2tcost']
                new_password = True
            if not item.get('lyra2nrows'):
                item['lyra2nrows'] = original['lyra2nrows']
                new_password = True

            if new_password:
                item['lyra2salt'] = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])

                cmd =  lyra2dir + "Lyra2" +" "+ item['username'] +" "+ item['password'] +" "+ item['lyra2salt'] +" "
                cmd += item['lyra2klen'] +" "+ item['lyra2tcost'] +" "+ item['lyra2nrows']

                password_hash = subprocess.check_output(cmd, shell=True).strip()
                item['password'] = password_hash

    app = Eve()

    app.on_insert_users += pre_insert_callback
    app.on_update_users += pre_update_callback

    app.run(host=host, port=port)
