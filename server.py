#!/usr/bin/env python3
"""Binai — Personal AI assistant backend. Memory + AIVM + subscriptions."""

import os
import re
import time
import json
import sqlite3
import threading
import urllib.request as urllib_req
from urllib.parse import quote as url_quote

import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=_ROOT, static_url_path="")
CORS(app, origins="*")

# ── CONFIG ───────────────────────────────────────────────────────────────────
AIVM_RELAY = os.environ.get(
    "AIVM_RELAY", "https://web-production-aaaba.up.railway.app"
)
OWNER_WALLET = os.environ.get(
    "OWNER_WALLET", "0x6518fd07b3da01b17bd37d7c40f9a5e3c87a09ba"
).lower()
MONTHLY_PRICE_USD = float(os.environ.get("MONTHLY_PRICE_USD", "1.00"))
FREE_ACTIONS_LIFETIME = int(os.environ.get("FREE_ACTIONS_LIFETIME", "5"))
# Beta default: everyone unlimited. Set TEST_MODE=false when billing goes live.
_test_flag = os.environ.get("TEST_MODE", "true").lower()
TEST_MODE = _test_flag not in ("0", "false", "no", "off")
LCAI_RPC = "https://rpc.mainnet.lightchain.ai"

_data_dir = os.environ.get("DATA_DIR", os.path.join(os.path.dirname(__file__), "data"))
os.makedirs(_data_dir, exist_ok=True)
DB_PATH = os.path.join(_data_dir, "binai.db")

_jobs = {}
_jobs_lock = threading.Lock()

BINAI_SYSTEM = """You are Binai 💜, a warm personal AI assistant powered by Lightchain AIVM.
You remember the user across sessions. Speak naturally, concisely, and kindly.
You are in BETA — responses may take up to 2 minutes (fast mode coming soon).

RULES:
- Use the user's name if you know it.
- Reference stored memories when relevant.
- For weather, reminders, notes — the app handles those; guide the user to use buttons if needed.
- Never claim to send texts, make calls, or access the phone until those features ship.
- If asked to remember something, confirm what you will remember.
- Lightchain community app — users know LCAI, AIVM, and the Orca Pod ecosystem.

USER PROFILE:
{profile}

LONG-TERM MEMORIES:
{memories}

RECENT CHAT (last few turns):
{recent_chat}
"""


# ── AIVM ADAPTER (swap this module when REST API lands) ──────────────────────

class AIVMProvider:
    """Today: aaaba HTTP relay. Tomorrow: REST API — change only this class."""

    @staticmethod
    def infer(prompt: str, timeout: int = 180) -> str:
        start = requests.post(
            f"{AIVM_RELAY}/api/chat",
            json={"message": prompt, "mode": "chat"},
            timeout=30,
        )
        if not start.ok:
            raise RuntimeError(f"AIVM start failed: {start.status_code} {start.text[:200]}")
        data = start.json()
        job_id = data.get("job_id")
        if not job_id:
            return data.get("reply") or data.get("message") or "No response from AIVM."
        deadline = time.time() + timeout
        while time.time() < deadline:
            time.sleep(5)
            poll = requests.get(
                f"{AIVM_RELAY}/api/chat/status",
                params={"job_id": job_id},
                timeout=15,
            )
            if not poll.ok:
                raise RuntimeError(f"AIVM poll failed: {poll.status_code}")
            pd = poll.json()
            if pd.get("status") == "done":
                return pd.get("reply") or ""
            if pd.get("status") == "error":
                raise RuntimeError(pd.get("error") or "AIVM job failed")
        raise RuntimeError("AIVM timed out — try again.")


