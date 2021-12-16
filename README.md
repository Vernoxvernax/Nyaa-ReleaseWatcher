# Nyaa-Gotify-Notifications
### using the awesome self-hosted [gotify](https://github.com/gotify/server#gotifyserver).
###### DepriSheep#1841

---
Small project of mine to receive notifications, if a new release has been found on nyaa(.)si.

---

### Requirements:

* up and running gotify server
* gotify applet token
* python3 (2 probably works as well)

---

### Usage:

`$ python main.py`

then edit `config.txt`.
There you'll have to fill out every entry.

Example `config.txt`:

```
[config]
url = http://nyaa.si/rss 
search_term = neohevc
app_token = <GOTIFY-TOKEN>
gotify_url = <GOTIFY-ADRESS>
notification_title = RSS-Script
```

---