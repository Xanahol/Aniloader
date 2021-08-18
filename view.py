from logging import PlaceHolder, disable
import threading
from time import sleep
from tkinter import Button, Label
from tkinter.constants import RIGHT
import userhandler
import PySimpleGUI as sg
import re
import os
import importlib
import importlib.util
from PySimpleGUI.PySimpleGUI import ButtonMenu, WIN_CLOSED
import crawler
import fileinput
from logger import info, error, debug

def import_conf():
    spec = importlib.util.spec_from_file_location("config", "config.py")
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config

main_layout = [
    [sg.Button("Get one specific Anime"), ],
    [sg.Button('Update Episodes labaled "NEW"')],
    [sg.Button("Get All Seasonal Anime")],
    [sg.Button("Standardize Library")],
    [sg.Button("Settings", button_color=(sg.theme_background_color()))],
    [sg.Output(size=(70, 12))],
    [sg.Input(), sg.Button("Send"), sg.Text('Aniloader Beta v0.3.4',
                                            size=(16, 1), background_color="black", text_color="gray")]
]

settings_window_called = False

sg.theme('DarkBlack')

main_window = sg.Window('Aniloader Beta', main_layout, icon='icon.ico')


def disable_all_buttons():
    main_window['Get one specific Anime'].update(disabled=True)
    main_window['Update Episodes labaled "NEW"'].update(disabled=True)
    main_window['Get All Seasonal Anime'].update(disabled=True)
    main_window['Standardize Library'].update(disabled=True)


def enable_all_buttons():
    main_window['Get one specific Anime'].update(disabled=False)
    main_window['Update Episodes labaled "NEW"'].update(disabled=False)
    main_window['Get All Seasonal Anime'].update(disabled=False)
    main_window['Standardize Library'].update(disabled=False)


def ask_for_specific_anime():
    print("Which anime would you like to download?\n")
    while True:
        event, values = main_window.read()
        if event == "Send":
            anime_name = values[0]
            return anime_name


def ask_for_username():
    print("Please enter your credentials for qBittorrent:\nUsername: ")
    while True:
        event, values = main_window.read()
        if event == "Send":
            username = values[0]
            return username


def ask_for_password():
    print("Password:")
    while True:
        event, values = main_window.read()
        if event == "Send":
            password = values[0]
            return password


def create_settings_window():
    settings_layout = [
        [sg.Text("IP-Address:"), sg.Text(config.ip_4)],
        [sg.Text("Torrent-Port:"), sg.Text(config.torrent_port, key='settings_torrent_port'),
         sg.Button("Edit")],
        [sg.Text("Directories:"), sg.Combo(config.directories, key='settings_dir_combo'), sg.Button("-", key="settings_dir_minus"), sg.Button("+", key="settings_dir_plus")]
    ]

    settings_window = sg.Window(
        'Settings', settings_layout, icon='icon.ico')

    return settings_window


def create_adjust_port_window():
    adjust_port_layout = [
        [sg.Input(config.torrent_port, size=(15, 1))],
        [sg.Button("Save", key="save_port_adjustment")]
    ]

    adjust_port_window = sg.Window(
        'Edit Port', adjust_port_layout, icon='icon.ico')

    return adjust_port_window


def delete_dir(value):
    value = value.replace("\\", "\\\\")

    with fileinput.FileInput("config.py", inplace=True) as file:
        for line in file:
            if re.search(",+ +'"+value+"',+ +", line):
                print(re.sub(",* *'"+value+"',* *", ', ', line), end='')
            else:
                print(re.sub(",* *'"+value+"',* *", '', line), end='')


def add_dir(value):
    with fileinput.FileInput("config.py", inplace=True) as file:
        for line in file:
            print(re.sub("']", "', '"+ value + "']", line), end='')


def adjust_port(value):
    with fileinput.FileInput("config.py", inplace=True) as file:
        for line in file:
            print(line.replace('torrent_port = "'+config.torrent_port +
                  '"', 'torrent_port = "'+value+'"'), end='')


