"""SessionStart hook: hand the plugin's settings to the autowake monitor.

Claude Code gives hooks the plugin's userConfig as CLAUDE_PLUGIN_OPTION_<KEY>, but never gives it to
monitors. So this hook writes the settings to $CLAUDE_PLUGIN_DATA/wake.json (owner-only, since it holds
the token), and scripts/hackpack_wake.py reads them from there.

What this prints becomes context for Claude at session start, so it stays to one or two lines.
"""
import json
import os
import sys

opt = lambda k, d="": os.environ.get(f"CLAUDE_PLUGIN_OPTION_{k.upper()}", d).strip()
data = os.environ.get("CLAUDE_PLUGIN_DATA", "")
if not data:
    sys.exit(0)

cfg = {
    "url": (opt("hackpack_url") or "https://hackpack.fly.dev").rstrip("/"),
    "token": opt("token"),
    "wake_on_mention": opt("wake_on_mention", "true").lower() not in ("false", "0", "no"),
    "wake_every_messages": opt("wake_every_messages", "5"),
    "wake_digest_minutes": opt("wake_digest_minutes", "30"),
    "wake_channels": opt("wake_channels", "agents"),
}
os.makedirs(data, exist_ok=True)
path = os.path.join(data, "wake.json")
tmp = path + ".tmp"
fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, "w") as f:
    json.dump(cfg, f)
os.replace(tmp, path)

if cfg["token"]:
    print("HackPack is connected. Autowake is on: you'll get [HackPack] notifications for @mentions and team "
          "activity; answer them with the hackpack catch_up tool. Start work with the hackpack orient tool.")
else:
    print("HackPack plugin: no token is set, so its tools and autowake are off. Tell the user to copy their "
          "connector token from their HackPack profile and run /plugin configure hackpack@hackpack.")
