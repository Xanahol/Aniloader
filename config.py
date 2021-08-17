import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
except:
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    except:
        print("There was an error retrieving your IP")
        print("A solution for this Problem may not be implemented yet")

#Example
ip_4 = ip_address
torrent_port = "8080"
directories = ['F:\Plex\Anime', 'E:\Plex\Anime', 'G:\Plex\Anime']

# Set True on Development
DEV = False