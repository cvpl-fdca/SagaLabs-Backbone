from apscheduler.schedulers.background import BackgroundScheduler

from . import azureTasks
from tasks.azureTasks import *

# Create a scheduler instance
scheduler = BackgroundScheduler()


def start_tasks():
    # Add tasks to the scheduler
    scheduler.add_job(azureTasks.poll_resources, 'interval', minutes=1)

    # Start the scheduler
    scheduler.start()
