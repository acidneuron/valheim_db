========================================================================
  VALHEIM SELF HOSTED DEDICATED SERVER DISCORD CONTROL BOT
  COMPLETE SETUP GUIDE (run.py + config.json)
========================================================================

This bot controls your Valheim self hosted dedicated server through Discord slash
commands (/start, /stop, /status). All settings live in config.json.

Table of Contents:
  SECTION A ................ System Requirements & Prerequisites
  SECTION B ................ Creating Your Discord Bot (Step-by-Step)
  SECTION C ................ Filling in config.json
  SECTION D ................ Running the Bot & Slash Commands
  TROUBLESHOOTING .......... Common Errors & How to Fix Them

================================================================================
SECTION A — SYSTEM REQUIREMENTS & PREREQUISITES
================================================================================

This bot runs on Windows and controls a Valheim Dedicated Server process by
launching valheim_server.exe from the command line. You need four things set
up before anything else:

--------------------------------------------------------------------------------
A1. WINDOWS (10 or 11)
--------------------------------------------------------------------------------
    The bot uses Windows-specific features (process groups, taskkill). It will
    NOT work on Linux/macOS without significant changes.


--------------------------------------------------------------------------------
A2. PYTHON 3.10 OR NEWER
--------------------------------------------------------------------------------
    1) Go to https://www.python.org/downloads/   and download the latest stable
       Python release for Windows  (currently Python 3.1x).

    2) Run the .exe installer.  IMPORTANT:
       - CHECK the box that says "Add python.exe to PATH" at the bottom of the
         first setup screen.  If you skip this step, `python` won't work in
         Command Prompt and nothing here will run.

    3) Click "Install Now" and wait for completion.

    4) Verify installation: open a Terminal (Ctrl+X ? Terminal in VS Code, or
       search "cmd" / "Command Prompt" or "PowerShell"), then type:

           python --version

       You should see something like:  Python 3.1x.x


--------------------------------------------------------------------------------
A3. PYTHON PACKAGES (discord.py with voice support)
--------------------------------------------------------------------------------
    In a terminal, run:

           pip install "discord.py[voice]"

    This installs discord.py plus its optional voice-related dependencies PYNAKT
    (nacl and opus).  The "[voice]" tag is important — it pulls in the PyNaCl
    package required for encrypted connections.


--------------------------------------------------------------------------------
A4. STEAM DESKTOP CLIENT
--------------------------------------------------------------------------------
    1) Download Steam from https://store.steampowered.com/about/   if you don't
       already have it.

    2) Install and launch Steam, log in to your account.

    3) You do NOT need to "own" Valheim yourself — the dedicated server tool is
       free on Steam's list of "Dedicated Server Tools."


--------------------------------------------------------------------------------
A5. VALHEIM DEDICATED SERVER (installed via SteamCMD or Steam Client)
--------------------------------------------------------------------------------
    Method 1 — Steam Client GUI:
      1) In Steam, go to Library ? change the dropdown from "Games" to
         "Tools".

      2) Search for "Valheim Dedicated Server".

      3) Click Install.  Default install path is something like:

           C:\Program Files (x86)\Steam\steamapps\common\Valheim Dedicated Server

      The actual server executable you need is:

           valheim_server.exe

      It lives in a subfolder called "server":

           ...\Valheim Dedicated Server\server\valheim_server.exe


    Method 2 — SteamCMD (command-line, more reliable for servers):
      1) Download SteamCMD from https://developer.valvesoftware.com/wiki/SteamCMD
         (Windows version: steamcmd.zip).

      2) Extract to e.g. C:\steamcmd\.

      3) Open Command Prompt and cd into that folder:

           cd C:\steamcmd

      4) Install the dedicated server:

           steamcmd.exe +login anonymous +app_update 896660 validate +quit

         (App ID 896660 = Valheim Dedicated Server.)

      5) This installs to a path like
         C:\steamcmd\steamapps\common\Valheim Dedicated Server\server\


