import os
import subprocess
import sys
import platform

# Determine current platform
is_windows = platform.system() == 'Windows'

# Define the activate script depending on the OS
activate_script = '.\\venv\\Scripts\\activate' if is_windows else './venv/bin/activate'

# Create a Python virtual environment
subprocess.run([sys.executable, '-m', 'venv', 'venv'])

# Format command differently for Windows
if is_windows:
    pip_install_command = f'{activate_script} && pip install -r requirements.txt'
else:
    pip_install_command = f'. {activate_script}; pip install -r requirements.txt'

# Pip install requirements
subprocess.run(pip_install_command, shell=True, executable="/bin/bash" if not is_windows else None)

# Define paths differently for Windows and Unix-based systems
src_dir = os.path.join(os.getcwd(), 'src')
main_file = os.path.join(src_dir, 'main.py')

# Add 'src' directory to PYTHONPATH
os.environ['PYTHONPATH'] = f"{os.environ.get('PYTHONPATH', '')};{src_dir}" if is_windows else f"{os.environ.get('PYTHONPATH', '')}:{src_dir}"

# Set FLASK_APP environment variable
os.environ['FLASK_APP'] = main_file
