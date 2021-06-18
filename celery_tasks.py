from celery import Celery

app = Celery('celery_tasks', broker='pyamqp://guest@localhost//', backend='rpc://',)


@app.task
def add(x, y):
    return x + y
