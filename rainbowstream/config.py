import json
import re
import os
import os.path

from .db import *

db = RainbowDB()

# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)


def load_config(filepath):
    """
    Load config from filepath
    """
    try:
        with open(filepath) as f:
            content = ''.join(f.readlines())
            match = comment_re.search(content)
            while match:
                content = content[:match.start()] + content[match.end():]
                match = comment_re.search(content)
        return json.loads(content)
    except IOError:
        return None

# Load default colorset
c = {}
default_config = 'rainbowstream/colorset/default.json'
data = load_config(default_config)
if data:
    for d in data:
        c[d] = data[d]
db.theme_store('default')
# Load user's colorset
rainbow_config = os.environ.get(
    'HOME',
    os.environ.get(
        'USERPROFILE',
        '')) + os.sep + '.rainbow_config.json'
data = load_config(rainbow_config)
if data:
    for d in data:
        c[d] = data[d]
    db.theme_update('user')
