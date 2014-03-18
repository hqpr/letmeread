apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)

sys.path.append('/home/letmerea/domains/letmeread.ru/django/web/')
sys.path.append('/home/letmerea/domains/letmeread.ru/django/web/web/')
sys.path.append('/home/letmerea/virtualenv/web/')
sys.path.append('/home/letmerea/virtualenv/web/lib/python2.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()