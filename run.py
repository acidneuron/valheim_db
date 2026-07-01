import os, json, time, subprocess, signal
import discord

# Load config (ignoring keys starting with **)
with open("config.json") as f:
    raw = json.load(f)
cfg = {k:v for k,v in raw.items() if not k.startswith("*")}

client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)

val_proc = None
is_running = False
start_time = 0.0

def fmt_uptime(t):
    d, r = divmod(int(time.time() - t), 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    return f"{d}d {h}h {m}m" if d else f"{h}h {m}m"

@tree.command(name="start", description="Start Valheim server")
async def do_start(i):
    global val_proc, is_running, start_time
    await i.response.defer(thinking=True)
    
    if is_running and val_proc and val_proc.poll() is None:
        em = discord.Embed(title="🟡 Already Running", color=0xFFD700)
        em.add_field(name="Uptime", value=fmt_uptime(start_time))
        return await i.followup.send(embed=em)

    # Build the exact command line from config arguments
    cmd = [
        cfg["valheim_server_exe"],
        "-nographics", "-batchmode", 
        "-name", cfg["server_name"], 
        "-port", str(cfg["server_port"]),
        "-world", cfg["world_name"]
    ]
    
    if password := cfg.get("password"):
        cmd += ["-password", password]

    if cfg.get("use_crossplay") == True or cfg.get("use_crossplay") == "true":
        cmd.append("-crossplay")

    try:
        # CRITICAL FIX: Inject SteamAppId into the environment so it boots without the .bat file!
        env = os.environ.copy()
        env["SteamAppId"] = str(cfg.get("steam_app_id", 892970))

        # Launch exactly where the .exe lives so Unity finds its data folders
        val_proc = subprocess.Popen(
            cmd,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            env=env,
            cwd=os.path.dirname(cfg["valheim_server_exe"])
        )
        is_running = True; start_time = time.time()
        
        em = discord.Embed(title="🟢 Server Started", color=0x00FF00)
        await i.followup.send(embed=em)
    except Exception as e:
        await i.followup.send(f"❌ Failed to start: `{e}`", ephemeral=True)

@tree.command(name="stop", description="Stop Valheim server")
async def do_stop(i):
    global val_proc, is_running
    await i.response.defer(thinking=True)
    
    if not is_running or val_proc is None: 
        return await i.followup.send("🔴 Server already offline.", ephemeral=True)

    try:
        # Gracefully tells the process group to exit (saves world safely)
        val_proc.send_signal(signal.CTRL_C_EVENT) 

        # Gives it 15 seconds to close on its own
        for _ in range(30):
            if val_proc.poll() is not None: break
            time.sleep(0.5)

        # Force kills the whole tree (including Valheim.exe and cmd window)
        if val_proc.poll() is None:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(val_proc.pid)])

        is_running = False
        await i.followup.send("🔴 Server Stopped.")
    except Exception as e:
        await i.followup.send(f"❌ Error stopping: `{e}`")

@tree.command(name="status", description="Check Status")
async def do_status(i):
    global is_running
    await i.response.defer(thinking=True)
    
    if not is_running or val_proc is None or val_proc.poll() is not None:
        is_running = False
        return await i.followup.send("🔴 Server Offline")

    em = discord.Embed(title="🟢 Server Online", color=0x00FF00)
    em.add_field(name="World", value=cfg["server_name"])
    em.add_field(name="Uptime", value=fmt_uptime(start_time))
    await i.followup.send(embed=em)

@client.event
async def on_ready():
    print(f"[+] Live as {client.user}. Slash commands synced.")
    await tree.sync()

if __name__ == "__main__":
    client.run(cfg["discord_token"])

