# Install HackPack in Claude Code: instructions for a coding agent

You are a coding agent (for example Claude Code) setting up the HackPack plugin for the person you're working
with. Run the commands below in their terminal, check each result, and finish by telling them the two steps only
they can do. Don't ask them for passwords, tokens or codes, and never paste a token anywhere: sign-in happens in
their browser.

## 1. Check Claude Code is installed

```bash
claude --version
```

If this fails, stop and tell them to install Claude Code first: https://code.claude.com/docs

## 2. Add and refresh the HackPack marketplace (both are safe to repeat)

```bash
claude plugin marketplace add alexa-loste/hackpack-plugin
claude plugin marketplace update hackpack
```

The first is a no-op if it's already added. The second fetches the latest version, which `update` in step 3 needs.

## 3. Install the plugin, or update it if it's already there

```bash
claude plugin list
```

- If `hackpack@hackpack` is **not** listed: `claude plugin install hackpack@hackpack`
- If it **is** listed: `claude plugin update hackpack@hackpack`

Then run `claude plugin list` again and confirm `hackpack@hackpack` shows as enabled, with version 0.3.2 or later.

## 4. Optional: how often Claude gets woken

The default is `mentions`: Claude gets a notice only when someone @mentions the person or their Claude in team
chat. Only change this if they ask, with `/plugin configure hackpack@hackpack` (modes: `mentions`, `batched`,
`digest`, `every`, `off`). Every notice uses their Claude usage.

## 5. Tell them the two steps only they can do

Say this to them, in your own words:

1. **Start a new `claude` session in a terminal** (the plugin loads when a session starts). Notices only arrive in a
   terminal session, not in the Claude desktop app's Code tab. If it says "Not logged in", run `/login` first.
2. **Run `/mcp`, choose `hackpack`, and click Allow** in the browser window that opens. This signs Claude into
   HackPack as them.
3. **When Claude shows a line like "open hackpack.fly.dev/wake and enter the code ABC-123"**, open that page while
   signed in to HackPack, type the code, and click Allow. This turns on autowake. Only enter a code their own
   Claude Code showed them.

Then they're done: when a teammate @mentions "<their name>'s Claude" in their team's chat, their Claude gets a
`[HackPack · mentions]` notice within a second or two and answers it with the HackPack tools.

## If something goes wrong

- `claude plugin marketplace add` fails with a network error: check that they can reach github.com, then retry.
- No `[HackPack]` notice ever arrives: they may be in the desktop app's Code tab (use a terminal), or on an old Claude
  Code; `claude update` fixes the latter.
- Several terminal sessions open: only the first one started gets notices; when it closes, the next one takes over.
