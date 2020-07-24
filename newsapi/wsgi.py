from django.core.wsgi import get_wsgi_application

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise



from whitenoise import WhiteNoise


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsapi.settings')

application = get_wsgi_application()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

application = WhiteNoise(application, root=os.path.join(BASE_DIR,'/static'))

# application = DjangoWhiteNoise(application)
