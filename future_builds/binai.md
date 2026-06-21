---
name: future-binai
description: "Binai 💜 — LIVE at binai.win; personal AI assistant web beta; wallet+PIN; AIVM via aaaba relay; TEST_MODE=true; named after Cheng Bin (ai=爱 love)"
metadata:
  node_type: memory
  type: project
  originSessionId: d65fa248-a00e-4183-b6dd-f030a84a1eb4
---

# Binai 💜 — Claude memory node

**Canonical docs (read these — this file is a summary):**
- **Status / handoff:** `~/Desktop/binai/BINAI-BRIEFING.md` ← start here every session
- **Full plan:** `~/Desktop/binai/BINAI-PLAN.md`
- **This file:** Claude memory mirror — keep in sync with briefing after each session

---

## Live status (2026-06-21)

| Item | Value |
|------|--------|
| URL | https://binai.win |
| Railway | `binai-production` · volume `/app/data` |
| GitHub | Keiko-Dev-LCAI/binai · commit `02703a5` |
| Code shipped | through `18e5a03` (About Me) |
| TEST_MODE | true — Keiko dApp wallet `0x729fea…` pays via aaaba relay |
| DNS | binai.win ✅ CNAME → Railway (session 134, Claude) |

**Auth:** wallet once → wallet-bound PIN (`binai_wallet_pins`)  
**Chat:** POST /api/chat → job_id → poll /api/chat/status (~44s–2min)

---

## Shipped (web beta)

- Async chat / iPhone fix (`f534087`)
- Desktop Settings scroll (`7f1d754`)
- Mute voice 🔊/🔇 (`6e7d2da`)
- First-login setup wizard (`da928af`)
- Reply length Short/Balanced/Chatty (`805afc2`)
- About Me private bio 12k (`18e5a03`)

---

## Brainstorm only (not built)

- Camera / Google Lens (Cloudflare vision)
- User retention — 24h default, Remember / Save message / Save photo
- OrcaVault **Save to Archives** (permanent on-chain photos)
- LightTunes embed + play playlist
- Keiko App Registry (connect more apps)
- Custom assistant name (user picks; default Binai; changeable)

---

## Next priority

1. Real phone testing — Sherry (ZH iPhone) + Keiko (EN PC)
2. **Smart UX Phase 1c** ⭐ Keiko loves this — Catch Me Up, memory confirmation, welcome-back

## Keiko priority (Smart UX)

Catch Me Up button, memory confirmation moments, gentle suggestions on app open — makes memory *felt*. Web-first; no background services. Full spec: BINAI-PLAN.md § Smart UX.

---

## Name & concept

Named after Keiko's wife **Cheng Bin**. "ai" (爱) = love → Binai = Bin + love. Logo: 💜

Personal AI assistant on Lightchain AIVM. Remembers you. Privacy-first. $1/mo LCAI (beta free).

Tagline: *"The AI assistant that remembers everything about you, without Big Tech watching."*

---

## Stack

- Frontend: Capacitor / PWA (`index.html`)
- Backend: Railway Flask `server.py` · SQLite per wallet
- AI: aaaba relay → swap when AIVM REST API ships
- Memory: SQLite on Railway volume

---

## Who does what

| | |
|--|--|
| **Grok** | Code + deploy in `~/Desktop/binai/` |
| **Claude** | DNS, Railway env, copy, coordination |
| **Keiko** | Testing, product decisions |

**End of session:** update `BINAI-BRIEFING.md` + this file + Claude memory copy (same path in `~/.config/Claude/.../future_builds/binai.md`)

---

## Related

- OrcaVault / Lightchain Archives — Save to Archives target
- LightTunes — music connector target
- [[project_lightchat]] — voice UX patterns
- [[project_app_store_distribution]] — Google Play approved