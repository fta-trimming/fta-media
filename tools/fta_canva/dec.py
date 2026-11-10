import json,sys,base64,re
d=json.load(open(sys.argv[1]));t=d[0]['text']
m=re.search(r'"?([A-Za-z0-9+/=]{1000,})"?',t)
open(sys.argv[2],'wb').write(base64.b64decode(m.group(1)))
