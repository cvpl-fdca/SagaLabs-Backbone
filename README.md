<div align="center">

<h1>🔌 SagaLabs-Backbone</h1>

<a href="/LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg?longCache=true&style=flat-square" alt="licence"></a>
<a href="https://github.com/cvpl-fdca/Sagalabs-Backbone/issues"><img src="https://img.shields.io/github/issues/cvpl-fdca/SagaLabs-Backbone" alt="issues"></a>
<br>

<img src="https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white"/>
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
<a href="https://www.linkedin.com/company/foreningen-for-danske-cyber-alumner"><img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" /></a>

</div>

The purpose of SagaLabs Backbone is to serve as a central system that handles API communication and control of SagaLabs environments. It acts as a bridge between different components and services in the SagaLabs architecture, enabling efficient communication, management, and coordination of activities across these environments. This contributes to a more seamless and efficient operation of the SagaLabs environment as a whole.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have Python 3.11 or later installed on your machine. You can download Python from the [official website](https://www.python.org/downloads/).

### Installation

Clone the repository:
```bash
git clone https://github.com/cvpl-fdca/sagalabs_backbone.git
cd SagaLabs-Backbone
```

Then, depending on your operating system, run one of the following scripts to set up a virtual environment and install the necessary packages (assuming you have `virtualenv` installed):

**Windows:**
```cmd
virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Adding a New API Endpoint

To add a new API endpoint, create a new route and resource class in the appropriate file in the `api` directory. Here's an example:

```python
@api.route('/new-endpoint')
class NewEndpoint(Resource):
    def get(self):
        return {'message': 'This is a new endpoint!'}
```
Remember to add any necessary input validation, error handling, and documentation.


### Running the application

```bash
flask run
```

### Setting Up Redis

1. Install Docker Desktop:
   - Download and install Docker Desktop for your operating system from the official Docker website: <https://www.docker.com/products/docker-desktop>
   - Follow the installation instructions specific to your operating system.

2. Pull the Redis Docker image:
   - Open a terminal or command prompt.
   - Run the following command to pull the latest Redis image from Docker Hub:
     ```
     docker pull redis
     ```

3. Start a Redis container:
   - Run the following command to start a Redis container named `local-redis`:

 ```
 docker run --name local-redis -p 6379:6379 -d redis
 ```


- This command maps port 6379 inside the Redis container to port 6379 on your local machine. You can modify the port mapping as needed.

1. Verify Redis is running:
   - You can check if the Redis container is running by executing the following command:
     ```
     docker ps
     ```
   - You should see the `local-redis` container listed along with its status.

## Setting Up Pylint

Pylint is a tool that we use to maintain a consistent coding style across the project. It's already installed in your virtual environment via the `requirements.txt` file, but you'll also need the Pylint extension for Visual Studio Code.

Follow these steps to set up Pylint:

1. **Install the Pylint extension in VS Code**: Open Visual Studio Code, go to the Extensions view (you can press `Ctrl+Shift+X`), and search for "Pylint". Click on the first result, which should be [Pylint by Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint), and click the Install button.

2. **Enable Pylint in your VS Code settings**: Open the settings (you can press `Ctrl+,`), search for "Python Linting Enabled", and make sure it's checked. Then, search for "Python Linting Pylint Enabled", and make sure it's also checked.

3. **Configure Pylint rules**: If we have a specific Pylint configuration for this project, you'll find a `.pylintrc` file in the root directory. This file contains the rules that Pylint will enforce. If you want to know more about each rule, you can find a list of all Pylint rules and their explanations in the [Pylint documentation](http://pylint.pycqa.org/en/latest/technical_reference/features.html).

Now, whenever you save a Python file in VS Code, Pylint will check your code and highlight any issues it finds. You can also see a list of all issues by opening the Problems view (`Ctrl+Shift+M`).

