import os
import logger
from config import directories


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

# TODO
# Give back the amount of files in the animes directory


def check_if_anime_up_to_date(anime_name, episodes_available):
    for directory in directories:
        anime_path = os.path.isdir('{}:\Plex\Anime\{}'.format(directory, anime_name))
        if anime_path:
            episodes_downloaded = len([name for name in os.listdir(
                anime_path) if os.path.isfile(os.path.join(anime_path, name))])
            if int(episodes_available - episodes_downloaded) == 0:
                return None
            else:
                new_episodes = int(episodes_available - episodes_downloaded)
                return new_episodes
    try:
        os.mkdir('{}:\Plex\Anime\{}'.format(directories[-1], anime_name))
        return episodes_available
    except:
        logger.error("Couldn't create directory: " + '{}:\Plex\Anime\{}'.format(directories[-1], anime_name)
 
