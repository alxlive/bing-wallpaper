# Ubuntu

It's too hard with cron. Check this:
https://askubuntu.com/questions/140305/cron-not-able-to-succesfully-change-background

At first it was throwing errors about DISPLAY not being set. Then with "env display" before the bash script in crontab, I fixed that problem. It ran with no errors, yet the wallpaper still didn't change! Apparently you also need DBUS_SESSION_BUS_ADDRESS.

Instead of all this, just follow the instructions below for the systemd unit and timer. It's amazing. It works perfectly.

```
# NOTE: THIS DOES NOT WORK!
$ cd ~/projects
$ git clone git@github.com:alxlive/bing-wallpaper.git
$ echo ${USERNAME}
$ crontab -e
30 * * * * env DISPLAY=:0 python3 /home/<REPLACE USERNAME>/projects/bing-wallpaper/bing-wallpaper.py
```

# OSX

```
$ cd ~/projects
$ git clone git@github.com:alxlive/bing-wallpaper.git
$ crontab -e
30 * * * * cd /Users/alxlive/projects/bing-wallpaper && ./run_bing_wallpaper.sh
```

# Xfce

## Usage

`python3 ./bing-wallpaper.py`

## Usage (systemd unit)

More info here:
https://unix.stackexchange.com/a/730858

```
$ cd ~/projects
$ git clone git@github.com:alxlive/bing-wallpaper.git
$ echo ${USERNAME}

# Don't change "user" to "alxlive". This is the correct path as written.
$ mkdir -p ~/.config/systemd/user
$ cp systemd/* ~/.config/systemd/user

# Edit script path to:
#   /home/alxlive/projects/bing-wallpaper/bing-wallpaper.py
$ vi ~/.config/systemd/user/bing-wallpaper.service

# Do not use sudo for this.
$ systemctl --user daemon-reload
$ systemctl --user enable --now bing-wallpaper.timer

# Check that the timer is active, always as --user:
$ systemctl --user list-timers
```

## Configuration (Environment Variable)

* `BING_WALLPAPER_PATH`: Bing wallpaper store directory (default: ~/.wallpapers)
