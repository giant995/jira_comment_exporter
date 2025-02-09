import requests
import json
import os
from datetime import datetime

JIRA_BASE_URL = "https://mrdltd.atlassiant.net"
JIRA_API_TOKEN = os.environ["JIRA_API_TOKEN"]
