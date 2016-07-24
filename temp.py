import re

s = 'asdf=5;iwantthis123jasd'
result = re.search('df=5;(.*)123', s)
print result.group(1)