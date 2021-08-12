import json
import os

from .hooks import load_hooks
PLUGIN_PATH = os.path.dirname(__file__)

def load(app):
  load_hooks()
  
