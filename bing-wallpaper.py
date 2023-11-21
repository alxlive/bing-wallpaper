from datetime import date
import json
import os
import subprocess
from urllib.request import urlopen, Request

FEED_URL = 'https://peapix.com/bing/feed?country='
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
}


def main() -> None:
    if not os.environ.get('DISPLAY', None):
        print('$DISPLAY not set')
        return

    # Load configuration from environment variable
    # country = os.environ.get('BING_WALLPAPER_COUNTRY', '')
    # amm UPDATE: just hardcode the country to France.
    country = 'fr'
    wallpapers_dir = os.environ.get('BING_WALLPAPER_PATH', os.path.expanduser('~/.wallpapers'))

    # Check store directory.
    os.makedirs(wallpapers_dir, exist_ok=True)

    # Download feed json.
    with urlopen(Request(f'{FEED_URL}{country}', headers=DEFAULT_HEADERS)) as resp:
        feed = json.load(resp)

    # Download new wallpapers.
    for item in feed:
        for image in ('imageUrl', 'fullUrl'):
            path = os.path.join(wallpapers_dir, f'{item["date"]}_{image}.jpg')
            if os.path.exists(path):
                continue
            try:
                with urlopen(Request(item[image], headers=DEFAULT_HEADERS)) as resp:
                    data = resp.read()
            except Exception as e:
                print(f'Failed to download image {item[image]}. Exception: {e}')
                continue
            with open(path, 'wb') as f:
                f.write(data)

    # Update xfce4-desktop wallpaper configuration.
    today_prefix = os.path.join(wallpapers_dir, f'{date.today().isoformat()}')
    today_wallpaper = None
    for image in ('_imageUrl', '_fullUrl'):
        # 'imageUrl' is much higher quality, so prefer it.
        # Fall back to fullUrl only if necessary.
        today_wallpaper = today_prefix + image + '.jpg'
        if not os.path.exists(today_wallpaper):
            continue
        # We found what we wanted. No need to iterate further.
        break
    if not today_wallpaper:
        return
    proc = subprocess.run(['xrandr | grep " connected"'], capture_output=True, shell=True, text=True)
    monitors = [line.split()[0] for line in proc.stdout.split('\n') if line]
    for monitor in monitors:
        prop_name = f'/backdrop/screen0/monitor{monitor}/workspace0/last-image'
        subprocess.run(['xfconf-query', '-c', 'xfce4-desktop', '-p', prop_name, '-s', today_wallpaper])
    print(f"Successfully set today's wallpaper: {today_wallpaper}")

    # Clean up old files
    filenames = os.listdir(wallpapers_dir)
    filenames.sort(reverse=True)
    # Always keep last 30, no matter how old (that's 15 days because each day
    # has two files with different image quality.
    filenames_to_delete = filenames[30:]
    for filename in filenames_to_delete:
        full_path = os.path.join(wallpapers_dir, filename)
        print(f'Deleting old file: {full_path}')
        os.remove(full_path)


if __name__ == '__main__':
    main()
