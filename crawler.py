import filehandler
import userhandler
import sites.torrenthandler as torrenthandler
import sites.subsplease as subsplease
import logger
import config
from classes import Anime


def simple_download():

    import sites.torrenthandler as torrenthandler
    import sites.subsplease as subsplease

    subsplease.open_all_anime_page()
    torrenthandler.open_qbittorrent()

    torrenthandler.log_in()
    logger.info('Login successful!')

    anime = Anime(None, None, None)

    anime.title = userhandler.ask_for_anime().replace('–', '-')

    subsplease.go_to_anime(anime.title)

    anime.title = subsplease.detect_title(anime.title)

    anime.batched = subsplease.detect_batched()
    anime.latest_title_on_overview = subsplease.extract_latest_title()
    anime.season = subsplease.detect_season(anime.latest_title_on_overview)
    if anime.batched is True:
        logger.info("This anime is batched")
        anime.amount_of_episodes = subsplease.extract_amount_of_episodes_from_batch()
        anime.episodes = subsplease.extract_episodes_from_batch()
    else:
        anime.episodes = subsplease.get_magnet_links()
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

    download(episode_difference, anime, download_path)

    torrenthandler.torrent_driver.quit()
    subsplease.sp_driver.quit()


def update_seasonal():

    import sites.torrenthandler as torrenthandler
    import sites.subsplease as subsplease

    subsplease.open_overview_page()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()
    logger.info('Login successful!')

    anime_list = subsplease.get_every_anime_with_new_ep()
    logger.newline()
    logger.info('Starting Download-Process...')
    logger.newline()
    for anime in anime_list:
        subsplease.go_to_anime(anime.latest_title_on_overview)
        episodes_available = anime.amount_of_episodes
        logger.info("The anime {} has {} episodes so far".format(
            anime.title, episodes_available))
        episode_difference = filehandler.check_if_anime_up_to_date(
            anime.title, anime.season, episodes_available)
        download_path = filehandler.check_directory_for_anime(
            anime.title, anime.season)
        logger.info("Downloading them to {}".format(download_path))
        download(episode_difference, anime, download_path)

    torrenthandler.torrent_driver.quit()
    subsplease.sp_driver.quit()


def standardize_downloaded():
    for directory in config.directories:
        path_list = filehandler.select_paths(directory)
        filehandler.rename(path_list)


def download(episode_difference, anime, download_path):
    if episode_difference is not None and anime.batched is True:
        logger.info("Deleting out of date files")
        filehandler.remove_episodes(
            anime.title, anime.season)
        links_to_download = anime.episodes
        torrenthandler.queue(links_to_download, download_path)
        logger.info('Process finished for ' + anime.title)
        logger.newline()
    elif episode_difference is not None and anime.batched is False:
        logger.info("{} of which are not on the server yet".format(
            episode_difference))
        links_to_download = anime.episodes[:episode_difference]
        torrenthandler.queue(links_to_download, download_path)
        logger.info('Process finished for ' + anime.title)
        logger.newline()
    else:
        subsplease.leave_anime()
        logger.info(anime.title + ' is already up to date')
        logger.info('Process finished for ' + anime.title)
        logger.newline()
