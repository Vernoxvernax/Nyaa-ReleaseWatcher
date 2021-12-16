import os.path
import time
import gotify
import feedparser
from configparser import ConfigParser


def main():
    print("Reading config file...")
    global url, search_term, gotify_server, notification_title, gotify_server
    url, search_term, api_token, gotify_url, notification_title = reading_config_file()
    gotify_server = gotify.gotify(
        base_url=gotify_url,
        app_token=api_token,
    )
    based = True
    while based:
        time.sleep(120)
        requesting()


def reading_config_file():
    if not os.path.exists('config.txt'):
        print("No config file found.\nCreating one...")
        with open("config.txt", 'w') as fp:
            fp.write("[config]\nurl = \nsearch_term = \ngotify_url = \napp_token = \nnotification_title = ")
        print("Please enter your settings and restart the script.")
    else:
        config = ConfigParser()
        config.read("config.txt")
        config_header = config["config"]
        url = config_header["url"]
        search_term = config_header["search_term"]
        gotify_url = config_header["gotify_url"]
        app_token = config_header["app_token"]
        notification_title = config_header["notification_title"]
        print("The following settings have been imported:\n URL: {}\n Search-Term: {}\n Gotify-Domain: {}\n".format(url, search_term, gotify_url))
        return url, search_term, app_token, gotify_url, notification_title


def requesting():
    print("Preparing to request.")
    timeout = 0
    request_status = False
    while not request_status:
        try:
            rss = feedparser.parse(url)
            timeout = 0
        except:
            print("Connection failed. Retrying in 5 seconds.")
            if timeout == 10:
                gotify_timeout()
                timeout = 0
            time.sleep(5)
            timeout = timeout + 1
        else:
            print("RSS successfully retrieved.")
            request_status = True
    filtering(rss)
    return


def filtering(rss):
    entries = rss['entries']
    title_list = []
    link_list = []
    for item in entries:
        item_index = entries.index(item)
        item_title = entries[item_index]["title"]
        item_link = entries[item_index]["link"]
        if search_term in item_title:
            title_list.append(item_title)
            link_list.append(item_link)
    if not title_list:
        return
    print("New entries have been found.")
    database = open("rss.db", "a+")
    database.seek(0)
    duplicate_counter = 0
    notification = 0
    raw_db = str(database.read())
    for entry in link_list:
        if entry in raw_db:
            duplicate_counter = 1
        else:
            database.seek(0, 2)
            database.write(entry)
            database.write("\n")
            notification = 1
    if duplicate_counter == 1:
        print("At least one item was already in the database.")
    database.close()
    if notification == 1:
        gotify_success()
        return
    else:
        return


def gotify_success():
    print("Sending notification...")
    gotify_server.create_message(
        "NEW RELEASE FOUND!!!",
        title=notification_title,
        priority=15,
    )
    return


def gotify_timeout():
    print("This is the 10th connection failure. Sending notification...")
    gotify_server.create_message(
        "Connection failed 10 times in a row.",
        title=notification_title,
        priority=15,
    )
    return


main()
