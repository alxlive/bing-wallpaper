from datetime import date
import json
import os
import subprocess
from urllib.request import urlopen, Request


# Maintainer of this API: https://github.com/TimothyYe/bing-wallpaper
FEED_URL = 'https://bing.biturl.top/?resolution=3840&mkt=fr-FR&index='
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
}
FALLBACK_DAYS = 7
WALLPAPERS_DIR = os.path.expanduser('~/.wallpapers')


def download_wallpaper(day_index):
    # Download feed json.
    with urlopen(Request(f'{FEED_URL}{day_index}', headers=DEFAULT_HEADERS)) as resp:
        feed = json.load(resp)

    # Download new wallpapers.
    end_date = feed['end_date']
    url = feed['url']
    title = feed['copyright']
    path = os.path.join(WALLPAPERS_DIR, f'{end_date}.jpg')
    if os.path.exists(path):
        print(f'Image already exists: {path}')
        return title, path
    try:
        print(f'Downloading image: {url}')
        with urlopen(Request(url, headers=DEFAULT_HEADERS)) as resp:
            data = resp.read()
    except Exception as e:
        print(f'Failed to download image for {end_date} with URI: {url}.')
        raise
    with open(path, 'wb') as f:
        f.write(data)
    return title, path


def set_wallpaper(title, path):
    proc = subprocess.run(['xrandr | grep " connected"'], capture_output=True, shell=True, text=True)
    monitors = [line.split()[0] for line in proc.stdout.split('\n') if line]
    for monitor in monitors:
        prop_name = f'/backdrop/screen0/monitor{monitor}/workspace0/last-image'
        subprocess.run(['xfconf-query', '-c', 'xfce4-desktop', '-p', prop_name, '-s', path])


def main() -> None:
    if not os.environ.get('DISPLAY', None):
        print('$DISPLAY not set')
        return

    # Check store directory.
    os.makedirs(WALLPAPERS_DIR, exist_ok=True)

    chosen_wallpaper_title = None
    chosen_wallpaper_path = None
    # Iterate in reverse chronological order: today=0, yesterday=1, and so on.
    for day_index in range(FALLBACK_DAYS):
        try:
            title, path = download_wallpaper(day_index)
        except Exception as e:
            print(f'Exception while downloading wallpaper: {e}')
            continue
        if not chosen_wallpaper_title and not chosen_wallpaper_path:
            # Update xfce4-desktop wallpaper configuration.
            set_wallpaper(title, path)
            chosen_wallpaper_title = title
            chosen_wallpaper_path = path

    # Clean up old files.
    filenames = os.listdir(WALLPAPERS_DIR)
    filenames.sort(reverse=True)
    # Always keep last 30, no matter how old.
    filenames_to_delete = filenames[30:]
    if filenames_to_delete:
        print()
    for filename in filenames_to_delete:
        full_path = os.path.join(WALLPAPERS_DIR, filename)
        print(f'Deleting old file: {full_path}')
        os.remove(full_path)

    # Print summary message.
    if chosen_wallpaper_path and chosen_wallpaper_title:
        print()
        print(f"Successfully set today's wallpaper: {chosen_wallpaper_path}")
        print(f'Title: {chosen_wallpaper_title}')


if __name__ == '__main__':
    main()
