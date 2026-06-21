# Binai 💜 — Full Project Plan
**Last updated:** 2026-06-21 (brainstorm session — Grok)  
**Status:** Phase 1 community beta — **web live at binai.win** · **brainstorming only** — camera, retention, and UX below are planned, not built yet  
**Owner:** Keiko (Keiko-Dev-LCAI)  
**Repo:** `~/Desktop/binai/` (local; push to `Keiko-Dev-LCAI/binai` when ready)  
**Latest commit:** `ed9ba46` (plan) · shipped code through `18e5a03` (About Me)

---

## 📁 Document map — Grok & Claude

| File | Purpose |
|------|---------|
| **`BINAI-BRIEFING.md`** | **Start here** — live status, priorities, who does what, session log, Claude paste block |
| **`BINAI-PLAN.md`** (this file) | Full product plan — features, brainstorm, phases, architecture, open questions |
| **`future_builds/binai.md`** | Claude memory node (started session 116) — sync with briefing; also in Claude app memory folder |

**Rule:** End of every Binai session → update `BINAI-BRIEFING.md` (always) + sections here if plan changed → commit → push.

| Role | Typical work |
|------|----------------|
| **Grok** | Code, deploy, tests in `~/Desktop/binai/` |
| **Claude** | DNS/infra, copy, coordination; reads both files before advising |
| **Keiko** | Product decisions, real-device testing, paste briefing into new Claude chats |

---

## Phase 1 Build — Session 132 (2026-06-20) ✅ STARTED

**Community-first beta** for Lightchain Discord testers. Slow AIVM accepted; memory is the wow.

| File | Purpose |
|------|---------|
| `server.py` | Flask backend — SQLite memory, subscriptions, AIVM adapter (`AIVMProvider` class) |
| `index.html` | PWA frontend — chat, voice, briefing, notes, reminders, memory, WalletConnect |
| `Procfile` / `requirements.txt` | Railway deploy |
| `capacitor.config.json` | Android wrap (next step after web beta works) |

**Live stack today:** `AIVMProvider` → `web-production-aaaba.up.railway.app` (swap one class when REST API ships).

**v1 includes:** wallet identity, 5 free actions, $1/mo LCAI sub, long-term memory, voice in/out (Web Speech API), morning briefing, notes, reminders.

