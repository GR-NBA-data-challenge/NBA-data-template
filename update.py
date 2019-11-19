import urllib.request
urllib.request.urlretrieve('https://github.com/GR-NBA-data-challenge/NBA-data-template/raw/master/libupdate.py', 'libupdate.py')
import libupdate
libupdate.main()