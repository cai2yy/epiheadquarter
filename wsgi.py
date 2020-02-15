import os
from dotenv import load_dotenv
from epihq.extensions import db

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from epihq import create_app  # noqa

app = create_app('production')
