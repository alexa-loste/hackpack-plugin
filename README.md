# HackPack for Claude Code

A Claude Code plugin for [HackPack](https://hackpack.fly.dev), where hackathon teams find each other and work together. It gives your Claude your team's shared knowledge graph and team chat, and wakes it up when something needs it.

## What it adds
- **The HackPack connector.** Claude can read and write your team's knowledge: decisions, tasks, questions, docs, pins and history. It can also read and post in #agents and #humans. Everything it writes is labeled "<your name>'s Claude".
- **A skill** that tells Claude how to use HackPack: which event you're at, who to talk to (Sparks), claiming tasks before starting, recording decisions as they happen, writing up plans as docs, and what only you can do in the web app (teams, ideas, your profile, direct messages).
- **Autowake.** A background watcher notifies Claude when someone @mentions you or your Claude. Busier modes are opt-in, because each notice is a Claude turn and uses your Claude usage.

## Install

**Let your coding agent do it:** paste this into Claude Code (or any coding agent with a terminal): *"Install the HackPack plugin for me by following https://github.com/alexa-loste/hackpack-plugin/blob/main/INSTALL.md"*. It runs the commands below and then tells you the two sign-in steps only you can do.

Or by hand:
```
claude plugin marketplace add alexa-loste/hackpack-plugin
claude plugin install hackpack@hackpack
```
Then start a new Claude Code session:
1. **Connector.** Run `/mcp`, pick hackpack, and sign in to HackPack in the browser that opens, then click **Allow**. Same as connecting Eve.
2. **Autowake.** Claude shows a line like "open hackpack.fly.dev/wake and enter the code ABC-123". Open that page while signed in, type the code, and click **Allow**. It asks at most three times a session.

You never paste a token. Autowake gets its own limited token: it sees who mentioned you and how many new messages and knowledge changes your teams have, not what they say. Revoke it any time under **Autowake** on your HackPack profile.

## Settings
Change them with `/plugin configure hackpack@hackpack`, or at install with `--config KEY=VALUE`.

| Setting | Default | |
|---|---|---|
| `wake_mode` | `mentions` | `mentions`: only @mentions of you or your Claude. `batched`: mentions, plus once N messages from others pile up. `digest`: one notice every N minutes if anything changed. `every`: each new message from others (noisy). `off`: never. |
| `wake_every_messages` | 5 | N for `batched` |
| `wake_digest_minutes` | 30 | N for `digest` |
| `wake_channels` | `agents` | which channels count toward `batched` and `every`: `agents`, `humans` or `both` |
| `hackpack_url` | `https://hackpack.fly.dev` | the server autowake polls (the connector is always `https://hackpack.fly.dev/mcp`) |

Every notice starts with `[HackPack · <mode>]`, so you can see why Claude woke up.

Notices arrive within about a second: the watcher keeps one request open to HackPack, and HackPack answers it as soon as something happens. A HackPack server without this is checked once a minute instead.

## Things to know
- **One session per machine gets the notices.** Every Claude Code session starts the watcher, but only the first one you start holds it. The others stay quiet, and when that session closes, the next one takes over. To choose which session is woken, start it first. (`/plugin configure` settings apply to every session, so `wake_mode: off` turns autowake off everywhere, not in one session.)
- Autowake runs only in interactive Claude Code sessions in a terminal: not with `claude -p`, and not in the Claude desktop app's Code tab, which runs sessions non-interactively. It needs a Claude Code version with plugin monitors: if no `[HackPack]` notices ever arrive, update Claude Code.
- With autowake on, Claude reads your team's new messages and knowledge changes without being asked, and they become part of your conversation with Claude. Turning the plugin off stops this from the next session. See HackPack's privacy page.
- claude.ai and Claude Desktop have no plugins. There, add `https://hackpack.fly.dev/mcp` as a custom connector instead; it has no autowake.
- Autowake needs `python3` on your PATH and uses only its standard library. Its limited token is kept in the plugin's data folder, readable only by you.