--------------------------------------------------------------------------------
A6. VISUAL C++ REDISTRIBUTABLE
--------------------------------------------------------------------------------
    Unity games and their servers depend on Microsoft Visual C++ runtime
    libraries.  If you don't have one, valheim_server.exe will refuse to start.

    Download the latest x64 installer from:

       https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist
       ? click "vc_redist.x64.exe" under "x64"

    Run it and accept defaults.


------------------------------------------------------------------------
SECTION B: CREATING YOUR DISCORD BOT
------------------------------------------------------------------------

You need a Discord "Bot" application before the code works. Full process
below - takes about 10 minutes once.


STEP 1: Create an Application
------------------------------
  1. Go to https://discord.com/developers/applications in your browser.
     Log in with your normal Discord account if prompted.

  2. Click the "New Application" button (top-right).

  3. Give it a name - e.g. "Valheim Bot" or whatever you want.

  4. Click "Create".


STEP 2: Add a Bot to the Application
--------------------------------------
  1. In the left sidebar of your new application, click "Bot".

  2. Click "Add Bot" -> confirm with "Yes, let's go!"

  3. (Optional) Scroll down to "Bot Username" and rename it from the
     default random name to something like "Valheim-Bot", then Save
     Changes at the bottom of that section.


STEP 3: Configure Bot Privilegied Intents
------------------------------------------
  1. Still on the "Bot" page, look under PRIVILEGED GATE INTENTS.

  2. Turn ON both toggles:
       - [x] MESSAGE CONTENT INTENT
       - [x] SERVER MEMBERS INTENT

  3. Click "Save Changes".


STEP 4: Copy Your Bot Token
-----------------------------
  1. Under the bot username, click the "Reset Token" (or "View Bot
     Token") button.

  2. Discord shows your token - a long string that starts something
     like "MTIz..." and is hundreds of characters.

  3. COPY this entire string to your clipboard or a text editor.
     You'll paste it into config.json in Section B below.

  IMPORTANT: This token is like a password. Anyone who has it can control
  your bot - don't share it in screenshots, Discord messages, etc. If you
  suspect it's leaked, come back here and click "Reset Token".


STEP 5: Invite the Bot to Your Server
---------------------------------------
  1. In your application page, left sidebar -> "OAuth2" -> "URL Generator".

  2. Under SCOPES check:
       [x] bot

  3. Under BOT PERMISSIONS scroll and select (at minimum):
       - Send Messages
       - View Channel
     Or just toggle "Administrator" if this is a private server you fully
     control and don't care about least-privilege.

  4. At the bottom, copy the auto-generated URL (it starts with
     https://discord.com/api/oauth2/authorize?...)

  5. OPEN that URL in your browser - it will show Discord authorization:
       a) Pick the server you want to invite the bot to from the dropdown.
          Click "Continue".
       b) Review the permissions the bot is requesting. Click "Authorize".
       c) Complete the CAPTCHA verification if shown.

  6. The bot should now appear in your server's member list (under
     #OFFLINE since it isn't running yet).


-- BOT SETUP COMPLETE --



------------------------------------------------------------------------
SECTION C: FILLING IN config.json
------------------------------------------------------------------------

config.json pairs each actual setting with a "**" comment key for inline
documentation. The bot strips out those commentary keys automatically, so
they're harmless and useful to leave in place. Fill values as follows:


FIELD 1: discord_token
-----------------------
  PASTE the full token string you copied from Step 4 above (Discord Developer Portal).

  Example:
    "discord_token": ""


FIELD 2: valheim_server_exe
----------------------------
  Full filesystem path to your Valheim dedicated server .exe. On Windows,
  you MUST use DOUBLE backslashes (\\) because JSON treats a single \ as
  an escape character.

  Where to find it:
    - Open your Steam library
    - Right-click "Valheim Dedicated Server" -> "Manage" -> "Browse local files"
    - Navigate into the "server" subfolder
    - Find valheim_server.exe and copy its full path

  When writing to config.json, double every backslash:
    "valheim_server_exe": "C:\\Program Files (x86)\\Steam\\...\\valheim_server.exe"


