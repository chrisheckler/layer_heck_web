from charms.reactive import when, when_not, set_flag
from charmhelpers.core import hookenv


@when('snap.installed.flask-gunicorn-nginx')
@when_not('heck-web.http.port.available')
def set_available_status_and_open_port():
    """
    Sets the status and flag, and opens the http port.
    """
    hookenv.status_set('active', "Heck-Web Installed")
    hookenv.open_port(5000)
    set_flag('heck-web.http.port.available')
