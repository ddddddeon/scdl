import soundcloud
import sys
import requests

CLIENT_ID = 'YOUR CLIENT ID HERE'
username = sys.argv[1]

client = soundcloud.Client(client_id=CLIENT_ID)
user = client.get('/users', q=username)
uid = user[0].obj['id']
tracks = client.get('/users/' + str(uid) + '/tracks')
for t in tracks:
    filename = str(t.obj['title'] + '.mp3')
    f = open(filename, 'wb');
    print "Saving %s (%s)" % (t.obj['id'], t.obj['title'], t.obj['stream_url'])
    stream_url = t.obj['stream_url']
    stuff = requests.get(stream_url + '?client_id=' + CLIENT_ID, allow_redirects=True)
    for chunk in stuff.iter_content(chunk_size=512 * 1024): 
        if chunk:
            f.write(chunk)
    f.close()