# ── DATABASE ─────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            wallet TEXT PRIMARY KEY,
            display_name TEXT DEFAULT '',
            language TEXT DEFAULT 'en',
            preferences TEXT DEFAULT '{}',
            created_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT NOT NULL,
            content TEXT NOT NULL,
            due_at INTEGER,
            done INTEGER DEFAULT 0,
            created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS subscriptions (
            wallet TEXT PRIMARY KEY,
            expires_at INTEGER NOT NULL,
            tx_hash TEXT
        );
        CREATE TABLE IF NOT EXISTS usage (
            wallet TEXT PRIMARY KEY,
            actions_used INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS chat_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


init_db()


# ── HELPERS ──────────────────────────────────────────────────────────────────

_lcai_price_cache = {"price": 0.004, "ts": 0}


def get_lcai_price():
    global _lcai_price_cache
    now = time.time()
    if now - _lcai_price_cache["ts"] < 300:
        return _lcai_price_cache["price"]
    try:
        req = urllib_req.Request(
            "https://api.coingecko.com/api/v3/simple/price?ids=lightchain-ai&vs_currencies=usd",
            headers={"User-Agent": "Binai/1.0"},
        )
        with urllib_req.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            price = (data.get("lightchain-ai") or {}).get("usd")
            if price and float(price) > 0:
                _lcai_price_cache = {"price": float(price), "ts": now}
                return float(price)
    except Exception:
        pass
    try:
        req = urllib_req.Request(
            "https://api.dexscreener.com/latest/dex/search?q=LCAI",
            headers={"User-Agent": "Binai/1.0"},
        )
        with urllib_req.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            for pair in data.get("pairs") or []:
                price = float(pair.get("priceUsd") or 0)
                if price > 0:
                    _lcai_price_cache = {"price": price, "ts": now}
                    return price
    except Exception:
        pass
    _lcai_price_cache["ts"] = now
    return _lcai_price_cache["price"]


def norm_wallet(w):
    return (w or "").strip().lower()


def is_subscribed(wallet):
    w = norm_wallet(wallet)
    now = int(time.time())
    conn = get_db()
    row = conn.execute(
        "SELECT expires_at FROM subscriptions WHERE wallet = ?", (w,)
    ).fetchone()
    conn.close()
    return bool(row and row["expires_at"] > now)


def get_usage(wallet):
    w = norm_wallet(wallet)
    conn = get_db()
    row = conn.execute("SELECT actions_used FROM usage WHERE wallet = ?", (w,)).fetchone()
    conn.close()
    return row["actions_used"] if row else 0


def can_use_ai(wallet):
    if TEST_MODE:
        return True, "testing"
    if is_subscribed(wallet):
        return True, "subscribed"
    used = get_usage(wallet)
    if used < FREE_ACTIONS_LIFETIME:
        return True, "free"
    return False, "limit_reached"


def usage_payload(wallet):
    w = norm_wallet(wallet)
    used = get_usage(w)
    sub = is_subscribed(w)
    if TEST_MODE:
        return {
            "testing": True,
            "subscribed": False,
            "actions_used": used,
            "free_limit": FREE_ACTIONS_LIFETIME,
            "remaining_free": None,
            "tier": "testing",
        }
    return {
        "testing": False,
        "subscribed": sub,
        "actions_used": used,
        "free_limit": FREE_ACTIONS_LIFETIME,
        "remaining_free": max(0, FREE_ACTIONS_LIFETIME - used),
        "tier": "subscribed" if sub else "free",
    }


def increment_usage(wallet):
    w = norm_wallet(wallet)
    if TEST_MODE or is_subscribed(w):
        return
    conn = get_db()
    conn.execute(
        """INSERT INTO usage (wallet, actions_used) VALUES (?, 1)
           ON CONFLICT(wallet) DO UPDATE SET actions_used = actions_used + 1""",
        (w,),
    )
    conn.commit()
    conn.close()


def get_profile(wallet):
    w = norm_wallet(wallet)
    conn = get_db()
    row = conn.execute("SELECT * FROM profiles WHERE wallet = ?", (w,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def ensure_profile(wallet):
    w = norm_wallet(wallet)
    if get_profile(w):
        return
    now = int(time.time())
    conn = get_db()
    conn.execute(
        "INSERT INTO profiles (wallet, created_at, updated_at) VALUES (?, ?, ?)",
        (w, now, now),
    )
    conn.commit()
    conn.close()


def get_memories(wallet, limit=20):
    w = norm_wallet(wallet)
    conn = get_db()
    rows = conn.execute(
        "SELECT id, content, created_at FROM memories WHERE wallet = ? ORDER BY id DESC LIMIT ?",
        (w, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_memory(wallet, content):
    w = norm_wallet(wallet)
    content = (content or "").strip()
    if not content:
        return
    conn = get_db()
    conn.execute(
        "INSERT INTO memories (wallet, content, created_at) VALUES (?, ?, ?)",
        (w, content[:500], int(time.time())),
    )
    conn.commit()
    conn.close()


def maybe_extract_memory(wallet, message):
    msg = (message or "").strip()
    patterns = [
        r"(?:remember|don't forget|note that)\s+(?:that\s+)?(.+)",
        r"my name is\s+(.+)",
        r"i am\s+(.+)",
        r"call me\s+(.+)",
    ]
    for pat in patterns:
        m = re.search(pat, msg, re.I)
        if m:
            fact = m.group(1).strip().rstrip(".")
            if len(fact) > 3:
                add_memory(wallet, fact)
                if "name" in pat or "call me" in pat:
                    conn = get_db()
                    conn.execute(
                        "UPDATE profiles SET display_name = ?, updated_at = ? WHERE wallet = ?",
                        (fact.split()[0][:40], int(time.time()), norm_wallet(wallet)),
                    )
                    conn.commit()
                    conn.close()
            return


def get_recent_chat(wallet, limit=6):
    w = norm_wallet(wallet)
    conn = get_db()
    rows = conn.execute(
        """SELECT role, content FROM chat_log WHERE wallet = ?
           ORDER BY id DESC LIMIT ?""",
        (w, limit),
    ).fetchall()
    conn.close()
    lines = []
    for r in reversed(rows):
        lines.append(f"{r['role'].upper()}: {r['content']}")
    return "\n".join(lines) if lines else "(none yet)"


def log_chat(wallet, role, content):
    w = norm_wallet(wallet)
    conn = get_db()
    conn.execute(
        "INSERT INTO chat_log (wallet, role, content, created_at) VALUES (?, ?, ?, ?)",
        (w, role, content[:4000], int(time.time())),
    )
    conn.commit()
    conn.close()


def build_prompt(wallet, user_message):
    prof = get_profile(wallet) or {}
    prefs = json.loads(prof.get("preferences") or "{}")
    profile_text = json.dumps(
        {
            "name": prof.get("display_name") or "unknown",
            "language": prof.get("language") or "en",
            "preferences": prefs,
        },
        indent=2,
    )
    mems = get_memories(wallet)
    mem_text = (
        "\n".join(f"- {m['content']}" for m in mems)
        if mems
        else "(no memories yet — encourage user to share)"
    )
    system = BINAI_SYSTEM.format(
        profile=profile_text,
        memories=mem_text,
        recent_chat=get_recent_chat(wallet),
    )
    return f"{system}\n\nUSER: {user_message}\n\nBINAI:"


def lightchain_rpc(method, params):
    payload = json.dumps(
        {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    ).encode()
    req = urllib_req.Request(
        LCAI_RPC,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Binai/1.0"},
    )
    with urllib_req.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def fetch_weather(lat=None, lon=None, city=None):
    try:
        if lat is not None and lon is not None:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,weather_code,wind_speed_10m"
                f"&daily=temperature_2m_max,temperature_2m_min,weather_code"
                f"&timezone=auto&forecast_days=3"
            )
        elif city:
            geo_req = urllib_req.Request(
                f"https://geocoding-api.open-meteo.com/v1/search?name={url_quote(city)}&count=1",
                headers={"User-Agent": "Binai/1.0"},
            )
            with urllib_req.urlopen(geo_req, timeout=10) as gr:
                geo = json.loads(gr.read())
            results = geo.get("results") or []
            if not results:
                return None
            lat, lon = results[0]["latitude"], results[0]["longitude"]
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,weather_code"
                f"&timezone=auto"
            )
        else:
            return None
        req = urllib_req.Request(url, headers={"User-Agent": "Binai/1.0"})
        with urllib_req.urlopen(req, timeout=12) as r:
            return json.loads(r.read())
    except Exception:
        return None


WMO = {
    0: "clear", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "foggy", 61: "light rain", 63: "rain", 80: "rain showers",
    95: "thunderstorm",
}


# ── ROUTES ───────────────────────────────────────────────────────────────────

@app.route("/")
def serve_index():
    return send_from_directory(_ROOT, "index.html")


@app.route("/manifest.json")
def serve_manifest():
    return send_from_directory(_ROOT, "manifest.json")


@app.route("/api/health")
def health():
    return jsonify(
        {
            "ok": True,
            "service": "Binai",
            "aivm_relay": AIVM_RELAY,
            "free_actions": FREE_ACTIONS_LIFETIME,
            "test_mode": TEST_MODE,
            "beta": True,
        }
    )


@app.route("/api/price")
def api_price():
    price = get_lcai_price()
    required = MONTHLY_PRICE_USD / price if price else 0
    return jsonify(
        {
            "usd": MONTHLY_PRICE_USD,
            "lcai_price_usd": price,
            "required_lcai": round(required, 2),
            "owner_wallet": OWNER_WALLET,
        }
    )


@app.route("/api/subscription/<wallet>")
def api_subscription(wallet):
    w = norm_wallet(wallet)
    payload = usage_payload(w)
    conn = get_db()
    row = conn.execute(
        "SELECT expires_at FROM subscriptions WHERE wallet = ?", (w,)
    ).fetchone()
    conn.close()
    payload["expires_at"] = row["expires_at"] if row else None
    return jsonify(payload)


@app.route("/api/verify-subscription", methods=["POST"])
def verify_subscription():
    data = request.json or {}
    wallet = norm_wallet(data.get("wallet"))
    tx_hash = (data.get("tx_hash") or "").strip()
    if not wallet or not tx_hash:
        return jsonify({"error": "wallet and tx_hash required"}), 400
    try:
        tx = lightchain_rpc("eth_getTransactionByHash", [tx_hash])
        if not tx or not tx.get("to"):
            return jsonify({"error": "Transaction not found"}), 400
        if norm_wallet(tx.get("from")) != wallet:
            return jsonify({"error": "Transaction not from this wallet"}), 400
        if norm_wallet(tx.get("to")) != OWNER_WALLET:
            return jsonify({"error": "Payment not sent to owner wallet"}), 400
        value_wei = int(tx.get("value", "0x0"), 16)
        value_lcai = value_wei / 1e18
        price = get_lcai_price()
        required = MONTHLY_PRICE_USD / price if price else 999999
        if value_lcai < required * 0.9:
            return jsonify(
                {
                    "error": f"Insufficient LCAI. Need ~{required:.1f}, got {value_lcai:.2f}",
                }
            ), 400
        expires = int(time.time()) + 30 * 86400
        conn = get_db()
        conn.execute(
            """INSERT INTO subscriptions (wallet, expires_at, tx_hash) VALUES (?, ?, ?)
               ON CONFLICT(wallet) DO UPDATE SET expires_at = ?, tx_hash = ?""",
            (wallet, expires, tx_hash, expires, tx_hash),
        )
        conn.commit()
        conn.close()
        return jsonify({"subscribed": True, "expires_at": expires})
    except Exception as e:
        return jsonify({"error": str(e)[:200]}), 500


@app.route("/api/profile/<wallet>", methods=["GET", "POST"])
def api_profile(wallet):
    w = norm_wallet(wallet)
    ensure_profile(w)
    if request.method == "GET":
        prof = get_profile(w)
        return jsonify(prof or {})
    data = request.json or {}
    now = int(time.time())
    conn = get_db()
    conn.execute(
        """UPDATE profiles SET display_name = COALESCE(?, display_name),
           language = COALESCE(?, language),
           preferences = COALESCE(?, preferences),
           updated_at = ? WHERE wallet = ?""",
        (
            data.get("display_name"),
            data.get("language"),
            json.dumps(data["preferences"]) if "preferences" in data else None,
            now,
            w,
        ),
    )
    conn.commit()
    conn.close()
    return jsonify(get_profile(w))


@app.route("/api/memories/<wallet>", methods=["GET", "POST", "DELETE"])
def api_memories(wallet):
    w = norm_wallet(wallet)
    if request.method == "GET":
        return jsonify(get_memories(w))
    if request.method == "POST":
        data = request.json or {}
        add_memory(w, data.get("content", ""))
        return jsonify({"ok": True})
    mem_id = (request.json or {}).get("id")
    if mem_id:
        conn = get_db()
        conn.execute("DELETE FROM memories WHERE id = ? AND wallet = ?", (mem_id, w))
        conn.commit()
        conn.close()
    return jsonify({"ok": True})


@app.route("/api/notes/<wallet>", methods=["GET", "POST"])
def api_notes(wallet):
    w = norm_wallet(wallet)
    if request.method == "GET":
        conn = get_db()
        rows = conn.execute(
            "SELECT id, content, created_at FROM notes WHERE wallet = ? ORDER BY id DESC",
            (w,),
        ).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    data = request.json or {}
    content = (data.get("content") or "").strip()
    if not content:
        return jsonify({"error": "content required"}), 400
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO notes (wallet, content, created_at) VALUES (?, ?, ?)",
        (w, content, int(time.time())),
    )
    conn.commit()
    nid = cur.lastrowid
    conn.close()
    return jsonify({"id": nid, "content": content})


@app.route("/api/notes/<wallet>/<int:note_id>", methods=["DELETE"])
def delete_note(wallet, note_id):
    w = norm_wallet(wallet)
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ? AND wallet = ?", (note_id, w))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/reminders/<wallet>", methods=["GET", "POST"])
def api_reminders(wallet):
    w = norm_wallet(wallet)
    if request.method == "GET":
        conn = get_db()
        rows = conn.execute(
            """SELECT id, content, due_at, done, created_at FROM reminders
               WHERE wallet = ? ORDER BY done ASC, due_at ASC""",
            (w,),
        ).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    data = request.json or {}
    content = (data.get("content") or "").strip()
    if not content:
        return jsonify({"error": "content required"}), 400
    due_at = data.get("due_at")
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO reminders (wallet, content, due_at, created_at) VALUES (?, ?, ?, ?)",
        (w, content, due_at, int(time.time())),
    )
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return jsonify({"id": rid})


@app.route("/api/reminders/<wallet>/<int:rid>", methods=["PATCH", "DELETE"])
def patch_reminder(wallet, rid):
    w = norm_wallet(wallet)
    conn = get_db()
    if request.method == "DELETE":
        conn.execute("DELETE FROM reminders WHERE id = ? AND wallet = ?", (rid, w))
    else:
        done = (request.json or {}).get("done", 1)
        conn.execute(
            "UPDATE reminders SET done = ? WHERE id = ? AND wallet = ?",
            (1 if done else 0, rid, w),
        )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json or {}
    wallet = norm_wallet(data.get("wallet"))
    message = (data.get("message") or "").strip()
    if not wallet or not message:
        return jsonify({"error": "wallet and message required"}), 400
    ok, reason = can_use_ai(wallet)
    if not ok:
        return jsonify(
            {
                "error": "Free limit reached. Subscribe for $1/mo in LCAI.",
                "code": "limit_reached",
            }
        ), 402
    ensure_profile(wallet)
    maybe_extract_memory(wallet, message)
    log_chat(wallet, "user", message)
    prompt = build_prompt(wallet, message)
    try:
        reply = AIVMProvider.infer(prompt)
    except Exception as e:
        return jsonify({"error": str(e)[:300]}), 503
    log_chat(wallet, "assistant", reply)
    increment_usage(wallet)
    payload = usage_payload(wallet)
    payload.update({"reply": reply, "tier": reason})
    return jsonify(payload)


@app.route("/api/briefing/<wallet>")
def api_briefing(wallet):
    w = norm_wallet(wallet)
    prof = get_profile(w) or {}
    name = prof.get("display_name") or "friend"
    conn = get_db()
    notes_n = conn.execute(
        "SELECT COUNT(*) as c FROM notes WHERE wallet = ?", (w,)
    ).fetchone()["c"]
    rems = conn.execute(
        """SELECT content FROM reminders WHERE wallet = ? AND done = 0
           ORDER BY due_at ASC LIMIT 5""",
        (w,),
    ).fetchall()
    conn.close()
    mems = get_memories(w, 5)
    price = get_lcai_price()
    weather = fetch_weather(city="New York")
    wx_line = ""
    if weather and weather.get("current"):
        c = weather["current"]
        code = c.get("weather_code", 0)
        wx_line = f"Weather: {c.get('temperature_2m', '?')}°C, {WMO.get(code, 'conditions')}."
    rem_lines = [r["content"] for r in rems] or ["No open reminders."]
    mem_lines = [m["content"] for m in mems] or ["No memories yet — tell me about yourself!"]
    briefing = (
        f"Good morning, {name}! Here's your Binai briefing.\n\n"
        f"{wx_line}\n"
        f"LCAI price: about ${price:.4f} USD.\n"
        f"You have {notes_n} saved note(s).\n"
        f"Reminders: {'; '.join(rem_lines)}.\n"
        f"I remember: {'; '.join(mem_lines)}."
    )
    return jsonify({"briefing": briefing, "lcai_price": price})


@app.route("/api/weather")
def api_weather():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    city = request.args.get("city")
    data = fetch_weather(lat=lat, lon=lon, city=city)
    if not data:
        return jsonify({"error": "Weather unavailable"}), 404
    cur = data.get("current") or {}
    return jsonify(
        {
            "temp_c": cur.get("temperature_2m"),
            "description": WMO.get(cur.get("weather_code", 0), "unknown"),
            "raw": data,
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8190))
    app.run(host="0.0.0.0", port=port, debug=True)