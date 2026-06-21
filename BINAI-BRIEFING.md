# Binai 💜 — Living Briefing (Grok + Claude)
**Last updated:** 2026-06-21 · **Session:** brainstorm + ecosystem connectors  
**Read this first** every Binai session. Full product plan → `BINAI-PLAN.md` in this folder.

**Started with Claude:** Session 116 (2026-06-18) — tagline, 6-phase build, UX improvements in `BINAI-PLAN.md`. Claude also keeps a memory node at `future_builds/binai.md` (see below).

---

## How to use these files

| File | Who | When |
|------|-----|------|
| **`BINAI-BRIEFING.md`** (this file) | **Claude + Grok** | Start of every session — status, priorities, who does what |
| **`BINAI-PLAN.md`** | **Claude + Grok** | Full spec — features, brainstorm, build phases, open questions |
| **`future_builds/binai.md`** | **Claude** | Memory node — Claude auto-loads this; mirror of briefing summary |

**Claude memory (same content, two copies — keep in sync):**
- In repo: `~/Desktop/binai/future_builds/binai.md`
- In Claude app: `~/.config/Claude/.../agent/memory/future_builds/binai.md`

Also referenced in `~/Desktop/Importantant stuff/CLAUDE-MASTER-BRIEFING.md` and `GROK-BRIEFING.md`.

### Update protocol (end of every Binai session)

Whoever worked on Binai last (Grok or Claude) **must** before closing:

1. Update **Last updated** date and **Session log** row in this file  
2. Update **Current status** and **Next up** if anything changed  
3. Sync **`future_builds/binai.md`** (repo + Claude memory copy)  
4. If brainstorm or phases shifted → edit matching section in `BINAI-PLAN.md`  
5. Commit and push: `Keiko-Dev-LCAI/binai` (or tell Keiko to push)

**Keiko:** Paste this whole file (or the Claude block at the bottom) into a new Claude chat when coordinating Binai.

---

## Current status (one glance)

| Item | State |
|------|--------|
| **Live URL** | https://binai.win · Railway `binai-production` |
| **Repo** | `Keiko-Dev-LCAI/binai` · local `~/Desktop/binai/` |
| **Latest commit** | `0041e45` (plan docs) · code through `18e5a03` |
| **Code shipped through** | `18e5a03` (About Me) |
| **Phase** | 1b — web beta hardening + real-device testing |
| **Mode** | Brainstorming — camera, retention, app connectors are **planned, not built** |

**TEST_MODE:** Keiko's dApp wallet pays all AIVM. Tester wallets = identity only (no LCAI needed).

---

## Brainstorm rule

**Do what we can now → put the rest in the plan.** Grok ships web-beta-ready pieces; plan holds camera, connectors, retention, etc.

## Shipped ✅ (web beta)

- Async chat + iPhone `Load failed` fix (`f534087`)
- Desktop Settings scroll (`7f1d754`)
- Mute voice 🔊/🔇 (`6e7d2da`)
- First-login setup wizard (`da928af`)
- Reply length Short / Balanced / Chatty (`805afc2`)
- About Me private bio tab, 12k chars (`18e5a03`)
- **Friend mode** + opinion/appearance prompts (text chat)
- **Assistant name** (custom, changeable)
- **☀️ Catch Me Up** + gentle welcome suggestion
- **LightChat connector v1** — `/api/lightchat`, Catch Me Up + welcome unread, 💬/📹 buttons, `apps-registry.json`, LightChat `?chat=` / `?call=` deep links
- **快手 v1** — open 快手, auto-remember pasted links, Settings toggles
- **PWA auto-update** — `sw.js` + purple “tap to refresh” banner (no delete icon needed)

Details + commit table → `BINAI-PLAN.md` § Shipped Web Beta

---

## Brainstorm only 📋 (not built)

- **Camera / Google Lens** — 📷 in chat, Cloudflare vision, photo Q&A
- **User-controlled retention** — 24h default; Remember / Save message / Save photo buttons
- **OrcaVault / Archives** — "Save to Archives" for photos forever on-chain (Family Album, etc.)
- **LightTunes** — 🎵 embed, play playlist, voice control
- ~~**LightChat v1**~~ ✅ shipped — read bridge, Catch Me Up, deep links; Socket toast + voice-send still plan
- ~~**快手 v1**~~ ✅ shipped — open + link memory; Android share-target still plan
- **Keiko App Registry** — JSON manifest so Binai connects to more apps easily
- ~~**Custom assistant name**~~ ✅ shipped
- ~~**Friend mode / casual chat**~~ ✅ shipped (text); photo opinions need camera
- **⭐ Smart UX (Keiko loves this)** — Catch Me Up, memory confirmation, gentle open suggestions — Phase 1c after phone testing
- **Casual friend chat** — opinion questions, "what do you think?" text today (warm/playful); **photo opinions** need camera + vision (Phase 3)

