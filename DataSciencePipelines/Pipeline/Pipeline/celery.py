# @author Hongwei
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab

app = Celery('Pipeline',
             broker='amqp://',
             backend='amqp://',
             include=['Pipeline.tasks'])

app.conf.timezone = 'US/Eastern'

app.conf.beat_schedule = {
    # Execute every two minutes
    'run-every-2-minute': {
        'task': 'tasks.run',
        'schedule': crontab(minute='*/2')
    }

    # Executes every Day morning at 8:30 a.m.
    # 'run-every-day-morning': {
    #     'task': 'tasks.run',
    #     # 'schedule': crontab(hour=8, minute=30),
    # },

    # 'add-every-10-seconds': {
    #     'task': 'tasks.add',
    #     'schedule': 10.0,
    #     'args': (16, 16)
    # },

    # 'add-every-1-minute': {
    #     'task': 'tasks.add',
    #     'schedule': crontab(minute='*/2'),
    #     'args': (16, 16)
    # },
}


# for test
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, add.s(3, 3), name='add every 10')
#
#     # # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )
#
#


if __name__ == '__main__':
    app.start()
