import re
import base64
SEEK_REGEX = r'^[+|-]([1-9]|[1-5][0-9]|60)$'

# print(re.match(SEEK_REGEX, '+7').groups())

print(base64.urlsafe_b64encode(b'www.google.com').decode('utf-8'))
