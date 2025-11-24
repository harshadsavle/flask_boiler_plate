from celery import Celery
from core.config import Config
celery = Celery(
    "my_app",
    broker=Config.get_redis_url(),
    backend=Config.get_redis_url()
)
# celery -A core.celery_app.celery purge
# celery -A core.celery_app.celery control shutdown

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)
celery.conf.timezone = 'UTC'
celery.conf.task_default_queue = "data_extraction"
celery.autodiscover_tasks(['ai_agent.init_agent'],force=True)

