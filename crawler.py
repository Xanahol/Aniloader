import filehandler
import userhandler
import logger
import config
import re
from classes import Anime


def simple_download(site):

    import sites.torrenthandler as torrenthandler
    module_path = "sites."+site
    importlib = __import__("importlib")
    site = importlib.import_module(module_path)

    site.open_all_anime_page()
    torrenthandler.open_qbittorrent()

    torrenthandler.log_in()

    anime = Anime()

    anime.title = userhandler.ask_for_anime().replace('–', '-')

    downloadAnime(anime, site, torrenthandler)

    torrenthandler.torrent_driver.quit()
    site.sp_driver.quit()


def download_from_schedule(site):
    import sites.torrenthandler as torrenthandler
    module_path = "sites."+site
    importlib = __import__("importlib")
    site = importlib.import_module(module_path)

    site.open_schedule_page()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()

    anime_list = site.get_every_anime_from_schedule()
    site.open_all_anime_page()
    for anime in anime_list:
        downloadAnime(anime, site, torrenthandler)

    torrenthandler.torrent_driver.quit()
    site.sp_driver.quit()


def update_seasonal(site):

    import sites.torrenthandler as torrenthandler
    module_path = "sites."+site
    importlib = __import__("importlib")
    site = importlib.import_module(module_path)

    site.open_overview_page()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()

    anime_list = site.get_every_anime_with_new_ep()
    site.open_all_anime_page()
    for anime in anime_list:
        downloadAnime(anime, site, torrenthandler)

    torrenthandler.torrent_driver.quit()
    site.sp_driver.quit()


def get_all_anime(site):

    import sites.torrenthandler as torrenthandler
    module_path = "sites."+site
    importlib = __import__("importlib")
    site = importlib.import_module(module_path)

    site.open_all_anime_page()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()

    anime_list = site.get_every_anime()
    site.open_all_anime_page()
    for anime in anime_list:
        downloadAnime(anime, site, torrenthandler)

    torrenthandler.torrent_driver.quit()
    site.sp_driver.quit()


def standardize_downloaded():
    for directory in config.directories:
        path_list = filehandler.select_paths(directory)
        filehandler.rename(path_list)


def downloadAnime(anime, site, torrenthandler):
    if re.search("Movie", anime.title) or re.search("OVA", anime.title):
        logger.info("This Anime is a Movie and has to be downloaded manually")
        return

    if anime.title in config.blacklist:
        logger.info("Anime " + anime.title +
                    " is on Blacklist and will not be downloaded\n")
        return

    site.go_to_anime(anime.title)
    if site.episode_check():
        anime.title = site.detect_title(anime.title)

        anime.batched = site.detect_batched()
        anime.latest_title_on_overview = site.extract_latest_title()
        anime.season = site.detect_season(anime.latest_title_on_overview)
        if anime.batched is True:
            logger.info("This anime is batched")
            logger.info("Collecting batch-links for {} | Season {}".format(
                anime.title, anime.season))
            anime.amount_of_episodes = site.extract_amount_of_episodes_from_batch()
            anime.episodes = site.extract_episodes_from_batch()
            logger.info("Collected batch-link".format(
                anime.title, anime.season))
        else:
            logger.info("Collecting links for {} | Season {}".format(
                anime.title, anime.season))
            anime.episodes = site.get_magnet_links()
            anime.amount_of_episodes = len(anime.episodes)

        logger.info('Starting Download-Process...')
        logger.info("The anime {} has {} episodes so far".format(
            anime.title, anime.amount_of_episodes))

        episode_difference = filehandler.check_if_anime_up_to_date(
            anime.title, anime.season, anime.amount_of_episodes)

        logger.info("{} of which are not on the server yet".format(
                    episode_difference))

        download_path = filehandler.check_directory_for_anime(
            anime.title, anime.season)

        logger.info("Downloading them to {}".format(download_path))

        if episode_difference is not None and anime.batched is True:
            logger.info("Deleting out of date files")
            filehandler.remove_episodes(
                anime.title, anime.season)
            links_to_download = anime.episodes
            torrenthandler.queue(links_to_download, download_path)
            logger.info('Process finished for ' + anime.title)
            logger.newline()
            site.leave_anime()

        elif episode_difference is not None and anime.batched is False:
            links_to_download = anime.episodes[:episode_difference]
            torrenthandler.queue(links_to_download, download_path)
            logger.info('Process finished for ' + anime.title)
            logger.newline()
            site.leave_anime()

        else:
            logger.info(anime.title + ' is already up to date')
            logger.info('Process finished for ' + anime.title)
            logger.newline()
            site.leave_anime()
