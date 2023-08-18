import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('mysql-connector-python')
install('python-dateutil')
install('numpy')
install('numba')
install('python-dotenv')