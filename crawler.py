import filehandler
import userhandler
import logger
import config
import re
from classes import Anime


def simple_download():

    import sites.torrenthandler as torrenthandler
    import sites.subsplease as subsplease

    subsplease.open_all_anime_page()
    torrenthandler.open_qbittorrent()

    torrenthandler.log_in()

    anime = Anime(None, None, None)

    anime.title = userhandler.ask_for_anime().replace('–', '-')

    downloadAnime(anime, subsplease, torrenthandler)

    torrenthandler.torrent_driver.quit()
    subsplease.sp_driver.quit()


def download_from_schedule():
    import sites.torrenthandler as torrenthandler
    import sites.subsplease as subsplease

    subsplease.open_schedule_page()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()

    anime_list = subsplease.get_every_anime_from_schedule()
    subsplease.open_all_anime_page()
    for anime in anime_list:
        downloadAnime(anime, subsplease, torrenthandler)

    torrenthandler.torrent_driver.quit()
    subsplease.sp_driver.quit()


def update_seasonal():

    import sites.torrenthandler as torrenthandler
    import sites.subsplease as subsplease

    subsplease.open_overview_page()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()

    anime_list = subsplease.get_every_anime_with_new_ep()
    subsplease.open_all_anime_page()
    for anime in anime_list:
        downloadAnime(anime, subsplease, torrenthandler)

    torrenthandler.torrent_driver.quit()
    subsplease.sp_driver.quit()


def standardize_downloaded():
    for directory in config.directories:
        path_list = filehandler.select_paths(directory)
        filehandler.rename(path_list)


def downloadAnime(anime, subsplease, torrenthandler):
    if re.search("Movie", anime.title) or re.search("OVA", anime.title):
        logger.info("This Anime is a Movie and has to be downloaded manually")
    else:
        subsplease.go_to_anime(anime.title)

        anime.title = subsplease.detect_title(anime.title)

        anime.batched = subsplease.detect_batched()
        anime.latest_title_on_overview = subsplease.extract_latest_title()
        anime.season = subsplease.detect_season(anime.latest_title_on_overview)
        if anime.batched is True:
            logger.info("This anime is batched")
            logger.info("Collecting batch-link for {} | Season {}".format(
                anime.title, anime.season))
            anime.amount_of_episodes = subsplease.extract_amount_of_episodes_from_batch()
            anime.episodes = subsplease.extract_episodes_from_batch()
            logger.info("Collected batch-link".format(
                anime.title, anime.season))
        else:
            logger.info("Collecting batch-link for {} | Season {}".format(
                anime.title, anime.season))
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

        if episode_difference is not None and anime.batched is True:
            logger.info("Deleting out of date files")
            filehandler.remove_episodes(
                anime.title, anime.season)
            links_to_download = anime.episodes
            torrenthandler.queue(links_to_download, download_path)
            logger.info('Process finished for ' + anime.title)
            logger.newline()
            subsplease.leave_anime()

        elif episode_difference is not None and anime.batched is False:
            links_to_download = anime.episodes[:episode_difference]
            torrenthandler.queue(links_to_download, download_path)
            logger.info('Process finished for ' + anime.title)
            logger.newline()
            subsplease.leave_anime()

        else:
            logger.info(anime.title + ' is already up to date')
            logger.info('Process finished for ' + anime.title)
            logger.newline()
            subsplease.leave_anime()
