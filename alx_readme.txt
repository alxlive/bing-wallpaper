On OSX, it's not possible (or at least really hard) to run after each sleep.

I've added the script to login items, but that's only after boot.

So I've also added it to cron every 30 min:
*/30 * * * * cd /Users/alxlive/projects/xfce-bing-wallpaper && ./run_bing_wallpaper.sh
