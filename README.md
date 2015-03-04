# scdl
Given a soundcloud user, download all their trax and, if you like, all their favs.

## Installation
Download this repo from github by clicking the download link, or:
`git clone https://github.com/ddddddeon/scdl.git`

### Get a SoundCloud API key:
- Go to http://soundcloud.com/you/apps/new to register a new app and get an API key.
- Copy your CLIENT ID to clipboard,
- Set the following environment variable in your shell. Put it in your .bashrc to make it permanent:
- `export SOUNDCLOUD_CLIENT_ID=your-client-id-here`

#### If you don't have pip:
`sudo easy_install soundcloud requests argparse unidecode`

#### If you have pip:
`cd /path/to/scdl`
`sudo pip install -r requirements.txt`

## Running scdl:
- If you're on a mac, enter the bash shell: `bash`
- `cd /path/to/scdl`
- `python sc.py user-name-here`
- To download a user's favorites also, add the `-f` flag: `python sc.py user-name-here -f`
- To get multiple users' trax, just add more arguments: `python sc.py user-name-one user-name-two`