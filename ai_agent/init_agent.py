from celery_app import celery
from core.api_call import api_call
from core.logger import info
from ai_agent.service import run_agent


def trigger_callback(callback:dict,data:dict,jobid:str,extra:dict):
    # do something with the callback
    data = {
        'jobid': jobid,
        'extra': extra,
        'data': data
    }
    api_call(url=callback['url'],data=data)
    return {}

@celery.task
def init_agent(file_content,callback:dict,jobid:str,extra:dict):
    info(f"Agent 1 Job started")
    data = run_agent(file_content)
    trigger_callback(callback,data,jobid,extra)
    info(f"Agent 1 Job finished")