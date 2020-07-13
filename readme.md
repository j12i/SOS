This is my take on backing up your soup.io history. Just the HTML files from last to first, only on the first page the assets are saved to have a copy of the CSS styling your page. It doesn't take care of saving the pictures and videos in the posts after the first page. Essentially it is just a wrapper around wget, which does the heavy lifting like retrying, cookies etc.

*Only works with pagination (endless scrolling OFF).*

Prerequisites: Python 3 and wget.

```
Usage: SOS <soup name> <since> <working directory>
  At least give the soup name as argument.
  If you want to give wd but not since, enter 0.
```

Everything except the wget log and the cookie file will be saved in a `<your>.soup.io` directory inside the working directory.

To save a private soup, start the script once, stop it, and copy the session cookie values for `www.soup.io` and `<your>.soup.io` as well as the `soup_user_id` cookie into the `cookie` file in the working directory.