FIELD 3: server_name
---------------------
  Whatever you want your server to appear as in the Valheim server list.
  This is just a string - use quotes.

    "server_name": "literallythenameofyourserver"


FIELD 4: world_name
--------------------
  Your world filename WITHOUT the .db extension.

  Where to find it:
    - Press Win+R, paste this path and hit Enter:
        C:\WHERE YOUR valheim_server.exe IS LOCATED\valheim_save_data\worlds_local
	
    - Find your .db file (e.g., "Valheimworld.db" -> write "Valheimworld")

  If you want a fresh world, just make up a name and the server will generate it:
    "world_name": "NewWorldName"


FIELD 5: server_port
---------------------
  UDP port for the Valheim server. Default is 2456 - leave this unless
  you need multiple servers on one machine or have a specific firewall config.

    "server_port": "2456"

  Note: If your ISP/router requires port forwarding, forward BOTH
  UDP 2456 and UDP 2457 (2456 is game, 2457 is discovery).


FIELD 6: password (OPTIONAL)
------------------------------
  Leave as empty string "" for no password. Add text for a password-protected server:

    "password": ""                       -- no password
    "password": "your-secret-pass"      -- with password


FIELD 7: use_crossplay
------------------------
  Set to true or false (no quotes) depending on whether you want Xbox players able to join.

    "use_crossplay": true    -- allow PS/Xbox players from pc.
    "use_crossplay": false   -- PC players only.


FIELD 8: steam_app_id
----------------------
  DO NOT CHANGE THIS - it's set to 892970 which is the Steam App ID for Valheim. The bot injects this into the environment.


-- COMPLETE EXAMPLE config.json --

{
  "** DISCORD TOKEN": "Your bot token from discord.com/developers"
  "discord_token": "PASTE_YOUR_TOKEN_HERE",

  "** VALHEIM EXE PATH": "Full path to valheim_server.exe (use double backslashes)"
  "valheim_server_exe": "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Valheim Dedicated Server\\server\\valheim_server.exe",

  "** SERVER NAME (-name)": "The name players see in the server list"
  "server_name": "Valkaramanga",

  "** WORLD FILE (-world)": "Your world file name (no .db extension)"
  "world_name": "yourworldname",

  "** PORT (-port) UDP port (usually 2456)"
  "server_port": "2456",

  "** PASSWORD (-password)": "Leave empty for no password"
  "password": "",

  "** CROSSPLAY?": "true to enable, false to disable"
  "use_crossplay": true,

  "*** DO NOT TOUCH": "This is how we bypass your .bat file and talk to Steam.",
  "steam_app_id": 892970
}


------------------------------------------------------------------------
SECTION D: RUNNING THE BOT
------------------------------------------------------------------------

1. Make sure both run.py and config.json are in the same folder
   (fore expample C:\valheim_server\valheim_db\).

2. Open a terminal / Command Prompt / PowerShell in that folder:
     cd C:\valheim_server\valheim_db\

3. Run it with Python or use the run.bat provided,it is the same thing
     python run.py

4. You'll see this if successful:
     [+] Live as <BotName>. Slash commands synced.

5. In Discord, type /start to boot the Valheim server. The bot will
   launch valheim_server.exe and stream its output inline in Discord.


COMMANDS AVAILABLE

  /start    - Launches the Valheim dedicated server (streams console
              output back into Discord)
  /stop     - Sends Ctrl+C for a graceful world save, then force-kills
              if it doesn't shut down within 15 seconds
  /status   - Shows whether the bot is connected and alive
  /say      - Makes the bot send messages to your channel (useful for
              announcing things while you're not at Discord)


TROUBLESHOOTING

- "Application commands require intents" error:
  Go back to Step 5 above and make sure MESSAGE CONTENT INTENT is ON.

- Bot doesn't show up in server member list:
  You didn't complete the OAuth2 invite (Step 7). Re-do it with a fresh URL.

- it crashes on start:
  Double-check steam_app_id is 892970 in config.json and valheim_server_exe
  points to the actual .exe, not to a shortcut or a wrapper script.

---------------------------------------------------------