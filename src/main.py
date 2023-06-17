# main.py
from . import create_app
from .tasks.taskScheduler import start_tasks

app = create_app()

# Start the scheduled tasks
start_tasks()
