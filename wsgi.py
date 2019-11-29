#!/home7/jmsansco/public_html/mypyproject2/ENV/bin/python

from flup.server.fcgi import WSGIServer
from application import create_app

app = create_app()

WSGIServer(app).run()