from charms.reactive import when, when_not, set_flag, endpoint_from_flag
from charmhelpers.core import hookenv
import json


@when('snap.installed.flask-gunicorn-nginx')
@when_not('heck-web.http.port.available')
def set_available_status_and_open_port():
    """
    Sets the status and flag, and opens the http port.
    """
    hookenv.status_set('active', "App installed")
    hookenv.open_port(5000)
    set_flag('heck-web.http.port.available')


@when('database.connected')
@when_not('heck-web.db.created')
def create_web_db():
    """ Create heck-web db
    """
    hookenv.status_set("maintenance", "Creating heck-web MySQL database")
    database = endpoint_from_flag('database.connected')
    database.configure('heckweb', 'heckweb')
    set_flag('heck-web.db.created')


@when('database.available', 'heck-web.db.created')
@when_not('heck-web.db.acquired')
def get_db_conn(database):
    """ Get/Set mysql connection details when db is available
    """
    db_info = json.dumps({'host': database.db_host(),
                          'port': 3306,
                          'user': database.username('heckweb'),
                          'password': database.password('heckweb'),
                          'database': database.database('heckweb')})
    hookenv.log(db_info)
    hookenv.status_set('active', db_info)
    set_flag('heck-web.db.acquired')
