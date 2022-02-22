# Nyaa-ReleaseWatcher
### using the awesome self-hosted [gotify](https://github.com/gotify/server#gotifyserver).
###### DepriSheep#1841

---
Small project to receive notifications, if a new release has been found on nyaa.si.

---

![Imgur](https://i.imgur.com/rrbR14K.png)

---
### Requirements:

* git (for git clone)
* up and running gotify container and an app-token
* docker and docker-compose

---

### Installation:

Clone this GitHub repository:
```
$ git clone https://github.com/Vernoxvernax/Nyaa-ReleaseWatcher.git
```

Build the docker image:
```
$ docker build -t depri/nyaa-releasewatcher .
```

Create the container using the `docker-compose.yml` file:
```
$ docker-compose up -d
```

Then fill out the pre-generated `config.yml` file, that has been created in the `app` folder.
```
$ vim config.yml
$ docker-compose start
```
###### If the container keeps stopping you can temporarily remove the `-d` flag to get the logs directly into you terminal.

You can obviously run the script outside a docker container, but screens suck and crash, so this method is a lot easier to set up and manage.

---

### Additional information:

+ ONLY WORKS ON NYAA.SI (and it's unsupported ad-filled proxies)
+ RSS gets updated every 120 seconds.
+ `.torrent` links of the releases that have been found, is saved in `rss.db`.

---
### To-Do:
+ comments :)
+ email-support (tomorrow)
+ quick-setup guide for gotify
___

### For educational purposes only!
Downloading certain sort of media from nyaa.si may not comply with your country's copyright laws.
