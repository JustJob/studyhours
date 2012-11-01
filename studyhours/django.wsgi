import os,sys

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

sys.path.append('/usr/local/www/studyhours')
sys.path.append('/usr/local/www/studyhours/studyhours')

def application(environ, start_response):
    environ['DJANGO_SETTINGS_MODULE'] = 'studyhours.settings'
    print 'environ is ', environ
    try:
        status = '200 OK'
        output = 'Hello World!1'

        return _application(environ, start_response)
    except Exception as inst:
        response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(inst.__str__())))]
        start_response(status, response_headers)
        return [inst.__str__()]
