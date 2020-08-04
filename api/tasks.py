from django.template import Template, Context
from quick_publisher.celery import app
from users.models import Profile
from demo.cellery import app
 
 
# @celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=1))
@app.task
def reset_number_request():
    for nor in Profile.objects.all():
        print(nor)
        nor.num_of_requests=0
        nor.save()