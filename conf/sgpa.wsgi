activate_this = '/var/www/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import os
from django.core.wsgi import get_wsgi_application


os.environ['DJANGO_SETTINGS_MODULE'] = 'sgpa.setting_production'

application = get_wsgi_application()
