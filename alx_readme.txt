On OSX, it's not possible (or at least really hard) to run after each sleep.

I've added the script to login items, but that's only after boot.

So I've also added it to cron every 30 min:
*/30 * * * * cd /Users/alxlive/projects/bing-wallpaper && ./run_bing_macos.sh

On OSX, I use Geektool (https://www.tynsoe.org/geektool/documentation/) to
display the title of the image on top of the desktop.

I could also burn it into the images, but I'd rather leave them clean.
You don't have to display the text though. You could just check the log if
you're wondering where the image is from.
