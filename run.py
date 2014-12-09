# -*- coding: utf-8 -*-

import os
import random
import string
import subprocess
from eve import Eve
from flask import request,redirect

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

    lyra2dir = "./Lyra2/bin/"

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

    def pos_fetched_item_callback(response):
            response['id'] = response['_id']
            del response['_id']
            # del response['_created']
            # del response['_updated']
            # del response['_links']
            del response['password']
            del response['lyra2salt']
            del response['lyra2klen']
            del response['lyra2tcost']
            del response['lyra2nrows']

    def pos_fetched_users_callback(response):
            for item in response['_items']:
                item['id'] = item['_id']
                del item['_id']
                # del item['_created']
                # del item['_updated']
                # del item['_links']
                del item['password']
                del item['lyra2salt']
                del item['lyra2klen']
                del item['lyra2tcost']
                del item['lyra2nrows']

            response['items'] = response['_items']
            del response['_items']
            # del response['_links']
            # del response['_meta']

    app = Eve()

    @app.route('/auth', methods=['POST'])
    def auth():
        username = request.form.get('username')
        password = request.form.get('password')

        users = app.data.driver.db['users']
        account = users.find_one({'username': username})

        if not account:
            return redirect(request.url_root + 'users/denied')

        cmd =  lyra2dir + "Lyra2" +" "+ username +" "+ password +" "+ account['lyra2salt'] +" "
        cmd += account['lyra2klen'] +" "+ account['lyra2tcost'] +" "+ account['lyra2nrows']
        password_hash = subprocess.check_output(cmd, shell=True).strip()

        if str(password_hash) == str(account['password']):
            return redirect(request.url_root + 'users/' + str(account['_id']))
        else:
            return redirect(request.url_root + 'users/denied')

    app.on_insert_users += pre_insert_callback
    app.on_update_users += pre_update_callback
    app.on_fetched_item_users += pos_fetched_item_callback
    app.on_fetched_resource_users += pos_fetched_users_callback

    app.run(host=host, port=port)
