from config import directories
import os
import logger
import pathlib
import re
import shutil


def check_episodes_status(anime, directory):
    os.path.isdir("{}:\Plex\Anime\{}\Season 01".format(directory, anime))
    print(len([name for name in os.listdir(
        "{}:\Plex\Anime\{}\Season 01".format(directory, anime))]))
    os.path.isfile('./path_of_file')


def detect_season_on_path(path):
    season_raw = re.split(r'\\', path)[-1]
    season = re.findall('Season \d.*', season_raw)[0]
    s = re.findall('\d.*', season)[0]
    return s


def detect_anime_on_path(path):
    title = re.split(r'\\', path)[-2]
    return title


def detect_episode_from_old_name(file_name):
    print(file_name)
    episode = re.findall(r'- \d+', file_name)[0]
    e = re.findall('\d.*', episode)[0]
    return e


def check_if_files_exist(anime):
    exist_in_J = os.path.isdir("J:\Plex\Anime\{}".format(anime))
    exist_in_G = os.path.isdir("G:\Plex\Anime\{}".format(anime))

    if exist_in_G == True or exist_in_J == True:
        return True
    else:
        return False


def check_directory_for_anime(anime_name, season):
    for directory in directories:
        dir = '{}\{}\Season 0{}'.format(directory, anime_name, season)
        anime_path = os.path.isdir(dir)
        if anime_path:
            return dir
    default_dir = directories[0] + '\{}\Season 0{}'.format(anime_name, season)
    return default_dir


def remove_episodes(anime_name, season):
    for directory in directories:
        anime_has_dir = os.path.isdir(
            directory + '\{}'.format(anime_name))
        if anime_has_dir:
            complete_dir = directory + \
                '\{}\Season 0{}'.format(anime_name, season)
            season_has_dir = os.path.isdir(
                directory + '\{}\Season 0{}'.format(anime_name, season))
            if season_has_dir:
                for filename in os.listdir(complete_dir):
                    file_path = os.path.join(complete_dir, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        logger.error(
                            'Failed to delete %s. Reason: %s' % (file_path, e))


def check_if_anime_up_to_date(anime_name, season, episodes_available):
    for directory in directories:
        anime_has_dir = os.path.isdir(
            directory + '\{}'.format(anime_name))
        if anime_has_dir:
            complete_dir = directory + \
                '\{}\Season 0{}'.format(anime_name, season)
            season_has_dir = os.path.isdir(
                directory + '\{}\Season 0{}'.format(anime_name, season))
            if season_has_dir:
                episodes_downloaded = len([name for name in os.listdir(
                    complete_dir) if os.path.isfile(os.path.join(complete_dir, name))])
                if int(episodes_available) - episodes_downloaded == 0:
                    return None
                else:
                    new_episodes = int(episodes_available) - episodes_downloaded
                    return new_episodes
            else:
                anime_dir = directory + '\{}'.format(anime_name)
                season_dir = 'Season 0' + season
                os.mkdir(os.path.join(anime_dir, season_dir))
                return check_if_anime_up_to_date(anime_name, season, episodes_available)

    anime_dir = directories[0] + '\{}'.format(anime_name)
    season_dir = 'Season 0' + season
    os.mkdir(anime_dir)
    os.mkdir(os.path.join(anime_dir, season_dir))
    return check_if_anime_up_to_date(anime_name, season, episodes_available)


def select_paths(directory):
    anime_list = os.walk(directory)
    dir_list = []
    for anime in anime_list:
        if re.search('Season ', anime[0]):
            dir_list.append(anime[0])
    logger.info('Collected every anime on '+directory)
    return dir_list


def rename(path_list):
    for path in path_list:
        season = detect_season_on_path(path)
        anime = detect_anime_on_path(path)
        logger.info('Renaming '+anime+' Season '+season)
        rename_anime(anime, season, path)
        logger.info('Renaming successful')


def rename_anime(anime, season, path):
    for part in pathlib.Path(path).iterdir():
        # if part.is_dir():
        #     print("A DIR" + str(part))
        if part.is_file():
            name = part.stem
            if not re.search(r'.mkv', name):
                directory = part.parent
                name = name+'.mkv'
                part.rename(pathlib.Path(directory, name))
            if re.search('1080p', name):
                episode = detect_episode_from_old_name(name)
                directory = part.parent
                name = anime+' - S0'+season+'E0'+episode+'.mkv'
                part.rename(pathlib.Path(directory, name))
            if re.search(r'- S\dE\d', name):
                episode = detect_fix_name(name)
                directory = part.parent
                name = anime+' - S0'+season+'E0'+episode+'.mkv'
                part.rename(pathlib.Path(directory, name))


def detect_fix_name(name):
    episode = re.findall(r'E\d+', name)[0]
    e = re.findall('\d*', episode)[1]
    return e