while True:
    try:
        main_event, main_values = main_window.read()
        if main_event == "Get one specific Anime":
            
            config = import_conf()
            disable_all_buttons()
            import sites.torrenthandler as torrenthandler
            torrenthandler.open_qbittorrent()
            if torrenthandler.log_in() == "Bypass":
                anime_name = ask_for_specific_anime()
                main_thread = threading.Thread(target=crawler.simple_download, args=(
                    torrenthandler, anime_name), daemon=True)
                main_thread.run()
                enable_all_buttons()
            else:
                username = ask_for_username()
                password = ask_for_password()
                if torrenthandler.log_in(username, password) == "Success":
                    anime_name = ask_for_specific_anime()
                    main_thread = threading.Thread(target=crawler.simple_download, args=(
                        torrenthandler, anime_name), daemon=True)
                    main_thread.run()
                    enable_all_buttons()
                elif torrenthandler.log_in(username, password) == "Failed":
                    while torrenthandler.log_in(username, password) == "Failed":
                        username = ask_for_username()
                        password = ask_for_password()
        elif main_event == 'Update Episodes labaled "NEW"':
            
            config = import_conf()
            disable_all_buttons()
            import sites.torrenthandler as torrenthandler
            torrenthandler.open_qbittorrent()
            if torrenthandler.log_in() == "Bypass":
                main_thread = threading.Thread(target=crawler.update_seasonal, args=[
                                               torrenthandler], daemon=True)
                main_thread.run()
                enable_all_buttons()
            else:
                username = ask_for_username()
                password = ask_for_password()
                if torrenthandler.log_in(username, password) == "Success":
                    main_thread = threading.Thread(target=crawler.update_seasonal, args=[
                                                   torrenthandler], daemon=True)
                    main_thread.run()
                    enable_all_buttons()
                elif torrenthandler.log_in(username, password) == "Failed":
                    while torrenthandler.log_in(username, password) == "Failed":
                        username = ask_for_username()
                        password = ask_for_password()
        elif main_event == "Get All Seasonal Anime":
             
            
            config = import_conf()
            disable_all_buttons()
            import sites.torrenthandler as torrenthandler
            torrenthandler.open_qbittorrent()
            if torrenthandler.log_in() == "Bypass":
                main_thread = threading.Thread(target=crawler.download_from_schedule, args=[
                                               torrenthandler], daemon=True)
                main_thread.run()
                enable_all_buttons()
            else:
                username = ask_for_username()
                password = ask_for_password()
                if torrenthandler.log_in(username, password) == "Success":
                    main_thread = threading.Thread(target=crawler.download_from_schedule, args=[
                                                   torrenthandler], daemon=True)
                    main_thread.run()
                    enable_all_buttons()
                elif torrenthandler.log_in(username, password) == "Failed":
                    while torrenthandler.log_in(username, password) == "Failed":
                        username = ask_for_username()
                        password = ask_for_password()
        elif main_event == "Standardize Library":
             
            
            config = import_conf()
            disable_all_buttons()
            main_thread = threading.Thread(
                target=crawler.standardize_downloaded, daemon=True)
            main_thread.run()
            enable_all_buttons()

        elif main_event == "Settings":
             
            
            config = import_conf()
            settings_window = create_settings_window()
            while True:
                 
                
                config = import_conf()
                settings_event, settings_values = settings_window.read()
                if settings_values == None:
                    settings_window['settings_dir_minus'].update(
                        disabled=True)
                settings_window['settings_torrent_port'].update(
                    config.torrent_port)
                if settings_event == "Edit":
                     
                    
                    config = import_conf()
                    adjust_port_window = create_adjust_port_window()
                    while True:
                        adjust_port_event, adjust_port_values = adjust_port_window.read()
                        if adjust_port_event == "save_port_adjustment":
                            adjust_port(adjust_port_values[0])
                            settings_window['settings_torrent_port'].update(
                                adjust_port_values[0])
                            adjust_port_window.close()
                            break
                        if adjust_port_event == WIN_CLOSED:
                            adjust_port_window.close()
                            break
                elif settings_event == "settings_dir_minus":
                    delete_dir(settings_values['settings_dir_combo'])
                     
                    
                    config = import_conf()
                    settings_window['settings_dir_combo'].update(
                        values=config.directories)
                    settings_window['settings_dir_minus'].update(
                        disabled=True)
                elif settings_event == "settings_dir_plus":
                    add_dir(settings_values['settings_dir_combo'])
                     
                    
                    config = import_conf()
                    settings_window['settings_dir_combo'].update(
                        values=config.directories)
                elif settings_event == WIN_CLOSED:
                     
                    
                    config = importlib.import_module(config)
                    settings_window.close()
                    break
        elif main_event == WIN_CLOSED:
             
            
            config = import_conf()
            main_window.close()
            break
    except Exception as e:
        print(e)
