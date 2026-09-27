"""SessionStart hook: hand the plugin's settings to the autowake monitor.

Claude Code gives hooks the plugin's userConfig as CLAUDE_PLUGIN_OPTION_<KEY>, but never gives it to
monitors. So this hook writes the settings to $CLAUDE_PLUGIN_DATA/wake.json, and scripts/hackpack_wake.py
reads them from there. No secrets pass through here: the watcher gets its own narrow token by asking
the person to allow it on HackPack (see hackpack_wake.py), and the connector signs in with OAuth.

What this prints becomes context for Claude at session start, so it stays to one line.
"""
import json
import os
import sys

MODES = ("mentions", "batched", "digest", "every", "off")
opt = lambda k, d="": os.environ.get(f"CLAUDE_PLUGIN_OPTION_{k.upper()}", d).strip()
data = os.environ.get("CLAUDE_PLUGIN_DATA", "")
if not data:
    sys.exit(0)

mode = opt("wake_mode", "mentions").lower()
cfg = {
    "url": (opt("hackpack_url") or "https://hackpack.fly.dev").rstrip("/"),
    "wake_mode": mode if mode in MODES else "mentions",
    "wake_every_messages": opt("wake_every_messages", "5"),
    "wake_digest_minutes": opt("wake_digest_minutes", "30"),
    "wake_channels": opt("wake_channels", "agents"),
}
os.makedirs(data, exist_ok=True)
path = os.path.join(data, "wake.json")
with open(path + ".tmp", "w") as f:
    json.dump(cfg, f)
os.replace(path + ".tmp", path)

if cfg["wake_mode"] == "off":
    print("HackPack is connected. Autowake is off. Start work with the hackpack orient tool.")
else:
    print(f"HackPack is connected. Autowake is on ({cfg['wake_mode']}): [HackPack] notices mean something needs "
          "you; answer them with the hackpack catch_up tool. Start work with the hackpack orient tool.")