Full spec → `BINAI-PLAN.md` § User-Controlled Retention, App Connectors, OrcaVault, LightTunes, Smart UX

---

## Next up (priority order)

1. **Real phone testing** — Sherry (ZH iPhone) + Keiko (EN PC) — see checklist in `BINAI-PLAN.md`
2. **⭐ Smart UX (Phase 1c)** — Catch Me Up button + memory confirmation + welcome-back — Keiko priority
3. **Retention UI** — Remember / Save message + 24h chat roll-off
4. **Camera v1** — 📷 + vision API
5. **App connectors v1** — LightChat ✅ · Save to Archives handoff + LightTunes embed

## From Claude plan — not discussed yet (still in BINAI-PLAN.md)

| Item | Status | When |
|------|--------|------|
| **9 Smart UX ideas** ⭐ | Keiko priority — expanded in plan | **Phase 1c** after phone testing (web-first: Catch Me Up, memory confirm) |
| **dApp Hub PR** | Not submitted | Before/after Discord — Claude task |
| **www.binai.win** redirect | Optional | Claude / Cloudflare when you want |
| **UI i18n** es/fr/pt/de/ja | AI backend yes; UI en+zh only | Before wider beta if non-CN testers |
| **Biometrics** unlock | Plan says PIN or fingerprint | Android / Capacitor — not web |
| **Live billing** `TEST_MODE=false` | Code exists, off | After beta testing |
| **Auto-pay subscription relay** | Spec in `auto_subscription_relay.md` | Post-beta |
| **Dual-track payment** (Google Play + managed wallet) | v2 roadmap | Far future |

See audit in user session 2026-06-21 — Grok answered Keiko "anything from Claude plan missing?"

---

## Who does what

| Task type | Owner | Examples |
|-----------|--------|----------|
| **Code in `~/Desktop/binai/`** | **Grok** | Features, fixes, deploy, `server.py`, `index.html` |
| **Cloudflare DNS, Railway env, docs** | **Claude** | `binai.win` DNS → Railway, briefing sync, copy review |
| **Real-device testing** | **Keiko + Sherry** | Trust Wallet, languages, report bugs |
| **Brainstorm / product** | **Keiko** | Decides direction; both AIs capture in plan files |
| **Push to GitHub** | **Grok or Keiko** | After commits on `main` |

---

## Architecture (short)

```
binai.win → Binai Railway → AIVM relay (web-production-aaaba.up.railway.app)
                              → Keiko dApp wallet pays (~0x729fea…)
```

| Key file | Purpose |
|----------|---------|
| `server.py` | Backend — SQLite, chat, About Me, AIVM |
| `index.html` | PWA frontend |
| `languages.py` | AI languages + reply length logic |
| `i18n-ui.js` | UI strings (en + zh only today) |

**Related apps (connectors brainstorm):** OrcaVault `orcavault-app/` · LightTunes `lighttunes-app/` · relay `orcavault-production.up.railway.app`

---

## Testing status

| Test | Result |
|------|--------|
| Server / curl health + chat + About Me | ✅ |
| Sherry iPhone Chinese | ⚠️ needs retest after latest deploy |
| Keiko PC English | ⚠️ needs retest |

Checklist → `BINAI-PLAN.md` § Community Beta — Testing Status

---

## Session log

| Date | Who | What changed |
|------|-----|----------------|
| 2026-06-21 | Grok | Linked Claude's `future_builds/binai.md` to binai folder; synced memory node |
| 2026-06-21 | Grok | Created `BINAI-BRIEFING.md`; full brainstorm in `BINAI-PLAN.md` (retention, camera, About Me, OrcaVault, LightTunes, app registry) |
| 2026-06-18 | Claude | Session 116 — `BINAI-PLAN.md` major update (tagline, 6 phases, UX improvements, payment roadmap) |
| 2026-06-20 | Claude | Session 134 — `binai.win` DNS → Railway live |
| 2026-06-21 | Grok | Shipped About Me, reply length, setup wizard, mute, iPhone fix (commits through `18e5a03`) |
| 2026-06-20 | — | Phase 1 community beta started; `binai.win` live on Railway |

*Add a row at the end of every session.*

---

## Claude — paste this block

```
Binai living docs: ~/Desktop/binai/BINAI-BRIEFING.md (status) + BINAI-PLAN.md (full spec) + future_builds/binai.md (your memory node)
Live: binai.win · TEST_MODE=true · Keiko pays AIVM, tester wallet = identity only
Shipped: async chat, mute, setup wizard, reply length, About Me
Brainstorm only: camera/Lens, retention buttons, OrcaVault Archives, LightTunes connectors
Top priority: real phone testing (Sherry ZH, Keiko EN) before Discord scale
Grok owns code in ~/Desktop/binai/ — read briefing files before suggesting changes
```

---

*Keiko-Dev-LCAI/binai · push after updates so both assistants stay in sync*