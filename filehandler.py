import os


def check_episodes_status(anime, directory):

    os.path.isdir("{}:\Plex\Anime\{}\Season 01".format(directory, anime))
    print(len([name for name in os.listdir(
        "{}:\Plex\Anime\{}\Season 01".format(directory, anime))]))
    os.path.isfile('./path_of_file')


def check_if_files_exist(anime):
    exist_in_J = os.path.isdir("J:\Plex\Anime\{}".format(anime))
    exist_in_G = os.path.isdir("G:\Plex\Anime\{}".format(anime))

    if exist_in_G == True or exist_in_J == True:
        return True
    else:
        return False
