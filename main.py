import os
os.chdir(os.getcwd())
from dotenv import load_dotenv
from backend import create_app  # noqa


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print(os.getcwd())
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app('production')
