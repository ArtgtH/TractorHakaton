from celery import Celery

from .send_mail import send_email

app_celery = Celery(
	'tasks',
	broker='redis://localhost:6379/0',
	backend='redis://localhost:6379/0'
)


@app_celery.task
def send_email_to_user(receiver, result, topic):
	try:
		send_email(receiver, result, topic)
	except Exception as e:
		return e
	else:
		return 'success'
