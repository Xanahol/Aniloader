from qbittorrent import Client

qb = Client('http://192.168.1.135:8080/')

qb.login('Xana', 'Xanaholovous01')
# not required when 'Bypass from localhost' setting is active.
# defaults to admin:admin.
# to use defaults, just do qb.login()

torrents = qb.torrents()

for torrent in torrents:
    print("{}".format(torrent['name']))