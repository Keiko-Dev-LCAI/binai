# Binai 💜 — Living Briefing (Grok + Claude)
**Last updated:** 2026-06-21 · **Session:** brainstorm + ecosystem connectors  
**Read this first** every Binai session. Full product plan → `BINAI-PLAN.md` in this folder.

---

## How to use these files

| File | Who | When |
|------|-----|------|
| **`BINAI-BRIEFING.md`** (this file) | **Claude + Grok** | Start of every session — status, priorities, who does what |
| **`BINAI-PLAN.md`** | **Claude + Grok** | Full spec — features, brainstorm, build phases, open questions |

### Update protocol (end of every Binai session)

Whoever worked on Binai last (Grok or Claude) **must** before closing:

1. Update **Last updated** date and **Session log** row in this file  
2. Update **Current status** and **Next up** if anything changed  
3. If brainstorm or phases shifted → edit matching section in `BINAI-PLAN.md`  
4. Commit and push: `Keiko-Dev-LCAI/binai` (or tell Keiko to push)

**Keiko:** Paste this whole file (or the Claude block at the bottom) into a new Claude chat when coordinating Binai.

---

## Current status (one glance)

| Item | State |
|------|--------|
| **Live URL** | https://binai.win · Railway `binai-production` |
| **Repo** | `Keiko-Dev-LCAI/binai` · local `~/Desktop/binai/` |
| **Latest commit** | `ed9ba46` (plan: OrcaVault + LightTunes connectors) |
| **Code shipped through** | `18e5a03` (About Me) |
| **Phase** | 1b — web beta hardening + real-device testing |
| **Mode** | Brainstorming — camera, retention, app connectors are **planned, not built** |

**TEST_MODE:** Keiko's dApp wallet pays all AIVM. Tester wallets = identity only (no LCAI needed).

---

## Shipped ✅ (web beta)

- Async chat + iPhone `Load failed` fix (`f534087`)
- Desktop Settings scroll (`7f1d754`)
- Mute voice 🔊/🔇 (`6e7d2da`)
- First-login setup wizard (`da928af`)
- Reply length Short / Balanced / Chatty (`805afc2`)
- About Me private bio tab, 12k chars (`18e5a03`)

Details + commit table → `BINAI-PLAN.md` § Shipped Web Beta

---

## Brainstorm only 📋 (not built)

- **Camera / Google Lens** — 📷 in chat, Cloudflare vision, photo Q&A
- **User-controlled retention** — 24h default; Remember / Save message / Save photo buttons
- **OrcaVault / Archives** — "Save to Archives" for photos forever on-chain (Family Album, etc.)
- **LightTunes** — 🎵 embed, play playlist, voice control
- **Keiko App Registry** — JSON manifest so Binai connects to more apps easily

Full spec → `BINAI-PLAN.md` § User-Controlled Retention, App Connectors, OrcaVault, LightTunes

---

## Next up (priority order)

1. **Real phone testing** — Sherry (ZH iPhone) + Keiko (EN PC) — see checklist in `BINAI-PLAN.md`
2. **Retention UI** — Remember / Save message + 24h chat roll-off (when ready to build)
3. **Camera v1** — 📷 + vision API
4. **App connectors v1** — Save to Archives handoff + LightTunes embed

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
| 2026-06-21 | Grok | Created `BINAI-BRIEFING.md`; full brainstorm in `BINAI-PLAN.md` (retention, camera, About Me, OrcaVault, LightTunes, app registry) |
| 2026-06-21 | Grok | Shipped About Me, reply length, setup wizard, mute, iPhone fix (commits through `18e5a03`) |
| 2026-06-20 | — | Phase 1 community beta started; `binai.win` live on Railway |

*Add a row at the end of every session.*

---

## Claude — paste this block

```
Binai living docs: ~/Desktop/binai/BINAI-BRIEFING.md (status) + BINAI-PLAN.md (full spec)
Live: binai.win · TEST_MODE=true · Keiko pays AIVM, tester wallet = identity only
Shipped: async chat, mute, setup wizard, reply length, About Me
Brainstorm only: camera/Lens, retention buttons, OrcaVault Archives, LightTunes connectors
Top priority: real phone testing (Sherry ZH, Keiko EN) before Discord scale
Grok owns code in ~/Desktop/binai/ — read briefing files before suggesting changes
```

---

*Keiko-Dev-LCAI/binai · push after updates so both assistants stay in sync*