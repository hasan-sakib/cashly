try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import os
from cashly.app import create_app

app = create_app("production")
