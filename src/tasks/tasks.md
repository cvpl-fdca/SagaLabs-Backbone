# Tasks Module

The `tasks` module contains background tasks that are offloaded from the main application to ensure quick response times
from our API endpoints. These tasks might involve long-running processes or periodic tasks that need to be executed
separately from the main application thread.

The structure of the `tasks` module is as follows:

```bash
tasks/
├── init.py
├── azureTasks.py
├── deploy_tasks.py
└── vpn_tasks.py
```

Each Python file within the `tasks` module corresponds to a specific category of tasks related to our application:

- `azure_tasks.py`: Contains tasks related to interfacing with Azure, such as running commands on a range of Azure
  resources or polling Azure for updates.

- `deploy_tasks.py`: Contains tasks related to deployment processes.

- `vpn_tasks.py`: Contains tasks related to VPN operations, such as listing all VPN users or delivering VPN files to
  servers.

These tasks are typically run asynchronously and may be scheduled to run periodically or triggered by certain actions in
the main application.

To use these tasks, import the necessary task file in your Python code like so: `from src.tasks import azure_tasks`.
