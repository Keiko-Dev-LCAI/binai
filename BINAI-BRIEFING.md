# Binai 💜 — Living Briefing (Grok + Claude)
**Last updated:** 2026-07-24 · **Session:** leave beta + billing live + hub PR + profile/QA fix  
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
- In repo: `~/Desktop/Orca Apps/web/binai/future_builds/binai.md`
- In Claude app: `~/.config/Claude/.../agent/memory/future_builds/binai.md` (if present)

Also referenced in `~/Desktop/Importantant stuff/CLAUDE-MASTER-BRIEFING.md` and `GROK-BRIEFING.md` · **App Manager** `orcapod-app/index.html`.

### Update protocol (end of every Binai session)

1. Update **Last updated** + **Session log** in this file  
2. Update **Current status** / **Next up**  
3. Sync **`future_builds/binai.md`**  
4. Plan-only changes → `BINAI-PLAN.md`  
5. Commit/push `Keiko-Dev-LCAI/binai` when code changed  

---

## Current status (one glance) — 2026-07-24 evening

| Item | State |
|------|--------|
| **Live URL** | https://binai.win · Railway project `binai` · volume `/app/data` |
| **Repo** | `Keiko-Dev-LCAI/binai` · local `~/Desktop/Orca Apps/web/binai/` |
| **Build** | **`20260724-30`** (profile/name/QA wipe fix) |
| **Health** | `test_mode: false` · `free_actions: 20` · `monthly_price_usd: 3.0` |
| **Phase** | **Out of beta** — production billing on |
| **Hub PR** | https://github.com/lightchain-protocol/lcai-dApp-hub/pull/60 — **open**, X=`x.com/KeikoDevLCAI` |

### Railway env (authoritative)

| Variable | Value |
|----------|--------|
| `TEST_MODE` | **`false`** |
| `FREE_ACTIONS_LIFETIME` | **`20`** |
| `MONTHLY_PRICE_USD` | **`3`** |
| `FREE_FOREVER_WALLETS` | `0xA3a653a8cBA0710ff57Ac34E2278C603B4259FD3` (Keiko — unlimited AI) |
| `OWNER_WALLET` | `0x6518fd07b3da01b17bd37d7c40f9a5e3c87a09ba` (MetaMask fee collector) |
| `DATA_DIR` | `/app/data` |

### Billing model (live)

| Layer | Rule |
|--------|------|
| **Free forever (no AIVM cost)** | Calendar, reminders, contacts, dialer, notes, local/instant chat commands |
| **Free AI** | **20 lifetime** AIVM messages per wallet |
| **Paid** | **~$3/mo LCAI** (dynamic from CoinGecko/price API) → MetaMask OWNER_WALLET |
| **Free forever AI** | Wallets in `FREE_FOREVER_WALLETS` (comma-separated) |
| **Quota** | Only real AIVM replies burn free count (not calendar/contacts/local) |

### Product shipped (recent — 2026-07-24)

- First-login wizard + **feature tour** (skippable)  
- Calendar full page: Day/Week/Month, tap day → full-day list, chat “show today’s calendar”  
- Date-only + recurring events (every Monday, birthday yearly)  
- Phone contacts + call-by-name (includes match, edit contacts)  
- Custom Quick Actions + **快手** in Quick Add presets  
- Log off, PIN, no auto-replay of stale chat  
- Beta wording removed from UI  
- Settings → **Contact** 𝕏 @KeikoDevLCAI  
- Profile save fix: load before save; never wipe name/QA with empty POST  

### Local path note
Code lives at **`~/Desktop/Orca Apps/web/binai/`** (not `~/Desktop/binai/`).

---

## Next up

1. **Real-device smoke** — Keiko free-forever wallet + a second wallet (20 free → paywall)  
2. **Hub #60** — wait for Lightchain merge (rebased; X set)  
3. Optional: more free-forever wallets (e.g. Sherry) via Railway `FREE_FOREVER_WALLETS`  
4. Camera / retention / Archives / LightTunes embed — still plan only  

---

## Session log

| Date | Session | Notes |
|------|---------|--------|
| 2026-07-24 | Grok | Leave beta: 20 free AI, $3/mo, FREE_FOREVER, tour, disclosures, build 27–30; hub PR #60; profile wipe fix; hub PRs rebased + X |
| 2026-07-24 | earlier | Name-first setup, QA, calendar, dialer, mobile UX |

---

## Claude paste block (short)

```
Binai 💜 LIVE https://binai.win — OUT OF BETA.
TEST_MODE=false · 20 free AI / wallet · $3/mo LCAI · FREE_FOREVER_WALLETS=0xA3a6…9FD3
Build 20260724-30 · calendar + contacts + dialer free forever · hub PR #60 open (x.com/KeikoDevLCAI)
Repo: Keiko-Dev-LCAI/binai · local: ~/Desktop/Orca Apps/web/binai/
Permission: told+confirmed only. Full briefing: BINAI-BRIEFING.md
```