**Shipped in web beta (2026-06-21):** see [Shipped Web Beta](#shipped-web-beta-2026-06-21) below.

**Not in v1 yet:** Capacitor Android build, camera/vision (Lens), user-controlled retention tiers, calls/SMS, phone cleaner, Play Store.

**Local dev:** `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && PORT=8190 .venv/bin/python server.py` → open `index.html` with backend at localhost:8190.

**Railway:** Project `binai` — **LIVE** at https://binai-production.up.railway.app · volume `binai-volume` at `/app/data` · repo `Keiko-Dev-LCAI/binai`  
**Domain:** `binai.win` ✅ live — Cloudflare CNAME → Railway (Claude session 134, 2026-06-20) · `www.binai.win` redirect not added yet (optional)

**Android:** `android/` folder scaffolded — build APK with Android Studio: `npx cap open android`

---

## Community Beta — Auth & Architecture

### Who pays for AI (TEST_MODE)

| Role | Wallet | Pays AIVM? |
|------|--------|------------|
| **Keiko (host)** | dApp payment wallet (~`0x729fea…`) | ✅ Yes — all inference during beta |
| **Testers (Sherry, Discord, etc.)** | Their own wallet | ❌ No — wallet = **identity only** |

- `TEST_MODE=true` on Railway — testers need **no LCAI** to chat
- UI copy: "Keiko pays for AI during beta; your wallet is your account"
- Subscription flow still exists for when beta ends

### Request flow

```
Phone/browser (binai.win)
  → Binai Railway (binai-production)
    → AIVM relay (orcaappbuilder-server)
      → https://web-production-aaaba.up.railway.app
        → Keiko payment wallet pays per inference
```

- Frontend uses **same-origin API** (`location.origin`) — fixes iPhone `Load failed`
- Chat is **async**: `POST /api/chat` → `job_id` → poll `/api/chat/status` (up to ~2 min)

### Testers

| Tester | Device | Language | Role |
|--------|--------|----------|------|
| **Sherry** | iPhone, Trust Wallet | Chinese UI + Chinese AI | Primary real-device tester |
| **Keiko** | PC (phone TBD) | English UI + English AI | Secondary tester |

---

## Community Beta — Testing Status

**Server/curl:** ✅ health, async chat, About Me API verified  
**Real phones:** ⚠️ **not fully done** after latest fixes — top priority before Discord scale

### Tomorrow checklist (both testers)

1. Hard refresh `binai.win` (close tab → reopen in Trust Wallet)
2. Send one message, wait on "thinking…" up to ~2 min — no `Load failed`
3. **English (Keiko):** UI in English, AI replies in English
4. **Chinese (Sherry):** UI in Chinese, AI replies in Chinese (no English welcome or mixed)
5. Note anything still wrong: wrong language, timeout, booking weirdness, wallet/PIN flow
6. **Reply length:** Keiko on **Short** → send `GM` → expect one line back
7. **About Me:** paste bio → Save → ask Binai something only in bio → confirm it knows
8. **Mute:** tap 🔇 → confirm no read-aloud
9. **Settings scroll (desktop):** scroll to PIN, export, legal

### Known gaps to watch

| Gap | Detail |
|-----|--------|
| **UI i18n** | `i18n-ui.js` = **English + Chinese only**; backend `languages.py` = 7 langs for AI |
| **Server PIN** | PIN locks device only — API trusts wallet address, no server-side PIN yet |
| **Data at rest** | SQLite on Railway — **not encrypted** like a bank vault (beta honesty) |
| **DNS** | `binai.win` on Cloudflare — confirm DNS → Railway if custom domain issues |

---

## Shipped Web Beta (2026-06-21)

| Commit | Feature |
|--------|---------|
| `f534087` | iPhone fix — same-origin API + async chat polling |
| `7f1d754` | Desktop scroll — Settings/Notes/Reminders panels scroll (`.main overflow-y: auto`) |
| `6e7d2da` | Mute voice — 🔊/🔇 next to mic; `binai_voice_muted` in localStorage |
| `da928af` | First-login setup wizard — language, personality, reply length, reminders, voice mute; once per wallet (`binai_prefs_setup_v1_<wallet>`) |
| `fb15579` | Shorter casual replies — instant one-liners for GM, time, holidays; trim AI ramble |
| `805afc2` | Reply length — **Short / Balanced / Chatty** in Settings + setup; `preferences.reply_depth`; personality defaults: direct→short, playful→chatty |
| `18e5a03` | **About Me** — 👤 tab, `/api/about-me/<wallet>` GET/POST, `profiles.bio` (12k chars), in AI prompt as PRIVATE ABOUT ME; export/delete clears bio |

### First-login setup wizard (shipped)

After wallet + PIN, new users see **"Set up your Binai"** popup:

1. Language  
2. AI personality (warm / direct / playful / professional)  
3. Reply length (Short / Balanced / Chatty)  
4. Political context (optional)  
5. Morning briefing on/off  
6. Reminder notifications on/off  
7. Mute voice on/off  

→ **"Save & start chatting"** → into chat. Returning users skip (once per wallet).

### Reply length (shipped)

| Mode | Who it's for | Behavior |
|------|--------------|----------|
| **⚡ Short** | GM-style pings | 1–2 sentences; instant one-liners for greetings/time |
| **💜 Balanced** | Default | Friendly, 2–4 sentences |
| **💬 Chatty** | Conversation lovers | Up to ~5 sentences; questions welcome |

- Stored in `preferences.reply_depth` per wallet
- `languages.py`: quick replies + `enforce_brief_reply` for Short mode
- Emotional messages ("bored", "feeling sad") always get real conversation regardless of mode

### Mute voice (shipped)

- 🔊/🔇 toggle next to mic in chat bar
- Mute stops current speech immediately
- Preference persists in `localStorage` (`binai_voice_muted`)
- Also available in first-login wizard and Settings

---

## What Is Binai?
A personal AI assistant for Android. Think Google Assistant, but powered by Lightchain AIVM — it knows you, remembers you across sessions, and controls your phone through natural voice commands. Built for everyone, not just tech users.

**Name meaning:** Named after Keiko's wife, Cheng Bin. In Chinese, "ai" (爱) means love — so Binai = Bin + love. Logo: 💜 (Lightchain purple heart — permanent).

**Tagline:** "The AI assistant that remembers everything about you, without Big Tech watching."

---

## Tech Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| Frontend | Capacitor | Web tech (HTML/JS/CSS) wrapped in native Android shell — same approach as other Keiko apps |
| Backend | Railway | Add as a new service inside an existing Railway project — share infra, no new project needed |
| AI | Lightchain AIVM | Server-side only (Railway calls AIVM). Same pattern as OrcaMail/LightChat |
| Memory | SQLite on Railway | Volume mount, per-user, keyed by wallet address |
| Distribution | Google Play | $25 one-time fee — already approved in Keiko's App Store Distribution Plan |
| Railway billing | CC on file | Already set up, no action needed |

---

## Why Build After REST API?
Current AIVM on-chain latency = 12–20 seconds per response. Too slow for a consumer assistant. The AIVM REST API is confirmed coming (after account abstraction ships). It will bring latency down to usable speeds. Design now, build after REST lands.

---

## Revenue Model

- **Price:** $1/month — no contracts; everything stops if unpaid (no partial free access)
- **Currency:** LCAI — dynamic pricing, LCAI equivalent of $1 USD at current rate (same pattern as SCExplainer)
- **Payment method:** WalletConnect (universal — works with all major wallets); QR code fallback for unsupported wallets
- **User payment options:**
  - Manual monthly — user pays each month themselves via WalletConnect
  - Auto-pay — relay pattern; user approves once, relay pulls monthly automatically (same as auto-subscription relay plan)
- **Free tier:** 5 AIVM actions lifetime — no more ever after that
- **Economics:** Each AIVM call costs ~0.02 LCAI; Keiko's node earns back on every query

**Why LCAI instead of Google Play billing:** This app is about building the Lightchain ecosystem, not maximizing profit. Every payment grows LCAI adoption.

### Payment Roadmap

**v1 — LCAI only (launch)**
- WalletConnect for crypto users
- Pay in LCAI directly
- Wallet address = user identity
- Simpler to build, targets existing Lightchain community first

**v2 — Dual track (future, after v1 is stable)**
- **Crypto track:** Same as v1 — WalletConnect, LCAI, on-chain identity
- **Normal track:** Email + password signup, Google Play billing ($1/month), managed wallet invisible under the hood — Keiko handles LCAI top-up behind the scenes
- Non-crypto users never see a wallet, never touch LCAI, never know it runs on Lightchain
- Tagline still works for both: "The AI assistant that remembers everything about you, without Big Tech watching"
- Reference: [[managed_wallet_auth]] — same pattern approved for LightView

---

## Required Disclosures (must be in app)
- No refunds under any circumstances
- App may go down temporarily or permanently at any time — no liability
- AI responses may be inaccurate — not professional advice
- Privacy policy — what is and isn't stored
- Permissions disclosure — why mic, contacts, calendar, location, and storage are needed
- Terms of service — payment terms, LCAI pricing is dynamic

---

## Onboarding Flow
1. Language selection on first launch (stored in user profile — controls voice input, AI responses, and TTS output)
   - Launch languages: English, Spanish, French, Portuguese, German, Japanese, Chinese (expandable)
2. App unlock setup: user chooses PIN, biometrics (fingerprint/face), or both — set at first launch, changeable in settings
3. Wallet connect for subscription
4. **Assistant name (brainstorm)** — optional in setup wizard; changeable anytime in Settings (see below)

---

## Custom Assistant Name — BRAINSTORM (locked direction: yes)

**Idea:** User picks what **their** AI is called — makes it feel personal. App product name stays **Binai**; the assistant they talk to can be Luna, Alex, 小助手, whatever they want.

### Today vs target

| | Today | Target |
|--|-------|--------|
| **User's name** | ✅ Settings — "What should Binai call you?" (`display_name`) | Same |
| **Assistant name** | ❌ Always "Binai" in AI + UI | ✅ User picks — default **Binai** if blank |
| **Changeable** | — | ✅ Settings + first-login wizard |

### What stays "Binai" (brand)

- App icon, store listing, legal, disclaimers, footer
- "Powered by Binai" or small subtitle if needed
- Keiko ecosystem / marketing

### What uses custom name

| Place | Example |
|-------|---------|
| **AI system prompt** | "You are Luna 💜, a warm personal assistant…" (note: runs on Binai / Lightchain) |
| **Chat placeholder** | "Talk to Luna…" |
| **Voice read-aloud** | Assistant refers to itself by chosen name |
| **Setup wizard** | "What should your assistant be called?" — default Binai, skippable |

### Suggested UX

- **Settings → Assistant name** — text field, 2–20 chars, emoji ok (💜 stays app-wide)
- **First-login wizard** — same field, after language; hint: *"Leave as Binai or pick your own — change anytime"*
- **Validation:** trim whitespace; block empty → fallback Binai; light profanity filter optional
- **Storage:** `preferences.assistant_name` in profile JSON (same pattern as `reply_depth`, `personality`)
- **i18n:** UI labels in en/zh; user's chosen name is **not translated**

### Why this is a good fit

- Pairs with **personality** (warm / direct / playful) and **presentation** prefs already in setup
- Makes the "remembers you" moment stronger — *"Good morning, Keiko" from Luna* hits different than generic bot
- Low risk — cosmetic + prompt change; no new permissions or infra
- **Changeable is mandatory** — people rename pets, cars, and assistants; lock-in feels wrong

### Implementation notes (when we build)

- `server.py`: inject `{assistant_name}` into `BINAI_SYSTEM` instead of hardcoded "Binai"
- `languages.py` / quick replies: use assistant name in greetings where appropriate
- `index.html` + `i18n-ui.js`: dynamic label helper `getAssistantName()` — default `"Binai"`
- Export / delete all data: include `assistant_name` in preferences
- Do **not** rename the app binary or domain — personal name is per-wallet preference only

---

## Full Feature List

### 🎤 Voice Assistant Core
- **Voice in / voice out** — speak to it, it speaks back; solves latency perception problem
- **Long-term memory** — remembers facts across sessions, knows who you are; stored per wallet in Railway SQLite

### 📱 Phone & Productivity
- **Calendar** — read and write events ("add dentist Tuesday 3pm") via `@capacitor/calendar`
- **Reminders** — fires even when app is closed via `@capacitor/local-notifications`
- **Timers & alarms** — "set a timer for 10 minutes" / "wake me up at 7am"; fires when app is closed
- **Notes & shopping list** — "take a note: call dentist" / "add milk to my shopping list"; stored in app
- **Make calls** — reads contacts, dials on command ("call mom"); no confirmation needed
- **Send texts** — AI drafts message, shows user for confirmation before sending; requires Play Store SMS permission declaration (personal assistant use case — approvable)

### 🌐 Web & Navigation
- **Open apps & websites** — "open lightchain website" → browser; "open YouTube" → YouTube app
- **Web search** — "search for X" → opens browser with query pre-filled; free, no API
- **Nearby search** — "find cheeseburger nearby" → grabs location, opens Google Maps pre-filled; free
- **Navigation** — "navigate to X" → launches Google Maps in navigation mode; Maps handles turn-by-turn audio; free

### 📊 Information & Data
- **Weather** — calls Open-Meteo API (free, no key needed), reads forecast aloud in-app; same source as LightWeather
- **Crypto prices** — calls DexScreener API (free, same as TopTen), reads price + % change aloud ("what's the price of LCAI?")
- **News headlines** — free news API, reads top headlines aloud
- **Math & conversions** — "what's 20% tip on $63?" / "how many miles is 15km?" / "convert $100 to euros?"; AI handles directly, no API
- **Translate** — "how do you say thank you in Japanese?"; AI handles directly, no API
- **Battery check** — "how's my battery?" → reads percentage aloud

### 📷 Camera & Vision ("Google Lens" for Binai) — BRAINSTORM → Phase 3

**Goal:** Point camera or pick a photo → ask what something is, read a label, identify a plant, etc.

| Piece | Plan |
|-------|------|
| **UI** | 📷 button in chat bar (next to mic); phone: camera or gallery via PWA `capture="environment"`; Android later: `@capacitor/camera` |
| **Vision backend (v1)** | Cloudflare Workers AI vision (e.g. LLaVA) — same stack as OrcaArt Workers AI; free tier |
| **Vision backend (v2)** | AIVM vision model when Lightchain ships it |
| **Flow** | Image → vision API → text description → optional follow-up in chat with context |
| **Privacy notice** | Photo sent to vision service to answer; not visible to other users; see retention model below |
| **Beta cost** | Keiko pays during TEST_MODE (same as chat) or per-user caps TBD |

**Example prompts:** "What is this?" · "Read this label" · "Is this plant healthy?" · OCR on menus/signs.

**Not in scope for v1 web:** continuous live Lens, AR overlay, photo library search (Capacitor Phase 5+).

### 📁 Files (later)
- **Photo search** — browse and search photo library by description via `@capacitor/filesystem`
- **File sharing** — pick a document, AI reads and discusses it

### 🌅 Morning Briefing
- One-tap button on main screen
- User customizes what's included in Settings (each item toggleable): weather, calendar events, news headlines, LCAI price, reminders
- AI reads the full briefing aloud

### 🔦 Utilities
- **Flashlight** — "turn on the flashlight"; hands-free, instant
- **Translate** — any language pair, AI handles it

### 🔗 Keiko App Connectors — BRAINSTORM (how Binai talks to other apps)

**Goal:** Say or tap one thing in Binai → something happens in another Keiko app. Same wallet everywhere. Easy to add new apps later without rebuilding Binai core.

#### Three save paths for a photo (don't mix these up)

| Button / voice | Where it goes | How long |
|----------------|---------------|----------|
| *(default)* | Binai vision only | ~24h then gone |
| **Save photo** | Binai account (retention model) | Until user deletes or changes retention |
| **Save to Archives** | **OrcaVault / Lightchain Archives** | **Forever on Lightchain** — on-chain, permanent |

Users who take a beautiful sunset and want it **forever** → **Save to Archives**, not Binai temp storage.

#### Connector pattern (reusable for every app)

```
User intent (voice or button)
  → Binai parses intent + wallet
    → Keiko App Registry (JSON manifest per app)
      → Action: deep link | embed panel | signed API call
        → Target app (OrcaVault, LightTunes, LightWeather, …)
```

| Layer | What it is |
|-------|------------|
| **Registry** | One JSON file — app id, name, URL, icon, enabled actions |
| **Intents** | `save_to_archive`, `play_playlist`, `open_weather`, … — Binai AI maps natural language → intent |
| **Deep link (fastest)** | `orcavault?vault=3&add=photo` · `lighttunes?playlist=1` · already partial on LightTunes (`?song=`) |
| **Embed panel** | iframe/slide-over inside Binai — user stays in assistant, music keeps playing |
| **postMessage API** | Child app listens: `binai.action.playPlaylist()` — clean cross-app control |
| **Signed relay** | Binai backend → `orcavault-production` relay with wallet signature (upload without leaving Binai) |

**User control:** Settings → **Connected apps** — toggle which apps Binai can open or act on. Off by default for sensitive apps.

**Why wallet-first helps:** OrcaVault, LightTunes, Binai all key off the same wallet — identity is already shared.

---

### 🗄️ OrcaVault / Lightchain Archives — BRAINSTORM

**App:** [Lightchain Archives](https://keiko-dev-lcai.github.io/orcavault/) (folder `orcavault-app/`) · relay `orcavault-production.up.railway.app`  
**Also called:** OrcaVault, Orca Archives — same product.

**What it does today:** User creates an **archive** (vault) — Family Album, Pet Album, Travel, etc. — and adds photos/videos/audio **on-chain forever**.

| Piece | Today |
|-------|-------|
| Vault templates | Family Album, Pet Album, Travel, Memorial, … |
| Add memory | `addMemory(vaultId, memType, title, caption, date, dataURI)` on-chain |
| Deep link | `?vault=3` or `?vault=3&item=2` |
| Relay | Thumbnails, visibility, moderation — same relay as LightTube |

#### Binai integration (planned)

**UI — after camera or on any photo answer:**
```
[Remember this]  [Save photo]  [Save to Archives ▾]  [Ask more]
```
Dropdown: pick vault — "Family Album", "Travel 2026", or **+ New archive**.

**Voice examples:**
- "Save this to my family album"
- "Add this picture to my pet archive"
- "Keep this photo forever on Lightchain"

**Build tiers:**

| Tier | Effort | Flow |
|------|--------|------|
| **v1 — Handoff** | Low | Binai passes image + vault hint via deep link → OrcaVault upload screen pre-filled; user confirms wallet tx |
| **v1.5 — In-app picker** | Medium | Binai lists user's vaults (read chain events for wallet) → pick album → handoff |
| **v2 — One tap** | Higher | Binai calls OrcaVault relay with signed upload; toast "Saved to Family Album 💜" — user may still approve tx |

**Default vault:** Binai remembers `preferences.default_archive_vault_id` per wallet (set in setup or first Save to Archives).

**Privacy copy:** "This photo will be stored **permanently on Lightchain** — visible in your archive. Not the same as Binai's temporary chat photos."

---

### 🎵 LightTunes Integration — BRAINSTORM (expanded)

**App:** `lighttunes-app/` · same OrcaVault relay · playlist in `localStorage` (`lt_playlist_<wallet>`)  
**Today:** `?song=123` deep link auto-plays one track · ♥ Playlist is private per wallet · auto-play next in playlist order.

#### Binai integration (planned)

**UI:**
- **🎵 Music** button in Binai sidebar or chat bar → opens LightTunes panel (embed or new tab)
- Quick actions: **Play my playlist** · **Play something chill** · **Pause** · **Next song**

**Voice examples:**
- "Play my playlist"
- "Put on some music"
- "Pause the music"
- "Next song"

**Build tiers:**

| Tier | Effort | Flow |
|------|--------|------|
| **v1 — Open + embed** | Low | Music panel iframe → `lighttunes` · user picks song manually · audio continues when back to chat |
| **v1.5 — Deep link** | Low | `lighttunes?playlist=1` (needs new param on LightTunes) or `?song=` for specific track |
| **v2 — Voice control** | Medium | LightTunes adds `postMessage` listener: `{ action: 'playPlaylist' }` · Binai iframe sends commands |
| **v3 — Android native** | Later | Capacitor media session — "pause/next" works with screen off |

**Playlist gap today:** LightTunes playlist lives in **browser localStorage** — Binai on another origin **cannot read it** until we add one of:
- `postMessage` from embedded LightTunes panel
- Binai stores "favorite playlist mood" in its own DB
- LightTunes exposes wallet-keyed playlist API on relay (optional v2)

**Mood presets (nice UX):** User picks default in Binai setup — "When I say play music, start my ♥ Playlist" or a genre channel.

---

### 🧹 Phone Cleaner (CCleaner-style)
All of the following are confirmed achievable on Android:
- **Duplicate photo/video finder** — find and delete duplicates
- **Large file scanner** — surface what's eating storage
- **Photo cleaner** — blurry shots, near-duplicates, old screenshots
- **Storage breakdown** — visual map of space usage
- **Download folder cleanup** — clear old downloads
- **App uninstaller** — launches system uninstall dialog for unused apps (user must confirm — Android requirement)
- **Clipboard cleaner** — clear clipboard contents
- **AI-guided cleanup** — AI explains what to clean and why, not just raw numbers

### ❌ NOT Possible on Android (do not attempt)
- Clear other apps' caches — Android sandboxing blocks this
- RAM booster / kill background apps — Android re-launches immediately, useless
- Startup manager — Android blocks regular apps from controlling boot sequence
- Silent app uninstall — Android always requires user confirmation, no workaround

---

## Capacitor Plugins Needed

| Plugin | Purpose |
|--------|---------|
| `@capacitor/calendar` | Calendar read/write |
| `@capacitor/local-notifications` | Reminders, timers, alarms |
| `@capacitor/camera` | Photo snap + gallery pick |
| `@capacitor/filesystem` | Photo search, file access |
| `@capacitor/speech-recognition` | Voice input |
| `@capacitor-community/text-to-speech` | Voice output (with language param) |
| WalletConnect SDK | LCAI payment |
| `@capacitor/biometric-auth` (or equivalent) | Fingerprint/face unlock |

---

## Architecture Notes

**How AIVM works in this app:**
- User speaks → Capacitor STT converts to text → sent to Railway backend → Railway calls AIVM → response comes back → Railway sends to app → Capacitor TTS reads it aloud
- Wallet address = user identity (no username/password)
- Long-term memory stored in SQLite on Railway, keyed by wallet

**Password/login security:**
- Binai does NOT store passwords — security liability
- For "log me into my bank": app opens the website, device's built-in Android autofill handles credentials, biometrics confirm
- Keiko's decision: never store credentials in Binai

---

## What's Already Built / Available to Reuse

| Asset | Where |
|-------|-------|
| Cloudflare Workers AI vision (free tier) | Already set up from Emojis app |
| Open-Meteo weather integration | Same as LightWeather |
| DexScreener price API | Same as TopTen |
| AIVM Railway server pattern | Same as OrcaMail, LightChat |
| Auto-subscription relay pattern | Designed, ready to implement |
| WalletConnect integration | Same pattern as other apps |
| Google Play account | Already active ($25 fee approved) |

---

## Build Philosophy & Product Principles

These principles were locked in during planning (2026-06-18) and should guide every build decision.

### Execution Strategy

| Area | Recommendation | Why |
|------|---------------|-----|
| Build Order | Use clear phases internally, even if everything ships in v1 | Makes development and testing manageable |
| Core Loop First | Voice + Long-term Memory must be rock solid before adding other features | This is what makes Binai feel different |
| Risky Features Last | Phone calls, SMS, and aggressive phone cleaning built last | Highest permission & Play Store risk |
| Testing Strategy | Internal testing phases before Play Store submission | Need time to test everything properly |
| Positioning | Make "remembers you + private + on Lightchain" visible in app | This is the real differentiator |

### Product Principles

- **Make memory the star.** Long-term memory is the strongest thing AIVM can offer. Lean into it hard — it's what nobody else does.
- **Don't copy Google Assistant 1:1.** Focus on what Binai does *better*: memory, privacy, on-chain nature. Features that don't serve that story can wait.
- **Have a clear "Why Binai?" in onboarding.** Normal users need to understand the benefit in the first 30 seconds.
- **Voice quality and speed above all.** Even with every feature built, a bad voice experience ruins the app. Get this right first.
- **The first return visit is the moment.** The wow moment is when a user comes back the next day and Binai already knows their name, their family, their preferences — without re-explaining. This must happen on the first return visit.
- **User controls what stays.** Default = temporary. Nothing kept forever unless the user explicitly taps Save / Remember / Save photo. Opposite of Big Tech hoovering.

---

## About Me — Private Bio (✅ shipped web beta)

| Item | Detail |
|------|--------|
| **Tab** | 👤 About Me (sidebar) / 👤 Me (mobile) |
| **Purpose** | Full life story — age, work, family, friends, favorites — paste once, up to 12k chars |
| **Privacy** | Only visible to user's wallet; used to personalize AI; **not saved as chat** |
| **Never store** | Seed phrases, passwords, payment cards (UI warning) |
| **Controls** | Included in Export; wiped on Delete all data |
| **vs Memory** | About Me = big private document; Memory = individual facts ("remember I like iced coffee") |
| **vs Notes** | Notes = user's own lists (not in AI prompt today); About Me = AI reads privately each chat |
| **vs Chat** | Chat "remember that…" = one fact at a time; Memory tab = 500 chars/item chips — bad for dumping whole bio |

### Privacy honesty (beta — tell users)

- Data on **Keiko's Railway server** in SQLite — not end-to-end encrypted
- When Binai replies, About Me + memories go in the **AI prompt** (same as any assistant)
- Other Binai users **cannot** browse your data — keyed by wallet
- PIN locks **your device only** — not a server login yet
- Export + Delete all data must always include bio (✅ wired)

### Future brainstorm (not built)

- **"Add to About Me"** button on a chat reply — append a life update without re-pasting whole doc
- Server-side PIN or session token before API accepts wallet address

---

## User-Controlled Retention — BRAINSTORM (locked direction)

**Core rule:** *Default = temporary. Keep only what the user explicitly asks to keep.*

Normal users should never wonder "did Binai keep that forever?" — they tapped a button or they didn't.

### Four retention levels

| Level | Meaning | User action (UI label) | Where it lives |
|-------|---------|------------------------|----------------|
| **1. This moment** | Ephemeral — auto-expires | *(default, no tap)* | Session / 24h queue |
| **2. Save message** | Keep this chat exchange | **Save this message** | Chat history (saved subset) |
| **3. Remember** | One fact Binai uses forever | **Remember** / **Remember this** | Memory table |
| **4. Keep file** | Photo or attachment stored | **Save this photo** | User media store (optional thumbnail in Memory) |

**Also map to existing features:**
- **About Me** — user edits & saves themselves (not from a chat button)
- **Notes** — "Add to Notes" for lists, receipts, labels
- **Reminders** — time-based, separate flow

### Photos (camera / Lens)

| Default | User choice |
|---------|-------------|
| Photo used for analysis → **auto-delete after 24 hours** (or immediately after answer — TBD in testing) | **Save this photo** — keep on account |
| Vision text not kept unless user acts | **Remember this** — e.g. "This is my philodendron" → Memory |
| | **Add to Notes** — label, receipt, etc. |

If user does nothing → photo gone. Privacy-first default.

### Chat messages (today vs target)

| Today (beta) | Target |
|--------------|--------|
| All chat logged until Delete all data | **Default:** rolling window (~24h) for unsaved messages; keep last N turns for AI context only |
| Remember via "remember …" in chat | **Remember** button on each Binai reply |
| — | **Save this message** on each reply |
| — | Optional later: **Add to About Me** for big life updates |

### Buttons under Binai replies (target UI)

```
[Remember]  [Save message]  [Wrong]
```

- **Remember** — extract one fact → Memory table (explicit consent, replaces typing "remember that…")
- **Save message** — keep this exchange in saved chat history
- **Wrong** — feedback when Binai got it wrong; log for quality, optionally trim bad memory (TBD)

After a photo answer:

```
[Remember this]  [Save photo]  [Save to Archives ▾]  [Add to Notes]  [Ask more]
```

- **Save to Archives** — permanent on-chain via OrcaVault (Family Album, etc.) — **not** Binai temp storage
- **Add to Notes** — receipt, label, list item — separate from Memory facts
- **Ask more** — follow-up question with same photo context (until photo expires)

Short labels. No jargon. i18n needed for all 7 launch languages when built.

### Optional Settings (power users)

- Chat retention: 24h / 7 days / 30 days / forever (default 24h)
- Photo auto-delete: 24h on (default) / off
- "Always ask before saving photos" toggle

### Implementation notes (when we build)

- `media_uploads` table: `wallet`, `blob or path`, `created_at`, `expires_at`, `saved` boolean
- Cron or lazy delete: purge `saved=0 AND expires_at < now`
- `chat_log.saved` flag or separate `saved_messages` table
- Memory extraction unchanged — user tap = explicit consent
- Export / Delete all data must include photos + saved messages

---

## Smart UX Improvements (AIVM Memory Advantage) — ⭐ KEIKO PRIORITY

**Keiko (2026-06-21):** *"I really like this one."* — This is the emotional core of Binai: not a command bot, but something that **understands your life** and reduces mental load. Memory is the moat; these UX patterns make memory *felt*.

The goal: Binai should feel like it already knows your day, your people, your habits — and gently helps without nagging.

| # | UX Improvement | How It Helps | Leverages AIVM | Priority |
|---|---------------|-------------|----------------|----------|
| 1 | **Smart Contextual Reminders** | Instead of just setting reminders, Binai says: "You usually leave for work around 7:30. Want me to remind you to take your keys?" | Memory + pattern recognition | Very High |
| 2 | **Proactive Daily Suggestions** | In the morning briefing, Binai offers 2–3 useful suggestions based on your day ("You have a dentist at 3pm — want me to prepare directions?") | Memory + calendar awareness | Very High |
| 3 | **Natural Follow-up Conversations** | After a command, Binai asks smart follow-ups. "Add milk to shopping list" → Binai: "Do you want me to check if you already have milk based on your last grocery run?" | Memory + reasoning | High |
| 4 | **One-Tap "Catch Me Up"** | Prominent button that summarizes calendar, reminders, notes, weather — everything you might have missed. Combine with "What did I miss?" (same feature) | Memory + context | **Very High** ⭐ |
| 5 | **Location + Time Awareness** | Time of day / location changes what Binai suggests. Evening at home = different context than Monday morning. Opt-in only — clearly disclosed | Context awareness | High |
| 6 | **Smart Defaults & Preferences** | Binai learns your preferences over time ("You always want weather in Celsius," "You prefer short answers in the morning") | Long-term memory | High *(partial — reply length shipped)* |
| 7 | **Low-Friction Task Creation** | Very natural language for tasks: "Remind me to call mom when I get home" / "Add buy birthday gift for Sarah for next week" | Natural language understanding | Medium-High |
| 8 | **Memory Confirmation Moments** | Occasionally confirm important memories: "Just to confirm — your daughter's name is Lily, right?" Builds trust in the memory system — more powerful than any explanation | Memory | **Very High** ⭐ |
| 9 | **Gentle Background Help** | When user does something repetitive, Binai can gently offer help. Example: blurry photo → Binai offers to enhance or organize. Keep this very limited and opt-in | Image analysis + context | Medium |

### What this feels like (examples users will notice)

| Moment | Binai says / does |
|--------|-------------------|
| **First open next morning** | "Good morning, Keiko ☀️ You wanted to call the dentist today — still want a reminder at 2pm?" |
| **Catch Me Up tap** | One read-aloud summary: 2 reminders due, 1 note about groceries, yesterday you said you're tired of takeout |
| **After you share family info** | "Just checking — your wife's name is Bin, right? I'll remember that." |
| **Evening open** | "Long day? You usually wind down around 9 — want me to hold notifications?" *(opt-in, gentle)* |
| **Shopping list add** | "Added milk. You already had eggs on your list from Tuesday — want the full list?" |

### Web-first vs needs Android (important)

**No true background on web/Android without Capacitor tricks** — trigger Smart UX **when user opens the app**, not while phone is locked. That's fine and matches "proactive but not annoying."

| Feature | Web beta now? | Needs |
|---------|---------------|-------|
| **Catch Me Up** (#4) | ✅ Yes — reminders, notes, memory, briefing already exist | One button + `/api/catch-up` or prompt bundle |
| **Memory confirmation** (#8) | ✅ Yes — prompt + occasional card after "remember" | AI instruction + light UI |
| **Time-of-day tone** (#5 partial) | ✅ Yes — server sends local time in prompt | Already mostly there; sharpen |
| **Proactive on open** (#2 partial) | ✅ Yes — one suggestion when app opens AM/PM | Memory + About Me + reminders; no calendar yet |
| **Natural follow-ups** (#3) | ✅ Yes — mostly prompt engineering | `languages.py` + system prompt |
| **Smart contextual reminders** (#1) | ⚠️ Partial — needs usage patterns over days | Memory history |
| **Calendar-aware suggestions** (#2 full) | ❌ | Phase 2 `@capacitor/calendar` |
| **Location hints** (#5 full) | ❌ | Opt-in geolocation + disclosure |
| **"When I get home"** (#7) | ❌ | Location or manual home time memory |

### Phase 1c — Smart UX (web) — BRAINSTORM build order

*After phone testing passes; before camera if Keiko wants the "wow" on memory first.*

1. **Catch Me Up** — big button on chat screen + voice phrase "what did I miss?"
2. **Memory confirmation** — after new memory saved, Binai may ask one confirm question (toggle in Settings)
3. **Welcome-back line** — on return visit, one personalized line from About Me + memories (not generic hello)
4. **Morning/evening open nudge** — max **one** proactive suggestion per open; dismissible
5. **Follow-up prompts** — system prompt: offer one relevant follow-up when user adds note/reminder/list item

**UI sketch — chat bar area:**
```
[☀️ Catch Me Up]  [🌅 Briefing]     ← prominent, above or beside chat input
```

**Settings toggle:** "Gentle suggestions when I open Binai" — default **on**; power users can off.

### Implementation Notes
- **Memory is the hero.** Make it very visible when Binai remembers something. That's the differentiator — say it out loud in the UI.
- **Reduce taps.** Catch Me Up = one tap for the whole mental load dump.
- **Proactive but not annoying.** Max one unsolicited suggestion per app open. Never interrupt mid-chat. Easy dismiss.
- **The first return visit is the moment.** Welcome-back + memory confirm + Catch Me Up are how we win the second day.
- **Show your work:** When Binai uses a memory, subtle "💜 from your memories" or "from About Me" builds trust (optional UI).
- **Background (Android later):** Features 1, 2 full, and 9 may use foreground service with consent — web uses app-open triggers only.

---

## Build Order — 6 Phases (when REST API is ready)

| Phase | Focus | Key Features | Goal |
|-------|-------|-------------|------|
| Phase 1 | Core Foundation | Voice loop (STT + TTS), Long-term Memory, About Me, Reply length, setup wizard, Subscription (WalletConnect + wallet identity + free tier gating) | Assistant remembers you — payment identity from day one |
| Phase 1b | Web beta hardening | iPhone async chat, mute voice, setup wizard, reply length, About Me, 7-language AI backend, **UI i18n (en+zh done; es/fr/pt/de/ja TBD)**, real-device testing (Keiko EN + Sherry ZH) | Trust core chat before scaling Discord |
| **Phase 1c** | **Smart UX (web)** ⭐ | Catch Me Up, memory confirmation, welcome-back line, gentle open suggestions, follow-up prompts | **Memory feels magical** — Keiko priority |
| Phase 2 | Daily Usefulness | Weather, Calendar, Reminders, Notes, Morning Briefing, Translate, Flashlight | Genuinely useful every day |
| Phase 2b | User-controlled retention | 24h default chat/photo expiry; **Remember** / **Save message** / **Save photo** buttons; optional retention Settings | User trusts what Binai keeps |
| Phase 3 | Camera & Vision | 📷 in chat, Cloudflare vision API, Lens-style Q&A, photo 24h delete + save opt-in | "What is this?" — show AIVM-era smarts |
| Phase 3b | **App Connectors v1** | Keiko App Registry JSON; **Save to Archives** handoff (OrcaVault deep link); **🎵 Music** embed (LightTunes iframe); Connected apps toggles in Settings | Ecosystem feels like one assistant |
| Phase 3c | Files + Archives v2 | Photo search, document pick; one-tap archive upload via signed relay; default vault per wallet | Beautiful pics saved forever on-chain |
| Phase 4 | Phone Control | Make calls, Send texts, Open apps/websites, Navigation | Full assistant experience |
| Phase 5 | Advanced Tools | LightTunes voice control (postMessage / media session), phone cleaner, Capacitor camera native | Power user features |
| Phase 6 | Polish & Launch | Permissions flow, Play Store submission, Lightchain dApp Hub submission | Ready for real users |

**Why subscription in Phase 1:** Wallet address = user identity throughout the whole app. Building payment and identity from the foundation means every feature that follows knows who the user is and whether they're on free or paid tier — no retrofitting later.

### Suggested build order (brainstorm 2026-06-21)

1. **Now:** Real phone testing — chat, About Me, reply length, Settings scroll  
2. **Next (Keiko priority):** **Smart UX web** — Catch Me Up + memory confirmation + welcome-back (Phase 1c)  
3. **Then:** User retention UI — Remember / Save message buttons + 24h chat roll-off (backend)  
4. **Then:** Camera v1 — 📷 + Cloudflare vision + 24h photo delete + Save photo / Remember this  
5. **Then:** App connectors v1 — Save to Archives (OrcaVault handoff) + LightTunes embed + registry JSON  
6. **Later:** Archives one-tap upload, LightTunes voice/play playlist, calendar-aware Smart UX, native Android

*Still brainstorming — nothing in this section is committed code until we pick it up in a build session.*

---

## Open Questions (brainstorm — not decided)

| # | Question | Options |
|---|----------|---------|
| 1 | Photo delete timing | 24h default vs delete immediately after answer |
| 2 | Unsaved chat window | Strict 24h roll-off vs keep last N turns for AI context only |
| 3 | **Wrong** button behavior | Just log vs offer to forget bad memory vs re-ask AI |
| 4 | Vision cost in beta | Keiko pays all (TEST_MODE) vs per-user daily cap |
| 5 | UI i18n before Discord | Ship es/fr/pt/de/ja UI strings now vs en+zh only for first testers |
| 6 | Photo storage | Railway volume blobs vs Cloudflare R2 vs vision-only (no store) |
| 7 | Booking / action replies | More canned filters vs wait for better AIVM tool use |
| 8 | Archives handoff vs one-tap | Deep link to OrcaVault (user confirms tx) vs Binai relay upload in background |
| 9 | LightTunes playlist | postMessage from embed vs new `?playlist=` deep link vs relay API |
| 10 | Which apps in registry v1 | OrcaVault + LightTunes only vs also LightWeather, TopTen, LightTube |
| 11 | Assistant name in wizard | Optional skip (default Binai) vs encourage pick on first login |
| 12 | Assistant name length | 20 chars vs allow longer; emoji in name yes/no |

---

## Claude Briefing

**Use `BINAI-BRIEFING.md`** in this folder — it has the current paste block, session log, and status snapshot.  
Update that file at the end of every session so Claude stays in sync (he has no memory between chats).

---

## Related Projects & Files
- **OrcaVault / Lightchain Archives** (`orcavault-app/`) — permanent photo/video albums on-chain; **Save to Archives** target
- **LightTunes** (`lighttunes-app/`) — music + private ♥ playlist; embed + voice control target
- **OrcaVault relay** (`orcavault-production.up.railway.app`) — shared by LightTube, LightTunes, Archives uploads
- **LightChat** (lightchat.chat) — voice AI already live; voice layer patterns apply here
- **OrcaMail** (orcamail.ai) — AIVM Railway server pattern to reuse
- **LightWeather** (lightweather.win) — Open-Meteo integration to reuse
- **TopTen** — DexScreener API integration to reuse
- **App Store Distribution Plan** — Google Play already approved
- **Auto-Subscription Relay** — future_builds/auto_subscription_relay.md
- **AIVM REST API** — build trigger; confirmed coming after account abstraction

---

*Grok + Claude: `BINAI-BRIEFING.md` = status · `BINAI-PLAN.md` = full spec · update both after every session*
