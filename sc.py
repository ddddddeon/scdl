import soundcloud
import re
import os
import sys
import requests
from unidecode import unidecode

CLIENT_ID = os.getenv('SOUNDCLOUD_CLIENT_ID')
usernames = sys.argv[1::]
client = soundcloud.Client(client_id=CLIENT_ID)

for username in usernames:
    user = client.get('/users', q=username)
    try:
        uid = user[0].obj['id']
        tracks = client.get('/users/' + str(uid) + '/tracks')
    except:
        print 'username not found :('
        continue

    def bail_out(_file, filename):
        _file.close()
        os.remove(filename)
        print '  :('

    if not os.path.exists(username):
        os.makedirs(username)

    for t in tracks:
        filename = unidecode(t.obj['title']) + '.mp3'
        filename = re.sub("[/\*\~\\$]", "", filename)
        filename = username + '/' + filename
        f = open(filename, 'wb');
        sys.stdout.write("[SAVING] %s -> %s" % (t.obj['title'], filename))
        sys.stdout.flush()

        try:
            stream_url = t.obj['stream_url']
        except KeyError:
            bail_out()
            continue
        try:
            stuff = requests.get(stream_url + '?client_id=' + CLIENT_ID, allow_redirects=True)
        except:
            bail_out()
            continue

        for chunk in stuff.iter_content(chunk_size=512 * 1024): 
            if chunk:
                f.write(chunk)
        f.close()
        print u'  \u2713'
