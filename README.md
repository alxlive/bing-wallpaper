# Ubuntu

$ cd ~/projects
$ git clone git@github.com:alxlive/bing-wallpaper.git
$ crontab -e
30 * * * * python3 /home/ubuntu/projects/bing-wallpaper/bing-wallpaper.py

# Xfce

## Usage

`python3 ./bing-wallpaper.py`

## Usage (systemd unit)

```
$ mkdir -p ~/.config/systemd/user
$ cp systemd/* ~/.config/systemd/user
$ vi ~/.config/systemd/user/bing-wallpaper.service  # edit script path
$ systemctl --user enable --now bing-wallpaper.timer
```

## Configuration (Environment Variable)

* `BING_WALLPAPER_PATH`: Bing wallpaper store directory (default: ~/.wallpapers)
