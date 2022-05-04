# Itch.io Bundle Downloader

I've decided to rewrite my entire script because of how messy and unreadable it was to work on the previous one. This project has also changed from having the ability to download the games through only a url (without an account) to now only being able to download games with only an account (though this will be changed in the future once I have access to a bundle that isn't linked to my account).

If you want to only download a bundle where you don't have an account tied to the bundle (so you only have the url to deal with) and this script still currenly doesn't have the option to download bundles without an account, it is recommended that you visit and use the older branch though it is serverly outdated, quite unstable, and may not function well.

## Usage

To be able to use this script, we first must install the necessary modules to make the script work. Firstly, do `pip install -r requirements.txt` which will install all of the modules. Once that is done, you can be able to use the script.

If you want to make things easier for you, instead of having to constantly rewrite the exact same username or password when the script asks you for it, you can pass it on as a flag, with `-n` being the username, and `-p` being the password.

If you want to make things even easier for you, instead you can use enviroment variables to your advantage, being more secure than inputting data or passing it off as an argument. You can utilize this by changing the name of the template enviromental file from `.template.env` to just `.env`, filling out your username and password into the correct fields, then passing the `-e` flag and everything should be working out as normal.

Have fun with this script!

## Shoutout
[shakeyourbunny](https://github.com/shakeyourbunny) forked this project (mainly refering to the old branch) and [made their own python script](https://github.com/shakeyourbunny/itch-downloader) with none of my code left, to which I was inspired (and was given realization that many more users will be downloading with an account tied to them then without) to retackle this problem of downloading bundles but now with an account tied to it and making the code more pretty with comments to indicate what that specific part of the code was doing.

The issue that I see with their script, however, is that it takes many layers to be able to link the account before downloading games, which this script was an attempt to severly simplify that process.

Still, I believe that this script is still noteworthy to check out in case my script fails to work correctly.