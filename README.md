# Nyaa-Gotify-Notifications
### using the awesome self-hosted [gotify](https://github.com/gotify/server#gotifyserver).
###### DepriSheep#1841

---
Small project of mine to receive notifications, if a new release has been found on nyaa.si.

---

### Requirements:

* up and running gotify server
* gotify applet token
* python3 (2 probably works as well)
* requirements.txt

---

### Usage:

```
$ python -m pip install -r requirements.txt
$ python main.py
```

Then fill out the pre-generated `config.txt` and run the script again.

Example `config.txt`:

```
[config]
url = https://nyaa.si/rss 
search_term = neohevc
app_token = <GOTIFY-TOKEN>
gotify_url = <GOTIFY-ADRESS>
notification_title = RSS-Script
```

---

### Additional information:

+ ONLY WORKS ON NYAA.SI (and it's unsupported ad-filled proxies)
+ RSS gets updated every 120 seconds.
+ A list of releases that have been found, is saved in `rss.db`

---
### To-Do:
+ comments :)
___

### For educational purposes only!
Downloading certain sort of media from nyaa.si may not comply with your country's copyright laws.
