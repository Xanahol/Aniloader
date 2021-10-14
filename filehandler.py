from config import directories, blacklist_do_not_standardize
import os
from time import sleep
from classes import Anime, Episode
import logger
import pathlib
import re
import shutil


def detect_season_on_path(path):
    season_raw = re.split(r'\\', path)[-1]
    season = re.findall('Season \d.*', season_raw)[0]
    s = re.findall('\d.*', season)[0]
    return s


def detect_anime_on_path(path):
    title = re.split(r'\\', path)[-2]
    return title


def detect_episode(file_name):
    episode = re.findall(r'- \d+', file_name)[0]
    e = re.findall('\d.*', episode)[0]
    return e


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
                    new_episodes = int(episodes_available) - \
                        episodes_downloaded
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
    dir_list = []
    for (root, dirs, files) in os.walk(directory):
        if re.search(r'Season \d', root) and not re.search(r'Season \d+.{4,}', root) and not any(ext in root for ext in blacklist_do_not_standardize):
            dir_list.append(root)
    logger.info('Collected every anime on '+directory)
    return dir_list


def folders_in(path_to_parent):
    for fname in os.listdir(path_to_parent):
        if os.path.isdir(os.path.join(path_to_parent, fname)):
            yield os.path.join(path_to_parent, fname)


def move_files(source, destination):
    files_list = os.listdir(source)
    for file in files_list:
        file = str(source + "\\" + file)
        shutil.move(file, destination)
    os.rmdir(source)


def rename(path_list):
    for path in path_list:
        season = detect_season_on_path(path)
        anime_title = detect_anime_on_path(path)
        sub_dirs = list(folders_in(path))
        if sub_dirs != []:
            for dir in sub_dirs:
                move_files(dir, path)
        rename_anime(anime_title, season, path)


def detect_filler(name):
    if re.search(r'\d*\.5', name):
        return True
    else:
        return False


def detect_version(name):
    episode_and_version = re.findall(r'\d*\.\d+|\d*[v|V]\d+', name)
    if episode_and_version != []:
        episode_and_version = episode_and_version[0]
        version = re.findall(r'\d+', episode_and_version)[-1]
        return int(version)
    else:
        return 0


def clean_files_with_tripple_digits(fullpath, name):
    if re.search(r'S\d{3,}', name):
        seasonr = re.findall(r'S\d{3,}', name)[0]
        season = re.findall(r'\d+', seasonr)[0].lstrip('0')
        season = f"{int(season):02d}"
        anime_title = re.findall(r'.*(?= -)', name)[0]
        directory = fullpath.parent
        if re.search(r'E\d{3,}', name):
            epr = re.findall(r'E\d{3,}', name)[0]
            ep = re.findall(r'\d+', epr)[0].lstrip('0')
            ep = f"{int(ep):02d}"
        else:
            ep = str(re.findall(r'\d+$', name)[0])
        name = anime_title+' - S'+season+'E'+ep+'.mkv'
        fullpath.rename(pathlib.Path(directory, name))
    else:
        return


def rename_anime(anime_title, season, anime_path):
    for file in pathlib.Path(anime_path).iterdir():
        if file.is_file():
            episode = Episode()
            episode.raw_name = file.stem
            episode.season = f"{int(season):02d}"
            episode.version = detect_version(episode.raw_name)
            episode.is_filler = detect_filler(episode.raw_name)
            # Detatch in in case of files formatted like "Anime - S001E002"
            # clean_files_with_tripple_digits(file, episode.raw_name)
            if not episode.is_filler:
                if re.search('1080p', episode.raw_name):
                    episode.number = f"{int(detect_episode(episode.raw_name)):02d}"
                    directory = file.parent
                    name = anime_title+' - S'+episode.season+'E'+episode.number+'.mkv'
                    try:
                        file.rename(pathlib.Path(directory, name))
                        logger.info("renamed file " +
                                    episode.raw_name + " ------>> "+name)
                    except FileExistsError:
                        logger.error("File " + episode.raw_name + " in directory " +
                                     str(directory) + " not renamable, exists already")
            else:
                os.remove(file)
                logger.info("Removed File " + episode.raw_name +
                            " because its a filler")
