import os.path
import time
import gotify
import feedparser
import configparser
from datetime import datetime


def reading_config_file():
    def reading_settings(header, setting, template):
        try:
            variable = config[header][setting]
            if variable == template:
                print("Please change \"{}\" in app/config.yml.".format(setting))
                exit()
            else:
                print("\"{}\" has been set to \"{}\"".format(setting, variable))
            return variable
        except:
            if setting != "delay":
                config[header][setting] = template
            else:
                config[header][setting] = "120"
            with open("app/config.yml", 'w') as configfile:
                config.write(configfile)
            print("Please edit app/config.yml and restart the script.")
            exit()

    def header_check(header):
        try:
            config[header]
        except:
            config[header] = {}
            with open("app/config.yml", 'w+') as configfile:
                config.write(configfile)
    global domain, meow_uploader, gotify_url, gotify_token, gotify_title, gotify_priority, user_delay
    print("Checking for config...")
    config = configparser.ConfigParser()
    if not os.path.isdir("app"):
        os.mkdir("app")
    if os.path.exists('app/config.yml'):
        print("Found config.yml.")
        config.read("app/config.yml")
        header_check("ReleaseWatcher")
        domain = reading_settings("ReleaseWatcher", "url", "<INSERT URL like 'https://meow.com/?page=rss'>")
        meow_uploader = reading_settings("ReleaseWatcher", "uploader", "<INSERT RELEASE TAG like 'neoHEVC'>")
        user_delay = int(reading_settings("ReleaseWatcher", "delay", "0"))
        header_check("Gotify")
        gotify_url = reading_settings("Gotify", "gotify_url", "<INSERT GOTIFY-URL HERE>")
        gotify_token = reading_settings("Gotify", "token", "<INSERT GOTIFY-TOKEN HERE>")
        gotify_title = reading_settings("Gotify", "notification_title", "<INSERT NOTIFICATION TITLE HERE>")
        gotify_priority = int(reading_settings("Gotify", "priority", "<PRIORITY OF MESSAGE (0-15)>"))
        print("Settings have been successfully injected.")
    else:
        config["ReleaseWatcher"] = {}
        config["ReleaseWatcher"]["url"] = "<INSERT URL like 'https://meow.com/?page=rss'>"
        config["ReleaseWatcher"]["uploader"] = "<INSERT RELEASE TAG like 'neoHEVC'>"
        config["ReleaseWatcher"]["delay"] = "120"  # If you don't want to see the world burning, leave this above ~30s.
        config["Gotify"] = {}
        config["Gotify"]["gotify_url"] = "<INSERT GOTIFY-URL HERE>"
        config["Gotify"]["token"] = "<INSERT GOTIFY-TOKEN HERE>"
        config["Gotify"]["notification_title"] = "<INSERT NOTIFICATION TITLE HERE>"
        config["Gotify"]["priority"] = "<PRIORITY OF MESSAGE (0-15)>"
        with open("app/config.yml", 'w') as configfile:
            config.write(configfile)
        print("Created the config file.\nPlease edit app/config.yml and restart the script.")
        exit()


def requesting():
    timeout = 0
    request_status = False
    while not request_status:
        try:
            print("Requesting at {}.".format(datetime.now().strftime("%H:%M:%S")))
            rss = feedparser.parse(domain)
            timeout = 0
        except:
            print("Connection failed. Retrying in 5 seconds.")
            if timeout == 10:
                notification_send("ayo", False)
                timeout = 0
            time.sleep(5)
            timeout = timeout + 1
        else:
            print("  Connection: SUCCESS")
            filtering(rss)
            request_status = True
    return


def filtering(rss):
    entries = rss['entries']
    title_list = []
    link_list = []
    for item in entries:
        item_index = entries.index(item)
        item_title = entries[item_index]["title"]
        item_link = entries[item_index]["link"]
        if meow_uploader in item_title:
            title_list.append(item_title)
            link_list.append(item_link)
    if not title_list:
        print("No match has been found.")
        return
    database = open("app/rss.db", "a+")
    database.seek(0)
    raw_db = str(database.read())
    for entry in link_list:
        if entry not in raw_db:
            print("New release has been found, sending notification.")
            database.seek(0, 2)
            database.write("{} - {}".format(title_list[link_list.index(entry)], entry))
            database.write("\n")
            notification_send(title_list[link_list.index(entry)], True)
    database.close()
    return


def notification_send(title, all_good):
    gotify_server = gotify.gotify(
        base_url=gotify_url,
        app_token=gotify_token,
    )
    if all_good:
        gotify_server.create_message(
            "{} has just been released.".format(title),
            title=gotify_title,
            priority=gotify_priority,
        )
    else:
        gotify_server.create_message(
            "ATTENTION! The connection failed 10 times in a row!",
            title=gotify_title,
            priority=gotify_priority,
        )
    return


if __name__ == '__main__':
    reading_config_file()
    based = True
    while based:
        requesting()
        print("Retrying in {} seconds.".format(user_delay))
        time.sleep(user_delay)
