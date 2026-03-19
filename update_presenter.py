import re

with open('src/views/PresenterView.vue', 'r') as f:
    content = f.read()

# 1. Remove the static CSS vars from .presenter-theme
content = re.sub(r'  /\* Dynamic vars modified by JS \*/\n  --arabic-size: 3\.5rem;\n  --trans-size: 2rem;\n  --translit-size: 1\.5rem;\n', '', content)

# 2. Change slide-content max-width from 1200px to 90%
content = re.sub(r'  max-width: 1200px;', r'  max-width: 90%;', content)

with open('src/views/PresenterView.vue', 'w') as f:
    f.write(content)
