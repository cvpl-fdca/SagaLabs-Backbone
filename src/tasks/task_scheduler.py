from apscheduler.schedulers.background import BackgroundScheduler

from . import azure_tasks
from .azure_tasks import *

# Create a scheduler instance
scheduler = BackgroundScheduler()


def start_tasks():
    # Add tasks to the scheduler
    scheduler.add_job(azure_tasks.poll_resources, 'interval', minutes=1)

    # Start the scheduler
    scheduler.start()
