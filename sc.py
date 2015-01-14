import soundcloud
import re
import os
import sys
import requests
from unidecode import unidecode
import argparse

# you will need to set an environment variable with
# your soundcloud client_id from https://developers.soundcloud.com
CLIENT_ID = os.getenv('SOUNDCLOUD_CLIENT_ID')
client = soundcloud.Client(client_id=CLIENT_ID)

parser = argparse.ArgumentParser(description='scdl')
parser.add_argument('-f', '--favs', action='store_true')
parser.add_argument('user', nargs='+', type=str)
args = parser.parse_args()

usernames = args.user

def bail_out(_file, filename):
    _file.close()
    os.remove(filename)
    print u'  \u2718'

# call soundcloud api to get user ids, 
# make directories for usernames,
# call api again to get list of trax,
# then GET all the trax & write blobs to disk
def save_trax(client, username, trax_or_favs):
    user = client.get('/users', q=username)

    try:
        uid = user[0].obj['id']
        if trax_or_favs in ['favorites', 'tracks']:
            tracks = client.get('/users/' + str(uid) + '/' + trax_or_favs)
        else:
            print "must be either favorites or tracks"
            exit(1)
    except:
        raise Exception("user not found :(")
        
    if trax_or_favs == 'favorites':
        username += '/favs'

    if not os.path.exists(username):
        os.makedirs(username)
    
    for t in tracks:
        # remove any characters that might fuck up a unix box
        filename = unidecode(t.obj['title']) + '.mp3'
        filename = re.sub("[/\*\~\\$]", "", filename)
        filename = username + '/' + t.obj['user']['permalink'] + ' - ' + filename
        
        # make the file <username>/<trak>.mp3 
        f = open(filename, 'wb');
        sys.stdout.write("[SAVING] %s -> %s" % (t.obj['title'], filename))
        sys.stdout.flush()

        try:
            stream_url = t.obj['stream_url']
        except KeyError:
            bail_out(f, filename)
            continue
        
        # getting shady now...
        # GET the trak's stream url w/ our client_id >:D
        try:
            stuff = requests.get(stream_url + '?client_id=' + CLIENT_ID, allow_redirects=True)
        except:
            bail_out(f, filename)
            continue

        # ...and write it to a file XD XD 
        for chunk in stuff.iter_content(chunk_size=512 * 1024): 
            if chunk:
                f.write(chunk)
        f.close()
        print u'  \u2713' # great job!

for username in usernames:
    
    save_trax(client, username, 'tracks')
    if args.favs:
        save_trax(client, username, 'favorites')

