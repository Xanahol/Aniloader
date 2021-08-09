from logging import disable
import threading
from time import sleep
import userhandler
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
import crawler
from logger import info,error,debug

layout=[
    [sg.Button("Get one specific Anime")],
    [sg.Button('Update Episodes labaled "NEW"')],
    [sg.Button("Get All Seasonal Anime")],
    [sg.Button("Standardize Library")],
    [sg.Output(size=(70, 12))],
    [sg.Input(), sg.Button("Send")]
    ]

sg.theme('DarkBlack')
window = sg.Window('Aniloader Beta', layout)

def disable_all_buttons():
    window['Get one specific Anime'].update(disabled=True)
    window['Update Episodes labaled "NEW"'].update(disabled=True)
    window['Get All Seasonal Anime'].update(disabled=True)
    window['Standardize Library'].update(disabled=True)

def enable_all_buttons():
    window['Get one specific Anime'].update(disabled=False)
    window['Update Episodes labaled "NEW"'].update(disabled=False)
    window['Get All Seasonal Anime'].update(disabled=False)
    window['Standardize Library'].update(disabled=False)

def ask_for_specific_anime():
    print("Which anime would you like to download?\n")
    while True:
        event, values = window.read()
        if event == "Send":
            anime_name = values[0]
            return anime_name

def ask_for_username():
    print("Please enter your credentials for qBittorrent:\nUsername: ")
    while True:
        event, values = window.read()
        if event == "Send":
            username = values[0]
            return username

def ask_for_password():
    print("Password:")
    while True:
        event, values = window.read()
        if event == "Send":
            password = values[0]
            return password

while True:
    try:
        event, values = window.read()
        if event == "Get one specific Anime":
            disable_all_buttons()
            import sites.torrenthandler as torrenthandler
            torrenthandler.open_qbittorrent()
            if torrenthandler.log_in() == "Bypass":
                anime_name = ask_for_specific_anime()
                main_thread = threading.Thread(target=crawler.simple_download, args=(torrenthandler, anime_name), daemon=True)
                main_thread.run()
                enable_all_buttons()
            else:
                username = ask_for_username()
                password = ask_for_password()
                if torrenthandler.log_in(username, password) == "Success":
                    anime_name = ask_for_specific_anime()
                    main_thread = threading.Thread(target=crawler.simple_download, args=(torrenthandler, anime_name), daemon=True)
                    main_thread.run()
                    enable_all_buttons()
                elif torrenthandler.log_in(username, password) == "Failed":
                    while torrenthandler.log_in(username, password) == "Failed":
                        username = ask_for_username()
                        password = ask_for_password()
        elif event == 'Update Episodes labaled "NEW"':
            disable_all_buttons()
            import sites.torrenthandler as torrenthandler
            torrenthandler.open_qbittorrent()
            if torrenthandler.log_in() == "Bypass":
                main_thread = threading.Thread(target=crawler.update_seasonal, args=[torrenthandler], daemon=True)
                main_thread.run()
                enable_all_buttons()
            else:
                username = ask_for_username()
                password = ask_for_password()
                if torrenthandler.log_in(username, password) == "Success":
                    main_thread = threading.Thread(target=crawler.update_seasonal, args=[torrenthandler], daemon=True)
                    main_thread.run()
                    enable_all_buttons()
                elif torrenthandler.log_in(username, password) == "Failed":
                    while torrenthandler.log_in(username, password) == "Failed":
                        username = ask_for_username()
                        password = ask_for_password()
        elif event == "Get All Seasonal Anime":
            disable_all_buttons()
            import sites.torrenthandler as torrenthandler
            torrenthandler.open_qbittorrent()
            if torrenthandler.log_in() == "Bypass":
                main_thread = threading.Thread(target=crawler.download_from_schedule, args=[torrenthandler], daemon=True)
                main_thread.run()
                enable_all_buttons()
            else:
                username = ask_for_username()
                password = ask_for_password()
                if torrenthandler.log_in(username, password) == "Success":
                    main_thread = threading.Thread(target=crawler.download_from_schedule, args=[torrenthandler], daemon=True)
                    main_thread.run()
                    enable_all_buttons()
                elif torrenthandler.log_in(username, password) == "Failed":
                    while torrenthandler.log_in(username, password) == "Failed":
                        username = ask_for_username()
                        password = ask_for_password()
        elif event == "Standardize Library":
            disable_all_buttons()
            main_thread = threading.Thread(target=crawler.standardize_downloaded, daemon=True)
            main_thread.run()
            enable_all_buttons()
        elif event == WIN_CLOSED:
            window.close()
            break
    except Exception as e:
        print(e)