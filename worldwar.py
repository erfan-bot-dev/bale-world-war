import json
import time
import random
import sqlite3
import urllib.request
import re
import os
import threading
from flask import Flask
import libsql_experimental as libsql
import os

# ============================================================
# 🌍 جنگ جهانی شایسته ها
# نسخه تک فایلی - بدون Balethon
# API مستقیم Bale
# ============================================================


# ============================================================
# 🔑 تنظیمات
# ============================================================

TOKEN = os.environ.get("BOT_TOKEN", "my_bot_token")

API = f"https://tapi.bale.ai/bot{TOKEN}"

DATABASE_NAME = os.environ.get("DB_PATH", "world_war.db")

CHANNEL_USERNAME = "@shayestehaa"


# ============================================================
# 🌐 سرور HTTP کوچک برای بیدار نگه داشتن روی Koyeb
# ============================================================

web_app = Flask(__name__)


@web_app.route('/')
def home():
    return "alive"


@web_app.route('/health')
def health():
    return {"status": "ok"}, 200


def run_web():
    port = int(os.environ.get("PORT", 8080))
    print(f"🌐 Starting web server on port {port}")
    web_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


# ============================================================
# 🌍 کشورها
# ============================================================

COUNTRIES = [
    "ایران",
    "آمریکا",
    "کره شمالی",
    "کره جنوبی",
    "روسیه",
    "سوریه",
    "لبنان",
    "چین",
    "استرالیا",
    "نروژ",
    "هند",
    "ژاپن",
    "پاکستان",
    "افغانستان",
    "یمن",
    "سوئد",
    "اسرائیل",
    "ترکیه",
    "تاجیکستان",
    "قزاقستان",
    "مصر",
    "اسپانیا",
    "کانادا",
    "اردن",
    "آرژانتین",
    "فرانسه"
]


# ============================================================
# 🏆 لقب ها
# ============================================================

NICKNAMES = [
    "فاتح",
    "پولدار",
    "ابرقدرت",
    "سلطان منطقه",
    "غول کش"
]


# ============================================================
# ⛰ معادن
# ============================================================

MINES = {
    "الماس": {
        "price": 100_000,
        "income": 50_000
    },

    "طلا": {
        "price": 90_000,
        "income": 45_000
    }
}


# ============================================================
# 🚀 موشک ها
# قیمت / قدرت
# ============================================================

MISSILES = {

    "اراس ۲۸ سارمات": (2500, 500),

    "سجیل": (110, 200),

    "دونگ‌فنگ": (95, 100),

    "شهاب": (70, 55),

    "جریکو": (100, 65),

    "آگنی ۵": (365, 320),

    "هواسونگ": (560, 400),

    "تاماهاوک": (220, 230),

    "براهموس": (640, 380),

    "شیطان": (700, 300),

    "خیبر شکن": (1000, 800),

    "بالستیک تقویتی": (750, 450),

    "خا-۱۰۱": (65, 60),

    "زیرکان": (265, 230),

    "اسکندر": (260, 300),

    "فاتح": (80, 50),

    "فاتح ۱۱۰": (235, 200),

    "قیام": (200, 150),

    "اسکاد": (350, 175),

    "وی-۲": (90, 25),

    "هایپرسونیک": (550, 355),

    "هل‌فایر": (100, 80),

    "کورنت": (250, 160),

    "جاولین": (500, 330)
}


# ============================================================
# 🛩 تجهیزات هوایی / پهپادها
# ============================================================

DRONES = {
    "پهپاد ابابیل": (600, 90),
    "پهپاد هرون تیپی": (2000, 160),
    "پهپاد رستم ۲": (2005, 170),
    "پهپاد صاعقه": (320, 85),
    "پهپاد آذرخش": (450, 110),
    "پهپاد آرش": (800, 125),
    "پهپاد سپهر": (1200, 140),
    "پهپاد عقاب": (1800, 150),
    "پهپاد نگین": (3000, 190),
    "پهپاد فانتوم ایکس": (4500, 240)
}


# ============================================================
# ⚔ پدافندها
# ============================================================

DEFENSES = {

    "اس-۴۰۰": {
        "price": 900,
        "chance": 0.80
    },

    "اس-۳۰۰": {
        "price": 900,
        "chance": 0.80
    },

    "پاتریوت": {
        "price": 900,
        "chance": 0.80
    },

    "گنبد آهنین": {
        "price": 900,
        "chance": 0.80
    },

    "پانتسیر": {
        "price": 900,
        "chance": 0.80
    },

    "تور": {
        "price": 550,
        "chance": 0.70
    },

    "بوک": {
        "price": 550,
        "chance": 0.70
    },

    "پانزدهم خرداد": {
        "price": 550,
        "chance": 0.70
    },

    "باور-۳۷۳": {
        "price": 550,
        "chance": 0.70
    },

    "استر ۳۰": {
        "price": 550,
        "chance": 0.70
    },

    "تاد": {
        "price": 550,
        "chance": 0.70
    },

    "فلاخن داوود": {
        "price": 550,
        "chance": 0.70
    },

    "نسامس": {
        "price": 550,
        "chance": 0.70
    },

    "اس-۵۰۰": {
        "price": 550,
        "chance": 0.70
    },

    "سی اسپارو": {
        "price": 550,
        "chance": 0.70
    },

    "رپیر": {
        "price": 550,
        "chance": 0.70
    },

    "کورتال": {
        "price": 550,
        "chance": 0.70
    },

    "چاپارال": {
        "price": 550,
        "chance": 0.70
    },

    "اچ‌کیو-۹": {
        "price": 550,
        "chance": 0.70
    },

    "اداتس": {
        "price": 550,
        "chance": 0.70
    },

    "تونگوسکا": {
        "price": 550,
        "chance": 0.70
    },

    "هاوک": {
        "price": 550,
        "chance": 0.70
    },

    "باراک ۸": {
        "price": 550,
        "chance": 0.70
    },

    "آکاش": {
        "price": 550,
        "chance": 0.70
    },

    "میکا": {
        "price": 550,
        "chance": 0.70
    }
}


# ============================================================
# وضعیت های موقت
# ============================================================

pending_country = {}

pending_health = set()

pending_attack = {}
pending_attack_type = {}

# وضعیت فصل‌های هر گروه
BOT_ID = None


# ============================================================
# API
# ============================================================

def api(method, data=None):

    url = f"{API}/{method}"

    payload = json.dumps(
        data or {},
        ensure_ascii=False
    ).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=35
        ) as response:

            raw = response.read().decode("utf-8")

            return json.loads(raw)

    except Exception as error:

        print(
            f"[API ERROR] {method}: {error}"
        )

        return None


# ============================================================
# ارسال پیام
# ============================================================

def send_message(
    chat_id,
    text,
    reply_to=None,
    keyboard=None
):

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_to is not None:

        data["reply_to_message_id"] = reply_to

    if keyboard:

        data["reply_markup"] = {
            "inline_keyboard": keyboard
        }

    return api(
        "sendMessage",
        data
    )


# ============================================================
# ویرایش پیام
# ============================================================

def edit_message(
    chat_id,
    message_id,
    text,
    keyboard=None
):

    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    }

    if keyboard:

        data["reply_markup"] = {
            "inline_keyboard": keyboard
        }

    return api(
        "editMessageText",
        data
    )


# ============================================================
# پاسخ به دکمه
# ============================================================

def answer_callback(
    callback_id,
    text="",
    show_alert=False
):

    return api(
        "answerCallbackQuery",
        {
            "callback_query_id": callback_id,
            "text": text,
            "show_alert": show_alert
        }
    )


# ============================================================
# نرمال سازی متن
# ============================================================

def normalize(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace(
        "ي",
        "ی"
    )

    text = text.replace(
        "ى",
        "ی"
    )

    text = text.replace(
        "ك",
        "ک"
    )

    text = text.replace(
        "ۀ",
        "ه"
    )

    text = text.replace(
        "\u200c",
        " "
    )

    return text.strip()


# ============================================================
# اطلاعات کاربر
# ============================================================

def get_user(message):

    return (
        message.get("from")
        or message.get("author")
        or message.get("sender")
        or {}
    )


def get_user_id(message):

    user = get_user(message)

    return user.get("id")


def get_first_name(user):

    return (
        user.get("first_name")
        or user.get("firstName")
        or user.get("name")
        or "کاربر"
    )


# ============================================================
# نوع چت
# ============================================================

def is_group(message):

    chat = message.get(
        "chat",
        {}
    )

    chat_type = chat.get(
        "type",
        ""
    )

    return chat_type in (
        "group",
        "supergroup",
        "channel"
    )


# ============================================================
# DATABASE
# ============================================================

def get_connection():

    turso_url = os.environ.get("TURSO_URL")
    turso_token = os.environ.get("TURSO_TOKEN")

    if turso_url and turso_token:
        connection = libsql.connect("local_replica.db", sync_url=turso_url, auth_token=turso_token)
        connection.sync()
    else:
        connection = sqlite3.connect(DATABASE_NAME, timeout=30)

    connection.row_factory = sqlite3.Row

    return connection

# ============================================================
# ساخت جدول ها
# ============================================================

def migrate_country_schema():
    """قدیمی‌ترین نسخه یک UNIQUE سراسری روی کشور+لقب داشت؛
    این مهاجرت مالکیت کشور را به هر گروه مستقل می‌کند."""
    connection = get_connection()
    indexes = connection.execute("PRAGMA index_list(countries)").fetchall()
    has_global_unique = False
    for index in indexes:
        name = index[1]
        unique = index[2]
        if unique:
            cols = connection.execute(f"PRAGMA index_info(\"{name}\")").fetchall()
            names = [c[2] for c in cols]
            if names == ["country_name", "nickname"]:
                has_global_unique = True
                break
    connection.close()
    if not has_global_unique:
        return

    connection = get_connection()
    connection.execute("ALTER TABLE countries RENAME TO countries_old")
    connection.execute("""CREATE TABLE countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        country_name TEXT NOT NULL,
        nickname TEXT NOT NULL,
        balance INTEGER NOT NULL DEFAULT 500000,
        health INTEGER NOT NULL DEFAULT 10000,
        last_income_at REAL NOT NULL,
        UNIQUE(group_id, user_id),
        UNIQUE(group_id, country_name)
    )""")
    connection.execute("""INSERT INTO countries (id, group_id, user_id, country_name, nickname, balance, health, last_income_at)
                         SELECT id, group_id, user_id, country_name, nickname, balance, health, last_income_at FROM countries_old""")
    connection.execute("DROP TABLE countries_old")
    connection.commit()
    connection.close()
def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            group_id INTEGER NOT NULL,

            user_id INTEGER NOT NULL,

            country_name TEXT NOT NULL,

            nickname TEXT NOT NULL,

            balance INTEGER NOT NULL DEFAULT 500000,

            health INTEGER NOT NULL DEFAULT 10000,

            last_income_at REAL NOT NULL,

            UNIQUE(group_id, user_id),

            UNIQUE(country_name, nickname)

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mines (

            country_id INTEGER NOT NULL,

            mine_name TEXT NOT NULL,

            quantity INTEGER NOT NULL DEFAULT 0,

            PRIMARY KEY(
                country_id,
                mine_name
            )

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS missiles (

            country_id INTEGER NOT NULL,

            missile_name TEXT NOT NULL,

            quantity INTEGER NOT NULL DEFAULT 0,

            PRIMARY KEY(
                country_id,
                missile_name
            )

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drones (
            country_id INTEGER NOT NULL,
            drone_name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY(country_id, drone_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS defenses (

            country_id INTEGER NOT NULL,

            defense_name TEXT NOT NULL,

            quantity INTEGER NOT NULL DEFAULT 0,

            PRIMARY KEY(
                country_id,
                defense_name
            )

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_sessions (
            group_id INTEGER PRIMARY KEY,
            joined_at REAL NOT NULL,
            phase TEXT NOT NULL DEFAULT 'waiting',
            first_country_at REAL,
            prep_started_at REAL,
            war_started_at REAL,
            war_ends_at REAL,
            season INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS season_stats (
            group_id INTEGER NOT NULL,
            season INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            country_name TEXT NOT NULL,
            conquered_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY(group_id, season, user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS country_reservations (
            group_id INTEGER NOT NULL,
            country_name TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            reserved_at REAL NOT NULL,
            PRIMARY KEY(group_id, country_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conquests (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            attacker_country_id INTEGER NOT NULL,

            defeated_country_name TEXT NOT NULL,

            defeated_nickname TEXT NOT NULL,

            created_at REAL NOT NULL

        )
    """)

    connection.commit()

    connection.close()


# ============================================================
# ============================================================
# پاکسازی کشور فتح‌شده
# ============================================================

def remove_defeated_country(country_id):
    connection = get_connection()
    for table in ("mines", "missiles", "defenses", "drones"):
        connection.execute(f"DELETE FROM {table} WHERE country_id = ?", (country_id,))
    connection.execute("DELETE FROM countries WHERE id = ?", (country_id,))
    connection.commit()
    connection.close()


def cleanup_defeated_countries():
    connection = get_connection()
    rows = connection.execute("SELECT id FROM countries WHERE health <= 0").fetchall()
    for row in rows:
        country_id = row["id"]
        for table in ("mines", "missiles", "defenses", "drones"):
            connection.execute(f"DELETE FROM {table} WHERE country_id = ?", (country_id,))
        connection.execute("DELETE FROM countries WHERE id = ?", (country_id,))
    connection.commit()
    connection.close()


# درآمد ساعتی
# ============================================================

def calculate_hourly_income(country_id):

    connection = get_connection()

    total = 0

    for mine_name, info in MINES.items():

        row = connection.execute(
            """
            SELECT quantity
            FROM mines
            WHERE country_id = ?
            AND mine_name = ?
            """,
            (
                country_id,
                mine_name
            )
        ).fetchone()

        if row:

            total += (
                row["quantity"]
                * info["income"]
            )

    connection.close()

    return total


# ============================================================
# اعمال درآمد
# ============================================================

def apply_income(country_id):

    connection = get_connection()

    row = connection.execute(
        """
        SELECT
            balance,
            last_income_at
        FROM countries
        WHERE id = ?
        """,
        (country_id,)
    ).fetchone()

    if not row:

        connection.close()

        return

    now = time.time()

    elapsed = (
        now
        - row["last_income_at"]
    )

    hours = int(
        elapsed // 3600
    )

    if hours <= 0:

        connection.close()

        return

    hourly_income = calculate_hourly_income(
        country_id
    )

    earned = (
        hourly_income
        * hours
    )

    new_balance = (
        row["balance"]
        + earned
    )

    new_time = (
        row["last_income_at"]
        + hours * 3600
    )

    connection.execute(
        """
        UPDATE countries
        SET
            balance = ?,
            last_income_at = ?
        WHERE id = ?
        """,
        (
            new_balance,
            new_time,
            country_id
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# گرفتن کشور
# ============================================================

def get_country(
    group_id,
    user_id
):

    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM countries
        WHERE group_id = ?
        AND user_id = ?
        """,
        (
            group_id,
            user_id
        )
    ).fetchone()

    connection.close()

    if not row:

        return None

    apply_income(
        row["id"]
    )

    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM countries
        WHERE id = ?
        """,
        (row["id"],)
    ).fetchone()

    connection.close()

    return row


# ============================================================
# گرفتن کشور با نام و لقب
# ============================================================

def get_country_by_name(
    group_id,
    country_name,
    nickname
):

    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM countries
        WHERE group_id = ?
        AND country_name = ?
        AND nickname = ?
        """,
        (
            group_id,
            country_name,
            nickname
        )
    ).fetchone()

    connection.close()

    if row:

        apply_income(
            row["id"]
        )

    return row


# ============================================================
# 🌍 موتور فصل و زمان‌بندی گروه
# ============================================================

def get_group_session(group_id):
    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM group_sessions WHERE group_id = ?",
        (group_id,)
    ).fetchone()
    connection.close()
    return row


def group_phase(group_id):
    row = get_group_session(group_id)
    return row["phase"] if row else "not_started"


def ensure_group_session(group_id):
    row = get_group_session(group_id)
    if row:
        return row
    now = time.time()
    connection = get_connection()
    connection.execute(
        "INSERT OR IGNORE INTO group_sessions (group_id, joined_at, phase, season) VALUES (?, ?, 'waiting', 1)",
        (group_id, now)
    )
    connection.commit()
    connection.close()
    return get_group_session(group_id)


def mark_country_taken(group_id):
    session = get_group_session(group_id)
    if not session or session["phase"] != "country" or session["first_country_at"]:
        return
    now = time.time()
    connection = get_connection()
    connection.execute(
        "UPDATE group_sessions SET first_country_at = ? WHERE group_id = ? AND first_country_at IS NULL",
        (now, group_id)
    )
    connection.commit()
    connection.close()
    report_new_season(group_id)


def get_country_count(group_id):
    connection = get_connection()
    row = connection.execute("SELECT COUNT(*) AS c FROM countries WHERE group_id = ?", (group_id,)).fetchone()
    connection.close()
    return row["c"] if row else 0


def get_season_number(group_id):
    row = get_group_session(group_id)
    return row["season"] if row else 1


def record_conquest_for_season(group_id, user_id, country_name):
    season = get_season_number(group_id)
    connection = get_connection()
    connection.execute(
        """INSERT INTO season_stats (group_id, season, user_id, country_name, conquered_count)
           VALUES (?, ?, ?, ?, 1)
           ON CONFLICT(group_id, season, user_id) DO UPDATE SET conquered_count = conquered_count + 1""",
        (group_id, season, user_id, country_name)
    )
    connection.commit()
    connection.close()


def clear_pending_group_states(group_id):
    for key in list(pending_country):
        if key[0] == group_id:
            pending_country.pop(key, None)
    for key in list(pending_attack):
        if key[0] == group_id:
            pending_attack.pop(key, None)
            pending_attack_type.pop(key, None)
    for key in list(pending_health):
        if key[0] == group_id:
            pending_health.discard(key)


def reset_group_season(group_id):
    session = get_group_session(group_id)
    season = (session["season"] + 1) if session else 1
    connection = get_connection()
    country_ids = connection.execute("SELECT id FROM countries WHERE group_id = ?", (group_id,)).fetchall()
    for row in country_ids:
        cid = row["id"]
        for table in ("mines", "missiles", "defenses", "drones"):
            connection.execute(f"DELETE FROM {table} WHERE country_id = ?", (cid,))
    connection.execute("DELETE FROM countries WHERE group_id = ?", (group_id,))
    connection.execute("DELETE FROM conquests WHERE attacker_country_id NOT IN (SELECT id FROM countries)")
    connection.execute("DELETE FROM country_reservations WHERE group_id = ?", (group_id,))
    now = time.time()
    connection.execute(
        """INSERT INTO group_sessions (group_id, joined_at, phase, first_country_at, prep_started_at, war_started_at, war_ends_at, season)
           VALUES (?, ?, 'country', NULL, NULL, NULL, NULL, ?)
           ON CONFLICT(group_id) DO UPDATE SET joined_at=excluded.joined_at, phase='country', first_country_at=NULL, prep_started_at=NULL, war_started_at=NULL, war_ends_at=NULL, season=excluded.season""",
        (group_id, now, season)
    )
    connection.commit()
    connection.close()
    clear_pending_group_states(group_id)
    send_message(group_id, f"🔄 فصل جدید آغاز شد!\n\n🌍 فصل {season}\n🗺️ همه کشورها دوباره آزاد شدند.\n\n🇺🇳 برای انتخاب کشور بنویس:\nخرید کشور", keyboard=[[{"text":"🌍 خرید کشور","callback_data":"buy_country"}]])
    report_new_season(group_id)


def process_group_timers():
    connection = get_connection()
    sessions = connection.execute("SELECT * FROM group_sessions").fetchall()
    connection.close()
    now = time.time()
    for session in sessions:
        gid = session["group_id"]
        phase = session["phase"]
        if phase == "waiting" and now - session["joined_at"] >= 3600:
            connection = get_connection()
            connection.execute("UPDATE group_sessions SET phase='country' WHERE group_id=? AND phase='waiting'", (gid,))
            connection.commit(); connection.close()
            send_message(gid, "🚨🌍 کشورگیری آغاز شد! 🌍🚨\n\nاز همین لحظه هر بازیکن می‌تواند کشور خود را انتخاب کند.\n🇺🇳 کشور انتخاب‌شده دیگر در لیست دیگران نمایش داده نمی‌شود.\n\nبرای شروع بنویس: خرید کشور", keyboard=[[{"text":"🌍 خرید کشور","callback_data":"buy_country"}]])
        elif phase == "country" and session["first_country_at"] and now - session["first_country_at"] >= 1200:
            connection = get_connection()
            connection.execute("UPDATE group_sessions SET phase='prep', prep_started_at=? WHERE group_id=? AND phase='country'", (now, gid))
            connection.commit(); connection.close()
            send_message(gid, "🛡️🔥 مرحله قدرت‌سازی آغاز شد!\n\nکشور داران عزیز، شما ۲۴ ساعت کامل وقت دارید که کشور خود را قدرتمند کنید.\n⏳ از الان ۲۴ ساعت شروع می‌شود.\n🚫 در این مدت هیچ‌کس حق هیچ‌جور حمله‌ای ندارد.")
        elif phase == "prep" and session["prep_started_at"] and now - session["prep_started_at"] >= 86400:
            connection = get_connection()
            connection.execute("UPDATE group_sessions SET phase='war', war_started_at=?, war_ends_at=? WHERE group_id=? AND phase='prep'", (now, now + 1500, gid))
            connection.commit(); connection.close()
            send_message(gid, "🚨🌍 جنگ جهانی آغاز شد! 🌍🚨\n\n⚔️ از این لحظه همه تا ۲۵ دقیقه فرصت دارند کشور فتح کنند!\n🏆 هرکس کشورهای بیشتری فتح کند، برنده فصل است.\n⏰ زمان جنگ: ۲۵ دقیقه")
            report_war_started(gid)
        elif phase == "war" and session["war_ends_at"] and now >= session["war_ends_at"]:
            finish_group_war(gid)


def finish_group_war(group_id):
    session = get_group_session(group_id)
    if not session or session["phase"] != "war":
        return
    season = session["season"]
    connection = get_connection()
    rows = connection.execute(
        """SELECT s.user_id, s.country_name, s.conquered_count, c.nickname
           FROM season_stats s
           LEFT JOIN countries c ON c.user_id = s.user_id AND c.group_id = s.group_id
           WHERE s.group_id=? AND s.season=?
           ORDER BY s.conquered_count DESC, s.user_id ASC""",
        (group_id, season)
    ).fetchall()
    connection.close()
    if rows:
        winner = rows[0]
        leaderboard = "\n".join(f"{i+1}️⃣ {r['country_name']} — {r['conquered_count']} فتح" for i, r in enumerate(rows[:5]))
        text = f"🏆🌍 جنگ جهانی به پایان رسید! 🌍🏆\n\n👑 فاتح فصل: {winner['country_name']}\n⚔️ تعداد فتوحات: {winner['conquered_count']}\n\n📊 جدول برترین فاتحان:\n{leaderboard}\n\n🔄 فصل بعدی در حال آغاز است..."
        try:
            report_season_winner(
                group_id,
                winner["country_name"],
                winner["nickname"] or "بدون لقب",
                winner["user_id"],
                winner["conquered_count"]
            )
        except Exception as error:
            print(f"[WINNER REPORT ERROR] {error}")
    else:
        text = "🏆🌍 جنگ جهانی به پایان رسید! 🌍🏆\n\nهیچ فتحی در این فصل ثبت نشد.\n\n🔄 فصل بعدی آغاز می‌شود..."
    send_message(group_id, text)
    reset_group_season(group_id)


def reserve_country(group_id, country_name, user_id):
    connection = get_connection()
    connection.execute("DELETE FROM country_reservations WHERE reserved_at <= ?", (time.time()-600,))
    taken = connection.execute("SELECT id FROM countries WHERE group_id=? AND country_name=?", (group_id,country_name)).fetchone()
    reserved = connection.execute("SELECT user_id FROM country_reservations WHERE group_id=? AND country_name=?", (group_id,country_name)).fetchone()
    if taken or (reserved and reserved["user_id"] != user_id):
        connection.close(); return False
    connection.execute("INSERT OR REPLACE INTO country_reservations(group_id,country_name,user_id,reserved_at) VALUES(?,?,?,?)", (group_id,country_name,user_id,time.time()))
    connection.commit(); connection.close(); return True


def get_member_count(chat_id):
    result = api("getChatMemberCount", {"chat_id": chat_id})
    if isinstance(result, dict) and result.get("ok") and isinstance(result.get("result"), int):
        return result["result"]
    result = api("getChatMembersCount", {"chat_id": chat_id})
    if isinstance(result, dict) and result.get("ok") and isinstance(result.get("result"), int):
        return result["result"]
    return None


def leave_group(chat_id):
    return api("leaveChat", {"chat_id": chat_id})


def handle_bot_added(message):
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if not chat_id or not is_group(message):
        return False
    members = get_member_count(chat_id)
    if members is not None and members < 5:
        send_message(chat_id, "❌ من در گروه‌های کم‌جمعیت فعالیت نمی‌کنم.\n\n👥 حداقل اعضای موردنیاز: ۵ نفر\n👥 اعضای فعلی: " + str(members) + "\n\nوقتی گروه به ۵ نفر رسید، دوباره من را اضافه کنید.")
        leave_group(chat_id)
        return True
    ensure_group_session(chat_id)
    send_message(chat_id, "🎉🌍 به فرماندهان آینده خوش آمدم! 🌍🎉\n\n🔥 جنگ جهانی شایسته‌ها به‌زودی در این گروه آغاز می‌شود.\n⏳ یک ساعت تا شروع کشورگیری باقی مانده است.\n\nبعد از شروع، هر بازیکن فقط یک کشور می‌تواند انتخاب کند و کشور انتخاب‌شده برای دیگران آزاد نخواهد بود.")
    return True


def get_bot_id():
    global BOT_ID
    result = api("getMe")
    if isinstance(result, dict):
        user = result.get("result") or result.get("user") or {}
        BOT_ID = user.get("id")
    return BOT_ID


# ============================================================
# 📢 گزارش‌های کانال ویژه
# ============================================================

def get_chat_title(chat_id):
    """گرفتن اسم گروه از API"""
    result = api("getChat", {"chat_id": chat_id})
    if isinstance(result, dict):
        chat = result.get("result") or result.get("chat") or {}
        return chat.get("title") or f"گروه {chat_id}"
    return f"گروه {chat_id}"


def send_channel_report(text):
    """ارسال گزارش به کانال ویژه — خطا بازی رو خراب نمی‌کنه"""
    try:
        return send_message(CHANNEL_USERNAME, text)
    except Exception as error:
        print(f"[CHANNEL ERROR] {error}")
        return None


def format_username(user_id):
    """گرفتن یوزرنیم از API"""
    try:
        result = api("getChat", {"chat_id": user_id})
        if isinstance(result, dict):
            user = result.get("result") or result.get("user") or {}
            username = user.get("username")
            if username:
                return f"@{username}"
    except Exception:
        pass
    return "ندارد"


def report_new_season(group_id):
    """گزارش شروع فصل جدید در کانال"""
    title = get_chat_title(group_id)
    members = get_member_count(group_id) or "نامشخص"
    season = get_season_number(group_id)
    send_channel_report(
        f"🔄🌍 سیزن جدید شروع شد!\n\n"
        f"📛 گروه: {title}\n"
        f"👥 اعضای گروه: {members} نفر\n"
        f"🎯 فصل: {season}\n\n"
        f"⏳ یک ساعت تا شروع کشورگیری..."
    )


def report_war_started(group_id):
    """گزارش شروع جنگ در کانال"""
    title = get_chat_title(group_id)
    connection = get_connection()
    rows = connection.execute(
        "SELECT country_name, nickname FROM countries WHERE group_id = ?",
        (group_id,)
    ).fetchall()
    connection.close()
    if rows:
        countries_text = "\n".join(
            f"• {r['country_name']} ({r['nickname']})" for r in rows
        )
    else:
        countries_text = "• هیچ کشوری ثبت نشده"
    send_channel_report(
        f"⚔️🔥 جنگ جهانی آغاز شد!\n\n"
        f"📛 گروه: {title}\n\n"
        f"🌍 کشورهای حاضر در جنگ:\n{countries_text}\n\n"
        f"⏰ زمان جنگ: ۲۵ دقیقه"
    )


def report_attack(group_id, attacker, defender, weapon_name, quantity,
                  total_power, probability, intercepted, hit, damage,
                  is_drone=False):
    """گزارش حمله در کانال"""
    title = get_chat_title(group_id)
    icon = "🛩" if is_drone else "🚀"
    if damage > 0:
        result_line = "✅ حمله موفق"
    else:
        result_line = "🛡 قدرت دفاعی ما بی‌نظیر است!"
    send_channel_report(
        f"🌐 گزارش جهانی از حمله\n\n"
        f"📛 گروه: {title}\n"
        f"🎯 کشور حمله‌کننده: {attacker['country_name']} ({attacker['nickname']})\n"
        f"🛡 کشور مدافع: {defender['country_name']} ({defender['nickname']})\n"
        f"{icon} تجهیزات: {quantity} × {weapon_name}\n"
        f"💥 قدرت کل: {money(total_power)}\n"
        f"📊 احتمال موفقیت: {probability}٪\n"
        f"🚧 رهگیری شده: {intercepted}\n"
        f"💣 خسارت وارد شده: {money(damage)}\n\n"
        f"{result_line}"
    )


def report_conquest(group_id, attacker, defender, weapon_name, quantity,
                    is_drone=False):
    """گزارش فتح کامل در کانال"""
    title = get_chat_title(group_id)
    icon = "🛩" if is_drone else "🚀"
    send_channel_report(
        f"🌐🏆 گزارش جهانی: فتح کامل\n\n"
        f"📛 گروه: {title}\n"
        f"⚔️ کشور فاتح: {attacker['country_name']} ({attacker['nickname']})\n"
        f"🌍 کشور فتح‌شده: {defender['country_name']} ({defender['nickname']})\n"
        f"{icon} تجهیزات: {quantity} × {weapon_name}\n\n"
        f"💀 دشمن سقوط کرد"
    )


def report_season_winner(group_id, winner_country_name, winner_nickname,
                         winner_user_id, conquered_count):
    """گزارش فاتح فصل در کانال"""
    title = get_chat_title(group_id)
    username = format_username(winner_user_id)
    send_channel_report(
        f"🏆🌍 پایان فصل!\n\n"
        f"📛 گروه: {title}\n\n"
        f"👑 فاتح جهان در گروه {title}\n"
        f"کسی نیست جز: {winner_country_name} ({winner_nickname})\n"
        f"🆔 آیدی: {winner_user_id}\n"
        f"🔗 یوزرنیم: {username}\n"
        f"⚔️ تعداد فتوحات: {conquered_count}\n\n"
        f"🔄 فصل بعدی به‌زودی آغاز می‌شود..."
    )
# ============================================================
# ساخت کشور
# ============================================================

def create_country(
    group_id,
    user_id,
    country_name,
    nickname
):

    connection = get_connection()

    user_country = connection.execute(
        """
        SELECT id
        FROM countries
        WHERE group_id = ?
        AND user_id = ?
        """,
        (
            group_id,
            user_id
        )
    ).fetchone()

    if user_country:

        connection.close()

        return False, "already"

    same_name = connection.execute(
        """
        SELECT id
        FROM countries
        WHERE group_id = ?
        AND country_name = ?
        """,
        (group_id, country_name)
    ).fetchone()

    if same_name:

        connection.close()

        return False, "taken"

    now = time.time()

    cursor = connection.execute(
        """
        INSERT INTO countries
        (
            group_id,
            user_id,
            country_name,
            nickname,
            balance,
            health,
            last_income_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            group_id,
            user_id,
            country_name,
            nickname,
            500000,
            10000,
            now
        )
    )

    country_id = cursor.lastrowid

    for mine_name in MINES:

        connection.execute(
            """
            INSERT INTO mines
            (
                country_id,
                mine_name,
                quantity
            )
            VALUES (?, ?, 0)
            """,
            (
                country_id,
                mine_name
            )
        )

    for missile_name in MISSILES:

        connection.execute(
            """
            INSERT INTO missiles
            (
                country_id,
                missile_name,
                quantity
            )
            VALUES (?, ?, 0)
            """,
            (
                country_id,
                missile_name
            )
        )

    for drone_name in DRONES:
        connection.execute(
            "INSERT INTO drones (country_id, drone_name, quantity) VALUES (?, ?, 0)",
            (country_id, drone_name)
        )

    for defense_name in DEFENSES:

        connection.execute(
            """
            INSERT INTO defenses
            (
                country_id,
                defense_name,
                quantity
            )
            VALUES (?, ?, 0)
            """,
            (
                country_id,
                defense_name
            )
        )

    connection.execute(
        "DELETE FROM country_reservations WHERE group_id = ? AND country_name = ?",
        (group_id, country_name)
    )
    connection.commit()

    connection.close()

    mark_country_taken(group_id)
    return True, "created"


# ============================================================
# موجودی پول
# ============================================================

def get_balance(country_id):

    apply_income(
        country_id
    )

    connection = get_connection()

    row = connection.execute(
        """
        SELECT balance
        FROM countries
        WHERE id = ?
        """,
        (country_id,)
    ).fetchone()

    connection.close()

    if not row:

        return 0

    return row["balance"]


# ============================================================
# تغییر پول
# ============================================================

def change_balance(
    country_id,
    amount
):

    apply_income(
        country_id
    )

    connection = get_connection()

    row = connection.execute(
        """
        SELECT balance
        FROM countries
        WHERE id = ?
        """,
        (country_id,)
    ).fetchone()

    if not row:

        connection.close()

        return False

    new_balance = (
        row["balance"]
        + amount
    )

    if new_balance < 0:

        connection.close()

        return False

    connection.execute(
        """
        UPDATE countries
        SET balance = ?
        WHERE id = ?
        """,
        (
            new_balance,
            country_id
        )
    )

    connection.commit()

    connection.close()

    return True


# ============================================================
# موجودی آیتم
# ============================================================

def get_quantity(
    table,
    country_id,
    item_name
):

    columns = {
        "mines": "mine_name",
        "missiles": "missile_name",
        "defenses": "defense_name",
        "drones": "drone_name"
    }

    if table not in columns:

        return 0

    column = columns[table]

    connection = get_connection()

    row = connection.execute(
        f"""
        SELECT quantity
        FROM {table}
        WHERE country_id = ?
        AND {column} = ?
        """,
        (
            country_id,
            item_name
        )
    ).fetchone()

    connection.close()

    if not row:

        return 0

    return row["quantity"]


# ============================================================
# اضافه کردن آیتم
# ============================================================

def add_quantity(
    table,
    country_id,
    item_name,
    amount
):

    columns = {
        "mines": "mine_name",
        "missiles": "missile_name",
        "defenses": "defense_name",
        "drones": "drone_name"
    }

    if table not in columns:

        return False

    column = columns[table]

    connection = get_connection()

    connection.execute(
        f"""
        INSERT INTO {table}
        (
            country_id,
            {column},
            quantity
        )
        VALUES (?, ?, ?)

        ON CONFLICT(
            country_id,
            {column}
        )

        DO UPDATE SET
            quantity =
            quantity
            + excluded.quantity
        """,
        (
            country_id,
            item_name,
            amount
        )
    )

    connection.commit()

    connection.close()

    return True


# ============================================================
# کم کردن آیتم
# ============================================================

def remove_quantity(
    table,
    country_id,
    item_name,
    amount
):

    current = get_quantity(
        table,
        country_id,
        item_name
    )

    if current < amount:

        return False

    columns = {
        "mines": "mine_name",
        "missiles": "missile_name",
        "defenses": "defense_name",
        "drones": "drone_name"
    }

    if table not in columns:

        return False

    column = columns[table]

    connection = get_connection()

    connection.execute(
        f"""
        UPDATE {table}
        SET quantity = quantity - ?
        WHERE country_id = ?
        AND {column} = ?
        """,
        (
            amount,
            country_id,
            item_name
        )
    )

    connection.commit()

    connection.close()

    return True


# ============================================================
# گرفتن انبار
# ============================================================

def get_inventory(
    table,
    country_id
):

    connection = get_connection()

    rows = connection.execute(
        f"""
        SELECT *
        FROM {table}
        WHERE country_id = ?
        AND quantity > 0
        """,
        (country_id,)
    ).fetchall()

    connection.close()

    return rows


# ============================================================
# تغییر سلامت
# ============================================================

def set_health(
    country_id,
    health
):

    connection = get_connection()

    connection.execute(
        """
        UPDATE countries
        SET health = ?
        WHERE id = ?
        """,
        (
            health,
            country_id
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# کشور فتح شده
# ============================================================

def add_conquest(
    attacker_country_id,
    defeated_country_name,
    defeated_nickname
):

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO conquests
        (
            attacker_country_id,
            defeated_country_name,
            defeated_nickname,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            attacker_country_id,
            defeated_country_name,
            defeated_nickname,
            time.time()
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# لیست کشور های فتح شده
# ============================================================

def get_conquests(
    country_id
):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            defeated_country_name,
            defeated_nickname
        FROM conquests
        WHERE attacker_country_id = ?
        ORDER BY id DESC
        """,
        (country_id,)
    ).fetchall()

    connection.close()

    return rows


# ============================================================
# فرمت پول
# ============================================================

def money(number):

    return f"{int(number):,}"


# ============================================================
# دکمه انتخاب کشور
# ============================================================

def country_keyboard(chat_id=None, owner_id=None):

    taken = set()

    if chat_id is not None:
        connection = get_connection()
        rows = connection.execute(
            "SELECT country_name FROM countries WHERE group_id = ?",
            (chat_id,)
        ).fetchall()
        taken.update(row["country_name"] for row in rows)
        rows = connection.execute(
            "SELECT country_name FROM country_reservations WHERE group_id = ? AND reserved_at > ?",
            (chat_id, time.time() - 600)
        ).fetchall()
        taken.update(row["country_name"] for row in rows)
        connection.execute(
            "DELETE FROM country_reservations WHERE reserved_at <= ?",
            (time.time() - 600,)
        )
        connection.commit()
        connection.close()

    keyboard = []
    row = []
    for index, country in enumerate(COUNTRIES):
        if country in taken:
            continue
        callback_data = f"country:{index}" if owner_id is None else f"country:{index}:{owner_id}"
        row.append({"text": country, "callback_data": callback_data})
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return keyboard


# ============================================================
# دکمه انتخاب لقب
# ============================================================

def nickname_keyboard(owner_id=None):

    keyboard = []

    row = []

    for index, nickname in enumerate(NICKNAMES):

        row.append(
            {
                "text": nickname,
                "callback_data": f"nick:{index}" if owner_id is None else f"nick:{index}:{owner_id}"
            }
        )

        if len(row) == 2:

            keyboard.append(row)

            row = []

    if row:

        keyboard.append(row)

    return keyboard


# ============================================================
# متن لیست تجهیزات
# ============================================================

def country_panel(country):

    country_id = country["id"]

    apply_income(
        country_id
    )

    connection = get_connection()

    country = connection.execute(
        """
        SELECT *
        FROM countries
        WHERE id = ?
        """,
        (country_id,)
    ).fetchone()

    connection.close()

    income = calculate_hourly_income(
        country_id
    )

    # -------------------------
    # معادن
    # -------------------------

    mine_rows = get_inventory(
        "mines",
        country_id
    )

    if mine_rows:

        mines_text = []

        for row in mine_rows:

            name = row["mine_name"]

            quantity = row["quantity"]

            hourly = MINES[name]["income"]

            mines_text.append(
                f"• {name}: {quantity} عدد"
                f" | {money(hourly)}$ در ساعت"
            )

        mines = "\n".join(
            mines_text
        )

    else:

        mines = "• ندارد"

    # -------------------------
    # موشک ها
    # -------------------------

    missile_rows = get_inventory(
        "missiles",
        country_id
    )

    if missile_rows:

        missiles_text = []

        for row in missile_rows:

            name = row["missile_name"]

            quantity = row["quantity"]

            power = MISSILES[name][1]

            missiles_text.append(
                f"• {name}: {quantity} عدد"
                f" | قدرت {power}"
            )

        missiles = "\n".join(
            missiles_text
        )

    else:

        missiles = "• ندارد"

    # -------------------------
    # تجهیزات هوایی
    # -------------------------

    drone_rows = get_inventory("drones", country_id)
    if drone_rows:
        drones_text = []
        for row in drone_rows:
            name = row["drone_name"]
            drones_text.append(
                f"• {name}: {row['quantity']} عدد | قدرت {DRONES[name][1]}"
            )
        drones = "\n".join(drones_text)
    else:
        drones = "• ندارد"

    # -------------------------
    # پدافند
    # -------------------------

    defense_rows = get_inventory(
        "defenses",
        country_id
    )

    if defense_rows:

        defenses_text = []

        for row in defense_rows:

            name = row["defense_name"]

            quantity = row["quantity"]

            chance = int(
                DEFENSES[name]["chance"] * 100
            )

            defenses_text.append(
                f"• {name}: {quantity} عدد"
                f" | شانس دفع {chance}٪"
            )

        defenses = "\n".join(
            defenses_text
        )

    else:

        defenses = "• ندارد"

    # -------------------------
    # فتوحات
    # -------------------------

    conquests = get_conquests(
        country_id
    )

    if conquests:

        conquest_text = []

        for row in conquests:

            conquest_text.append(
                f"• {row['defeated_country_name']}"
                f" ({row['defeated_nickname']})"
            )

        conquered = "\n".join(
            conquest_text
        )

    else:

        conquered = "• ندارد"

    return (
        f"⚖ لیست تجهیزات کلی کشور "
        f"{country['country_name']} "
        f"({country['nickname']})\n\n"

        f"💰 موجودی بانک مرکزی کشور: "
        f"{money(country['balance'])} دلار\n"

        f"💵 درآمد ساعتی کشور: "
        f"{money(income)} دلار\n\n"

        f"⛰ معادن فعال:\n"
        f"{mines}\n\n"

        f"🚀 تجهیزات هجومی:\n"
        f"{missiles}\n\n"

        f"🛩 تجهیزات هوایی:\n"
        f"{drones}\n\n"

        f"⚔ تجهیزات دفاعی:\n"
        f"{defenses}\n\n"

        f"🔫 کشور های سرنگون کرده:\n"
        f"{conquered}\n\n"

        f"🩸 سلامت: "
        f"{money(country['health'])}"
    )


# ============================================================
# نمایش پنل کشور
# ============================================================

def send_country_panel(
    chat_id,
    country,
    reply_to=None
):

    owner_id = country["user_id"]

    keyboard = [

        [
            {
                "text": "⛰ خرید معدن",
                "callback_data": f"menu:{owner_id}:mines"
            },
            {
                "text": "🚀 خرید موشک",
                "callback_data": f"menu:{owner_id}:missiles"
            },
            {
                "text": "🛩 خرید پهپاد",
                "callback_data": f"menu:{owner_id}:drones_buy"
            }
        ],

        [
            {
                "text": "⚔ خرید پدافند",
                "callback_data": f"menu:{owner_id}:defenses"
            },
            {
                "text": "🩸 افزایش سلامت",
                "callback_data": f"menu:{owner_id}:health"
            }
        ]

    ]

    send_message(
        chat_id,
        country_panel(country),
        reply_to=reply_to,
        keyboard=keyboard
    )


# ============================================================
# منوی معدن
# ============================================================

def mine_menu():

    return (
        "🔮 لیست معادن درآمد زای بازی:\n\n"

        "💎 معدن الماس\n"
        "قیمت: 100,000 دلار\n"
        "📥 درآمد ساعتی: 50,000 دلار\n\n"

        "🏆 معدن طلا\n"
        "قیمت: 90,000 دلار\n"
        "📥 درآمد ساعتی: 45,000 دلار\n\n"

        "برای خرید:\n"
        "خرید معدن الماس 5\n"
        "خرید معدن طلا 2"
    )


# ============================================================
# منوی موشک
# ============================================================

def missile_menu():

    text = "🚀 لیست تجهیزات هجومی:\n\n"

    for name, data in MISSILES.items():

        price = data[0]

        power = data[1]

        text += (
            f"• {name}\n"
            f"💰 قیمت: {money(price)}$\n"
            f"💥 قدرت: {power}\n\n"
        )

    text += (
        "برای خرید:\n"
        "خرید موشک + نام موشک\n"
        "خرید موشک + نام موشک + تعداد\n\n"

        "مثال:\n"
        "خرید موشک سجیل\n"
        "خرید موشک سجیل 2"
    )

    return text


# ============================================================
# منوی پهپاد
# ============================================================

def drone_menu():
    text = "🛩 لیست تجهیزات هوایی:\n\n"
    for name, (price, power) in DRONES.items():
        text += f"• {name}\n💰 قیمت: {money(price)}$\n💥 قدرت: {power}\n\n"
    text += "برای خرید:\nخرید پهپاد + نام پهپاد\nخرید پهپاد + نام پهپاد + تعداد\n\nمثال:\nخرید پهپاد ابابیل\nخرید پهپاد ابابیل 2"
    return text


# ============================================================
# منوی پدافند
# ============================================================

def defense_menu():

    text = "⚔ لیست تجهیزات دفاعی:\n\n"

    for name, data in DEFENSES.items():

        price = data["price"]

        chance = int(
            data["chance"] * 100
        )

        text += (
            f"• {name}\n"
            f"💰 قیمت: {money(price)}$\n"
            f"🛡 شانس دفع: {chance}٪\n\n"
        )

    text += (
        "برای خرید:\n"
        "خرید پدافند + نام پدافند\n"
        "خرید پدافند + نام پدافند + تعداد\n\n"

        "مثال:\n"
        "خرید پدافند پاتریوت\n"
        "خرید پدافند پاتریوت 2"
    )

    return text
# ============================================================
# خرید معدن
# ============================================================

def buy_mine(
    chat_id,
    user_id,
    text,
    reply_to=None
):

    match = re.match(
        r"^خرید معدن\s+(.+?)(?:\s*\+?\s*(\d+))?$",
        text
    )

    if not match:

        return False

    mine_name = normalize(
        match.group(1)
    )

    quantity_text = match.group(2)

    quantity = int(
        quantity_text or 1
    )

    if mine_name not in MINES:

        send_message(
            chat_id,
            "❌ این معدن وجود ندارد.",
            reply_to=reply_to
        )

        return True

    if quantity <= 0:

        send_message(
            chat_id,
            "❌ تعداد نامعتبر است.",
            reply_to=reply_to
        )

        return True

    country = get_country(
        chat_id,
        user_id
    )

    if not country:

        send_message(
            chat_id,
            "❌ اول کشور خودت را بساز.\n"
            "بنویس: خرید کشور",
            reply_to=reply_to
        )

        return True

    price = (
        MINES[mine_name]["price"]
        * quantity
    )

    balance = get_balance(
        country["id"]
    )

    if balance < price:

        send_message(
            chat_id,
            f"❌ موجودی کافی نیست.\n\n"
            f"💰 قیمت: {money(price)}$\n"
            f"💵 موجودی شما: {money(balance)}$",
            reply_to=reply_to
        )

        return True

    change_balance(
        country["id"],
        -price
    )

    add_quantity(
        "mines",
        country["id"],
        mine_name,
        quantity
    )

    new_income = calculate_hourly_income(
        country["id"]
    )

    send_message(
        chat_id,
        f"✅ خرید معدن انجام شد.\n\n"
        f"⛰ معدن: {mine_name}\n"
        f"📦 تعداد: {quantity}\n"
        f"💸 هزینه: {money(price)}$\n"
        f"💰 موجودی جدید: "
        f"{money(get_balance(country['id']))}$\n"
        f"📥 درآمد ساعتی جدید: "
        f"{money(new_income)}$",
        reply_to=reply_to
    )

    return True


# ============================================================
# پیدا کردن نام آیتم + تعداد
# ============================================================

def find_item(
    text,
    items
):

    text = normalize(text)

    # اول حالت نام دقیق
    for name in items:

        if text == name:

            return name, 1

    # بعد حالت نام + تعداد
    for name in sorted(
        items,
        key=len,
        reverse=True
    ):

        if text.startswith(
            name + " "
        ):

            rest = text[
                len(name):
            ].strip()

            rest = rest.lstrip(
                "+"
            ).strip()

            if rest.isdigit():

                quantity = int(rest)

                if quantity > 0:

                    return (
                        name,
                        quantity
                    )

    return None, None


# ============================================================
# خرید موشک / پدافند
#
# نکته مهم:
# دیگر اسم ساده موشک یا پدافند خرید محسوب نمی‌شود.
#
# موشک:
# خرید موشک سجیل
# خرید موشک سجیل 5
#
# پدافند:
# خرید پدافند پاتریوت
# خرید پدافند پاتریوت 5
# ============================================================

def buy_weapon(
    chat_id,
    user_id,
    text,
    reply_to=None
):

    text = normalize(text)

    # ========================================================
    # موشک
    # فقط با عبارت «خرید موشک»
    # ========================================================

    missile_text = None

    if text.startswith(
        "خرید موشک "
    ):

        missile_text = text[
            len("خرید موشک "):
        ].strip()

    if missile_text:

        missile_name, quantity = find_item(
            missile_text,
            MISSILES
        )

        if not missile_name:

            send_message(
                chat_id,
                "❌ نام موشک یا تعداد موشک نامعتبر است.\n\n"
                "مثال:\n"
                "خرید موشک سجیل\n"
                "خرید موشک سجیل 2",
                reply_to=reply_to
            )

            return True

        country = get_country(
            chat_id,
            user_id
        )

        if not country:

            send_message(
                chat_id,
                "❌ اول کشور خودت را بساز.\n"
                "بنویس: خرید کشور",
                reply_to=reply_to
            )

            return True

        price = MISSILES[
            missile_name
        ][0]

        power = MISSILES[
            missile_name
        ][1]

        total_price = (
            price * quantity
        )

        balance = get_balance(
            country["id"]
        )

        if balance < total_price:

            send_message(
                chat_id,
                f"❌ موجودی کافی نیست.\n\n"
                f"🚀 سلاح: {missile_name}\n"
                f"📦 تعداد: {quantity}\n"
                f"💰 قیمت: {money(total_price)}$\n"
                f"💵 موجودی: {money(balance)}$",
                reply_to=reply_to
            )

            return True

        change_balance(
            country["id"],
            -total_price
        )

        add_quantity(
            "missiles",
            country["id"],
            missile_name,
            quantity
        )

        send_message(
            chat_id,
            f"✅ موشک خریداری شد.\n\n"
            f"🚀 {missile_name} ×{quantity}\n"
            f"💥 قدرت هر موشک: {power}\n"
            f"💸 هزینه: {money(total_price)}$\n"
            f"💰 موجودی: "
            f"{money(get_balance(country['id']))}$",
            reply_to=reply_to
        )

        return True

    # ========================================================
    # پهپاد
    # ========================================================

    drone_text = None
    if text.startswith("خرید پهپاد "):
        drone_text = text[len("خرید پهپاد "):].strip()
    elif text.startswith("خرید پهباد "):
        drone_text = text[len("خرید پهباد "):].strip()

    if drone_text:
        drone_name, quantity = find_item(drone_text, DRONES)
        if not drone_name:
            drone_name, quantity = find_item("پهپاد " + drone_text, DRONES)
        if not drone_name:
            send_message(chat_id, "❌ نام پهپاد یا تعداد پهپاد نامعتبر است.\n\nمثال:\nخرید پهپاد ابابیل\nخرید پهپاد ابابیل 2", reply_to=reply_to)
            return True
        country = get_country(chat_id, user_id)
        if not country:
            send_message(chat_id, "❌ اول کشور خودت را بساز.\nبنویس: خرید کشور", reply_to=reply_to)
            return True
        price, power = DRONES[drone_name]
        total_price = price * quantity
        balance = get_balance(country["id"])
        if balance < total_price:
            send_message(chat_id, f"❌ موجودی کافی نیست.\n\n🛩 پهپاد: {drone_name}\n📦 تعداد: {quantity}\n💰 قیمت: {money(total_price)}$\n💵 موجودی: {money(balance)}$", reply_to=reply_to)
            return True
        change_balance(country["id"], -total_price)
        add_quantity("drones", country["id"], drone_name, quantity)
        send_message(chat_id, f"✅ پهپاد خریداری شد.\n\n🛩 {drone_name} ×{quantity}\n💥 قدرت هر پهپاد: {power}\n💸 هزینه: {money(total_price)}$\n💰 موجودی: {money(get_balance(country['id']))}$", reply_to=reply_to)
        return True

    # ========================================================
    # پدافند
    # فقط با عبارت «خرید پدافند»
    # ========================================================

    defense_text = None

    if text.startswith(
        "خرید پدافند "
    ):

        defense_text = text[
            len("خرید پدافند "):
        ].strip()

    if defense_text:

        defense_name, quantity = find_item(
            defense_text,
            DEFENSES
        )

        if not defense_name:

            send_message(
                chat_id,
                "❌ نام پدافند یا تعداد پدافند نامعتبر است.\n\n"
                "مثال:\n"
                "خرید پدافند پاتریوت\n"
                "خرید پدافند پاتریوت 2",
                reply_to=reply_to
            )

            return True

        country = get_country(
            chat_id,
            user_id
        )

        if not country:

            send_message(
                chat_id,
                "❌ اول کشور خودت را بساز.\n"
                "بنویس: خرید کشور",
                reply_to=reply_to
            )

            return True

        price = DEFENSES[
            defense_name
        ]["price"]

        chance = int(
            DEFENSES[
                defense_name
            ]["chance"] * 100
        )

        total_price = (
            price * quantity
        )

        balance = get_balance(
            country["id"]
        )

        if balance < total_price:

            send_message(
                chat_id,
                f"❌ موجودی کافی نیست.\n\n"
                f"⚔ پدافند: {defense_name}\n"
                f"📦 تعداد: {quantity}\n"
                f"💰 قیمت: {money(total_price)}$\n"
                f"💵 موجودی: {money(balance)}$",
                reply_to=reply_to
            )

            return True

        change_balance(
            country["id"],
            -total_price
        )

        add_quantity(
            "defenses",
            country["id"],
            defense_name,
            quantity
        )

        send_message(
            chat_id,
            f"✅ پدافند خریداری شد.\n\n"
            f"⚔ {defense_name} ×{quantity}\n"
            f"🛡 شانس دفع: {chance}٪\n"
            f"💸 هزینه: {money(total_price)}$\n"
            f"💰 موجودی: "
            f"{money(get_balance(country['id']))}$",
            reply_to=reply_to
        )

        return True

    return False


# ============================================================
# افزایش سلامت
# ============================================================

def health_info(
    chat_id,
    user_id,
    reply_to=None
):

    country = get_country(
        chat_id,
        user_id
    )

    if not country:

        send_message(
            chat_id,
            "❌ اول کشور خودت را بساز.\n"
            "بنویس: خرید کشور",
            reply_to=reply_to
        )

        return

    pending_health.add(
        (
            chat_id,
            user_id
        )
    )

    send_message(
        chat_id,
        f"🩸 افزایش سلامت\n\n"
        f"🩸 سلامت فعلی: "
        f"{money(country['health'])}\n\n"
        f"💰 قیمت هر 1 واحد سلامت: 50 دلار\n\n"
        f"حالا فقط تعداد را بفرست.\n"
        f"مثال:\n"
        f"50",
        reply_to=reply_to
    )


# ============================================================
# خرید سلامت
# ============================================================

def buy_health(
    chat_id,
    user_id,
    text,
    reply_to=None
):

    key = (
        chat_id,
        user_id
    )

    if key not in pending_health:

        return False

    if not text.isdigit():

        send_message(
            chat_id,
            "❌ فقط عدد وارد کن.\n"
            "مثال: 50",
            reply_to=reply_to
        )

        return True

    amount = int(text)

    pending_health.discard(
        key
    )

    if amount <= 0:

        send_message(
            chat_id,
            "❌ مقدار سلامت معتبر نیست.",
            reply_to=reply_to
        )

        return True

    country = get_country(
        chat_id,
        user_id
    )

    if not country:

        return True

    cost = (
        amount * 50
    )

    balance = get_balance(
        country["id"]
    )

    if balance < cost:

        send_message(
            chat_id,
            f"❌ موجودی کافی نیست.\n\n"
            f"🩸 مقدار: {amount}\n"
            f"💰 هزینه: {money(cost)}$\n"
            f"💵 موجودی: {money(balance)}$",
            reply_to=reply_to
        )

        return True

    change_balance(
        country["id"],
        -cost
    )

    new_health = (
        country["health"]
        + amount
    )

    set_health(
        country["id"],
        new_health
    )

    send_message(
        chat_id,
        f"✅ سلامت افزایش یافت.\n\n"
        f"🩸 مقدار خریداری‌شده: "
        f"{money(amount)}\n"
        f"💸 هزینه: {money(cost)}$\n"
        f"🩸 سلامت جدید: "
        f"{money(new_health)}\n"
        f"💰 موجودی: "
        f"{money(get_balance(country['id']))}$",
        reply_to=reply_to
    )

    return True


# ============================================================
# احتمال موفقیت حمله
# ============================================================

def attack_probability(
    attack_power,
    defender_health
):

    if attack_power <= 0:

        return 1

    probability = (
        attack_power
        /
        (
            attack_power
            + max(
                1,
                defender_health
            )
        )
        * 100
    )

    probability = max(
        5,
        probability
    )

    probability = min(
        95,
        probability
    )

    return round(
        probability,
        1
    )


# ============================================================
# دکمه های موشک حمله
# ============================================================

def attack_keyboard(
    country_id
):

    rows = []

    inventory = get_inventory(
        "missiles",
        country_id
    )

    for row in inventory:

        name = row["missile_name"]

        quantity = row["quantity"]

        rows.append(
            [
                {
                    "text":
                        f"🚀 {name} ×{quantity}",
                    "callback_data":
                        "atk:" + name
                }
            ]
        )

    return rows


# ============================================================
# نمایش منوی حمله
# ============================================================

def show_attack_menu(chat_id, user_id, target_user_id, attack_type="missile", reply_to=None):
    attacker = get_country(chat_id, user_id)
    defender = get_country(chat_id, target_user_id)
    if not attacker:
        send_message(chat_id,"❌ شما هنوز کشور ندارید.\nبنویس: خرید کشور",reply_to=reply_to); return
    if not defender:
        send_message(chat_id,"❌ صاحب این پیام کشور ندارد.",reply_to=reply_to); return
    if attacker["id"] == defender["id"]:
        send_message(chat_id,"❌ نمی‌توانی به کشور خودت حمله کنی.",reply_to=reply_to); return
    if defender["health"] <= 0:
        send_message(chat_id,"❌ این کشور قبلاً فتح شده است.",reply_to=reply_to); return
    if attack_type == "drone":
        inventory=get_inventory("drones",attacker["id"]); title="🛩 پهپادهای شما"; label="🛩"; empty="❌ هیچ پهپادی در انبار شما وجود ندارد."
    else:
        inventory=get_inventory("missiles",attacker["id"]); title="🚀 موشک های شما"; label="🚀"; empty="❌ هیچ موشکی در انبار شما وجود ندارد."
    if not inventory:
        send_message(chat_id,empty,reply_to=reply_to); return
    key=(chat_id,user_id)
    pending_attack[key]=target_user_id
    pending_attack_type[key]=attack_type
    text=f"🎯 هدف:\n{defender['country_name']} ({defender['nickname']})\n\n🩸 سلامت هدف:\n{money(defender['health'])}\n\n{title}:\n"
    keyboard=[]
    for row in inventory:
        if attack_type == "drone":
            name,quantity=row["drone_name"],row["quantity"]; power=DRONES[name][1]; callback=f"drone:{user_id}:{name}"
        else:
            name,quantity=row["missile_name"],row["quantity"]; power=MISSILES[name][1]; callback=f"atk:{user_id}:{name}"
        text += f"• {name} ×{quantity} | قدرت {power}\n"
        keyboard.append([{"text":f"{label} {name} ×{quantity}","callback_data":callback}])
    text += "\nبرای حمله با متن بنویس:\nنام تجهیز\nیا\nنام تجهیز + تعداد\n\nیا روی دکمه تجهیز بزن."
    send_message(chat_id,text,reply_to=reply_to,keyboard=keyboard)


# ============================================================
# اجرای واقعی شبیه سازی حمله
# ============================================================

def run_attack_simulation(
    attacker,
    defender,
    missile_name,
    quantity
):

    power = MISSILES[
        missile_name
    ][1]

    intercepted = 0

    hit = 0

    damage = 0

    used_defenses = []

    defense_inventory = get_inventory(
        "defenses",
        defender["id"]
    )

    available_defenses = []

    for row in defense_inventory:

        for _ in range(
            row["quantity"]
        ):

            available_defenses.append(
                {
                    "name":
                        row["defense_name"],

                    "chance":
                        DEFENSES[
                            row["defense_name"]
                        ]["chance"]
                }
            )

    random.shuffle(
        available_defenses
    )

    for _ in range(quantity):

        if available_defenses:

            defense = (
                available_defenses.pop()
            )

            defense_name = (
                defense["name"]
            )

            chance = (
                defense["chance"]
            )

            used_defenses.append(
                defense_name
            )

            success = (
                random.random()
                < chance
            )

            remove_quantity(
                "defenses",
                defender["id"],
                defense_name,
                1
            )

            if success:

                intercepted += 1

            else:

                hit += 1

                damage += power

        else:

            hit += 1

            damage += power

    return {
        "intercepted":
            intercepted,

        "hit":
            hit,

        "damage":
            damage,

        "used_defenses":
            used_defenses
    }


# ============================================================
# اجرای حمله
# ============================================================

def run_drone_attack_simulation(defender, drone_name, quantity):
    power=DRONES[drone_name][1]; intercepted=hit=damage=0; used_defenses=[]; available=[]
    for row in get_inventory("defenses",defender["id"]):
        for _ in range(row["quantity"]):
            available.append({"name":row["defense_name"],"chance":DEFENSES[row["defense_name"]]["chance"]})
    random.shuffle(available)
    for _ in range(quantity):
        if available:
            d=available.pop(); name=d["name"]; used_defenses.append(name); stopped=random.random()<d["chance"]
            remove_quantity("defenses",defender["id"],name,1)
            if stopped: intercepted+=1
            else: hit+=1; damage+=power
        else: hit+=1; damage+=power
    return {"intercepted":intercepted,"hit":hit,"damage":damage,"used_defenses":used_defenses}


def execute_drone_attack(chat_id,user_id,target_user_id,drone_name,quantity,reply_to=None):
    attacker=get_country(chat_id,user_id); defender=get_country(chat_id,target_user_id)
    if not attacker or not defender: send_message(chat_id,"❌ اطلاعات کشور پیدا نشد.",reply_to=reply_to); return
    if attacker["id"]==defender["id"]: send_message(chat_id,"❌ نمی‌توانی به کشور خودت حمله کنی.",reply_to=reply_to); return
    if drone_name not in DRONES or quantity<=0: send_message(chat_id,"❌ اطلاعات پهپاد نامعتبر است.",reply_to=reply_to); return
    if get_quantity("drones",attacker["id"],drone_name)<quantity: send_message(chat_id,"❌ موجودی این پهپاد کافی نیست.",reply_to=reply_to); return
    total_power=DRONES[drone_name][1]*quantity; probability=attack_probability(total_power,defender["health"])
    remove_quantity("drones",attacker["id"],drone_name,quantity)
    result=run_drone_attack_simulation(defender,drone_name,quantity)
    new_health=max(0,defender["health"]-result["damage"]); set_health(defender["id"],new_health)
    defenses_text="\n".join(f"• {x}" for x in result["used_defenses"]) if result["used_defenses"] else "• هیچ پدافندی وجود نداشت."
    text=("🛩 نتیجه حمله پهپادی\n\n" f"🎯 هدف:\n{defender['country_name']} ({defender['nickname']})\n\n" f"🛩 پهپاد:\n{drone_name} ×{quantity}\n\n" f"💥 قدرت کل:\n{money(total_power)}\n\n" f"📊 احتمال موفقیت:\n{probability}٪\n\n" f"🛡 رهگیری شده:\n{result['intercepted']}\n\n" f"🎯 اصابت کرده:\n{result['hit']}\n\n" f"💣 خسارت:\n{money(result['damage'])}\n\n" f"🩸 سلامت باقی مانده:\n{money(new_health)}\n\n" f"⚔ پدافندهای درگیر شده:\n{defenses_text}")
    if new_health<=0:
        add_conquest(attacker["id"],defender["country_name"],defender["nickname"]); record_conquest_for_season(chat_id, user_id, defender["country_name"]); change_balance(attacker["id"],250_000)
        text += ("\n\n🏆🏆🏆 فتح کشور 🏆🏆🏆\n\n" f"🌍 کشور {defender['country_name']} ({defender['nickname']}) فتح شد!\n\n" "💰 پاداش فتح:\n250,000 دلار\n\n" f"💵 موجودی جدید شما:\n{money(get_balance(attacker['id']))}$")
        remove_defeated_country(defender["id"])
        report_attack(
            chat_id, attacker, defender, drone_name, quantity,
            total_power, probability, result["intercepted"],
            result["hit"], result["damage"], is_drone=True
        )
        report_conquest(
            chat_id, attacker, defender, drone_name, quantity,
            is_drone=True
        )
    else:
        report_attack(
            chat_id, attacker, defender, drone_name, quantity,
            total_power, probability, result["intercepted"],
            result["hit"], result["damage"], is_drone=True
        )
    send_message(chat_id,text,reply_to=reply_to)


def execute_attack(
    chat_id,
    user_id,
    target_user_id,
    missile_name,
    quantity,
    reply_to=None
):

    if group_phase(chat_id) != "war":
        send_message(chat_id, "🚫 حمله فقط در زمان جنگ جهانی مجاز است.", reply_to=reply_to)
        return

    attacker = get_country(
        chat_id,
        user_id
    )

    defender = get_country(
        chat_id,
        target_user_id
    )

    if not attacker or not defender:

        send_message(
            chat_id,
            "❌ اطلاعات کشور پیدا نشد.",
            reply_to=reply_to
        )

        return

    if attacker["id"] == defender["id"]:

        send_message(
            chat_id,
            "❌ نمی‌توانی به کشور خودت حمله کنی.",
            reply_to=reply_to
        )

        return

    if missile_name not in MISSILES:

        send_message(
            chat_id,
            "❌ این موشک وجود ندارد.",
            reply_to=reply_to
        )

        return

    if quantity <= 0:

        send_message(
            chat_id,
            "❌ تعداد موشک نامعتبر است.",
            reply_to=reply_to
        )

        return

    available = get_quantity(
        "missiles",
        attacker["id"],
        missile_name
    )

    if available < quantity:

        send_message(
            chat_id,
            "❌ موجودی این سلاح کافی نیست.",
            reply_to=reply_to
        )

        return

    power_each = MISSILES[
        missile_name
    ][1]

    total_power = (
        power_each
        * quantity
    )

    probability = attack_probability(
        total_power,
        defender["health"]
    )

    # موشک ها از انبار مهاجم کم می شوند
    remove_quantity(
        "missiles",
        attacker["id"],
        missile_name,
        quantity
    )

    result = run_attack_simulation(
        attacker,
        defender,
        missile_name,
        quantity
    )

    intercepted = result[
        "intercepted"
    ]

    hit = result[
        "hit"
    ]

    damage = result[
        "damage"
    ]

    new_health = max(
        0,
        defender["health"]
        - damage
    )

    set_health(
        defender["id"],
        new_health
    )

    if result["used_defenses"]:

        defenses_text = "\n".join(
            f"• {name}"
            for name in result[
                "used_defenses"
            ]
        )

    else:

        defenses_text = "• هیچ پدافندی وجود نداشت."

    text = (
        f"🚀 نتیجه حمله موشکی\n\n"

        f"🎯 هدف:\n"
        f"{defender['country_name']}"
        f" ({defender['nickname']})\n\n"

        f"🚀 سلاح:\n"
        f"{missile_name} ×{quantity}\n\n"

        f"💥 قدرت کل:\n"
        f"{money(total_power)}\n\n"

        f"📊 احتمال موفقیت:\n"
        f"{probability}٪\n\n"

        f"🛡 رهگیری شده:\n"
        f"{intercepted}\n\n"

        f"🎯 اصابت کرده:\n"
        f"{hit}\n\n"

        f"💣 خسارت:\n"
        f"{money(damage)}\n\n"

        f"🩸 سلامت باقی مانده:\n"
        f"{money(new_health)}\n\n"

        f"⚔ پدافندهای درگیر شده:\n"
        f"{defenses_text}"
    )

    # -------------------------
    # فتح کشور
    # -------------------------

    if new_health <= 0:

        add_conquest(
            attacker["id"],
            defender["country_name"],
            defender["nickname"]
        )
        record_conquest_for_season(chat_id, user_id, defender["country_name"])

        change_balance(
            attacker["id"],
            250_000
        )

        text += (
            "\n\n"
            "🏆🏆🏆 فتح کشور 🏆🏆🏆\n\n"

            f"🌍 کشور "
            f"{defender['country_name']}"
            f" ({defender['nickname']})"
            f" فتح شد!\n\n"

            f"💰 پاداش فتح:\n"
            f"250,000 دلار\n\n"

            f"💵 موجودی جدید شما:\n"
            f"{money(get_balance(attacker['id']))}$"
        )

        remove_defeated_country(defender["id"])
        report_attack(
            chat_id, attacker, defender, missile_name, quantity,
            total_power, probability, intercepted, hit, damage,
            is_drone=False
        )
        report_conquest(
            chat_id, attacker, defender, missile_name, quantity,
            is_drone=False
        )
    else:
        report_attack(
            chat_id, attacker, defender, missile_name, quantity,
            total_power, probability, intercepted, hit, damage,
            is_drone=False
        )
    send_message(
        chat_id,
        text,
        reply_to=reply_to
    )
# ============================================================
# متن شروع
# ============================================================

def start_text(user):

    name = get_first_name(
        user
    )

    return (
        f"{name} عزیز به بات پیشرفته "
        f"و جذاب جنگ جهانی شایسته ها خوش آمدید\n\n"

        "🎮 این بازی برای گروه طراحی شده است.\n\n"

        "برای شروع:\n"
        "1️⃣ بات را به گروه اضافه کن.\n"
        "2️⃣ بات را ادمین کن.\n"
        "3️⃣ داخل گروه بنویس:\n\n"
        "خرید کشور"
    )


# ============================================================
# راهنما
# ============================================================

def help_text():

    return (
        "📚 راهنمای جنگ جهانی شایسته ها\n\n"

        "🌍 ساخت کشور:\n"
        "خرید کشور\n\n"

        "⚖ مشاهده تجهیزات:\n"
        "لیست تجهیزات کشور\n\n"

        "⛰ خرید معدن:\n"
        "خرید معدن\n"
        "خرید معدن الماس 5\n\n"

        "🚀 خرید موشک:\n"
        "خرید موشک\n"
        "خرید موشک سجیل\n"
        "خرید موشک سجیل 2\n\n"

        "⚔ خرید پدافند:\n"
        "خرید پدافند\n"
        "خرید پدافند پاتریوت\n"
        "خرید پدافند پاتریوت 2\n\n"

        "🩸 افزایش سلامت:\n"
        "افزایش سلامت\n"
        "بعد تعداد را بفرست.\n\n"

        "🎯 حمله:\n"
        "روی پیام بازیکن ریپلای کن و بنویس:\n"
        "حمله ی موشکی\n\n"

        "بعد از آن برای حمله می‌توانی بنویسی:\n"
        "سجیل\n"
        "سجیل 2\n\n"

        "یا روی دکمه موشک بزن."
    )


def callback_owner_id(data):
    parts = data.split(":")
    if not parts:
        return None

    if parts[0] in ("menu", "my") and len(parts) >= 3:
        try:
            return int(parts[1])
        except Exception:
            return None

    if parts[0] in ("country", "nick") and len(parts) >= 3:
        try:
            return int(parts[-1])
        except Exception:
            return None

    if parts[0] in ("atk", "drone") and len(parts) >= 3:
        try:
            return int(parts[1])
        except Exception:
            return None

    return None


# ============================================================
# CALLBACK
# ============================================================

def handle_callback(
    callback
):

    callback_id = (
        callback.get("id")
        or callback.get(
            "callback_query_id"
        )
    )

    data = callback.get(
        "data",
        ""
    )

    message = (
        callback.get("message")
        or {}
    )

    user = (
        callback.get("from")
        or callback.get("user")
        or {}
    )

    chat = message.get(
        "chat",
        {}
    )

    chat_id = chat.get(
        "id"
    )

    message_id = message.get(
        "message_id"
    )

    user_id = user.get(
        "id"
    )

    owner_id = callback_owner_id(data)
    if owner_id is not None and owner_id != user_id:
        if callback_id:
            answer_callback(
                callback_id,
                "این پنل برای شما نیست.",
                show_alert=True
            )
        return

    if callback_id:

        answer_callback(
            callback_id
        )

    if chat_id is None:

        return

    if user_id is None:

        return

    # ========================================================
    # دکمه خرید کشور
    # ========================================================

    if data == "buy_country":
        if group_phase(chat_id) != "country":
            send_message(chat_id, "⏳ زمان انتخاب کشور هنوز نرسیده یا تمام شده است.")
            return
        if get_country(chat_id, user_id):
            send_message(chat_id, "❌ شما قبلاً کشور دارید.")
            return
        keyboard = country_keyboard(chat_id, user_id)
        if not keyboard:
            send_message(chat_id, "😔 همه کشورها گرفته شده‌اند.")
            return
        send_message(chat_id, "🌍 یک کشور انتخاب کن:", keyboard=keyboard)
        return

    # ========================================================
    # انتخاب کشور
    # ========================================================

    if data.startswith(
        "country:"
    ):

        try:

            index = int(data.split(":")[1])

            country_name = (
                COUNTRIES[index]
            )

        except Exception:

            send_message(
                chat_id,
                "❌ کشور نامعتبر است."
            )

            return

        if group_phase(chat_id) != "country":
            send_message(chat_id, "⏳ در حال حاضر زمان انتخاب کشور نیست.")
            return

        existing = get_country(
            chat_id,
            user_id
        )
        if existing:
            send_message(
                chat_id,
                f"❌ شما قبلاً کشور {existing['country_name']} ({existing['nickname']}) را دارید."
            )
            return

        if not reserve_country(chat_id, country_name, user_id):
            send_message(chat_id, "❌ این کشور همین الان توسط بازیکن دیگری انتخاب شده است.")
            edit_message(chat_id, message_id, "🌍 کشور دیگری انتخاب کن:", keyboard=country_keyboard(chat_id, user_id))
            return

        pending_country[
            (
                chat_id,
                user_id
            )
        ] = {
            "country":
                country_name
        }

        edit_message(
            chat_id,
            message_id,
            f"🌍 کشور انتخاب شد:\n"
            f"{country_name}\n\n"
            "حالا لقب کشور را انتخاب کن:",
            keyboard=
                nickname_keyboard(user_id)
        )

        return

    # ========================================================
    # انتخاب لقب
    # ========================================================

    if data.startswith(
        "nick:"
    ):

        state = pending_country.get(
            (
                chat_id,
                user_id
            )
        )

        if not state:

            send_message(
                chat_id,
                "❌ ابتدا خرید کشور را بزن."
            )

            return

        try:

            index = int(data.split(":")[1])

            nickname = (
                NICKNAMES[index]
            )

        except Exception:

            send_message(
                chat_id,
                "❌ لقب نامعتبر است."
            )

            return

        country_name = (
            state["country"]
        )

        ok, reason = create_country(
            chat_id,
            user_id,
            country_name,
            nickname
        )

        pending_country.pop(
            (
                chat_id,
                user_id
            ),
            None
        )

        if reason == "taken":

            send_message(
                chat_id,
                "❌ این اسم و لقب انتخاب شده است، "
                "انتخاب دیگری کنید."
            )

            return

        if reason == "already":

            send_message(
                chat_id,
                "❌ شما قبلاً در این گروه کشور ساخته‌اید."
            )

            return

        if ok:

            send_message(
                chat_id,
                f"✅ کشور شما ساخته شد\n\n"

                f"🌍 کشور: "
                f"{country_name}\n"

                f"⚖ لقب: "
                f"{nickname}\n"

                f"📊 وضعیت: تازه کار\n\n"

                f"💰 موجودی اولیه: "
                f"500,000 دلار\n"

                f"🩸 سلامت اولیه: "
                f"10,000",

                keyboard=[
                    [
                        {
                            "text":
                                "⚖ تجهیزات کشور",
                            "callback_data":
                                f"my:{user_id}:panel"
                        }
                    ],

                    [
                        {
                            "text":
                                "📚 راهنما",
                            "callback_data":
                                f"menu:{user_id}:help"
                        }
                    ]
                ]
            )

        return

    # ========================================================
    # پنل
    # ========================================================

    if data.startswith("my:") and data.split(":")[2] == "panel":

        country = get_country(
            chat_id,
            user_id
        )

        if not country:

            send_message(
                chat_id,
                "❌ شما کشور ندارید."
            )

            return

        send_country_panel(
            chat_id,
            country
        )

        return

    # ========================================================
    # معدن
    # ========================================================

    if data.startswith("menu:") and data.split(":")[2] == "mines":

        send_message(
            chat_id,
            mine_menu(),
            keyboard=[
                [
                    {
                        "text":
                            "⚖ برگشت",
                        "callback_data":
                            f"my:{user_id}:panel"
                    }
                ]
            ]
        )

        return

    # ========================================================
    # موشک
    # ========================================================

    if data.startswith("menu:") and data.split(":")[2] == "missiles":

        send_message(
            chat_id,
            missile_menu(),
            keyboard=[
                [
                    {
                        "text":
                            "⚖ برگشت",
                        "callback_data":
                            f"my:{user_id}:panel"
                    }
                ]
            ]
        )

        return

    # ========================================================
    # پدافند
    # ========================================================

    if data.startswith("menu:") and data.split(":")[2] == "drones":
        country=get_country(chat_id,user_id)
        if not country: send_message(chat_id,"❌ شما کشور ندارید."); return
        rows=get_inventory("drones",country["id"]); text="🛩 تجهیزات هوایی کشور شما:\n\n"; found=False
        for row in rows:
            if row["quantity"]>0:
                found=True; name=row["drone_name"]; text += f"• {name} ×{row['quantity']} | قدرت {DRONES[name][1]}\n"
        if not found: text += "❌ هنوز هیچ پهپادی ندارید.\n"
        send_message(chat_id,text,keyboard=[[{"text":"🛩 خرید پهپاد","callback_data":f"menu:{user_id}:drones_buy"}],[{"text":"⚖ برگشت","callback_data":f"my:{user_id}:panel"}]])
        return

    if data.startswith("menu:") and data.split(":")[2] == "drones_buy":
        send_message(chat_id,drone_menu(),keyboard=[[{"text":"🛩 تجهیزات هوایی من","callback_data":f"menu:{user_id}:drones"}],[{"text":"⚖ برگشت","callback_data":f"my:{user_id}:panel"}]])
        return

    if data.startswith("menu:") and data.split(":")[2] == "defenses":

        send_message(
            chat_id,
            defense_menu(),
            keyboard=[
                [
                    {
                        "text":
                            "⚖ برگشت",
                        "callback_data":
                            f"my:{user_id}:panel"
                    }
                ]
            ]
        )

        return

    # ========================================================
    # سلامت
    # ========================================================

    if data.startswith("menu:") and data.split(":")[2] == "health":

        health_info(
            chat_id,
            user_id
        )

        return

    # ========================================================
    # راهنما
    # ========================================================

    if data.startswith("menu:") and data.split(":")[2] == "help":

        send_message(
            chat_id,
            help_text()
        )

        return

    # ========================================================
    # حمله با دکمه
    # ========================================================

    if data.startswith(
        "atk:"
    ):

        missile_name = ":".join(data.split(":")[2:])

        target_user_id = pending_attack.get(
            (
                chat_id,
                user_id
            )
        )

        if not target_user_id:

            send_message(
                chat_id,
                "❌ ابتدا روی پیام هدف ریپلای کن "
                "و بنویس: حمله ی موشکی"
            )

            return

        attacker = get_country(
            chat_id,
            user_id
        )

        defender = get_country(
            chat_id,
            target_user_id
        )

        if not attacker or not defender:

            send_message(
                chat_id,
                "❌ اطلاعات کشور پیدا نشد."
            )

            return

        if defender["health"] <= 0:

            pending_attack.pop(
                (
                    chat_id,
                    user_id
                ),
                None
            )

            send_message(
                chat_id,
                "❌ این کشور قبلاً فتح شده است."
            )

            return

        if missile_name not in MISSILES:

            send_message(
                chat_id,
                "❌ این موشک وجود ندارد."
            )

            return

        if get_quantity(
            "missiles",
            attacker["id"],
            missile_name
        ) < 1:

            send_message(
                chat_id,
                "❌ موجودی این سلاح کافی نیست."
            )

            return

        pending_attack.pop(
            (
                chat_id,
                user_id
            ),
            None
        )

        power = MISSILES[
            missile_name
        ][1]

        probability = attack_probability(
            power,
            defender["health"]
        )

        send_message(
            chat_id,
            f"🎯 آماده حمله\n\n"
            f"🚀 {missile_name} ×1\n"
            f"💥 قدرت: {power}\n"
            f"📊 احتمال موفقیت: "
            f"{probability}٪\n\n"
            f"⚔ حمله در حال اجرا..."
        )

        execute_attack(
            chat_id,
            user_id,
            target_user_id,
            missile_name,
            1
        )

        return


    if data.startswith("drone:"):
        drone_name=":".join(data.split(":")[2:])
        key=(chat_id,user_id); target_user_id=pending_attack.get(key)
        if not target_user_id or pending_attack_type.get(key)!="drone":
            send_message(chat_id,"❌ ابتدا روی پیام هدف ریپلای کن و حمله پهپادی را شروع کن."); return
        attacker=get_country(chat_id,user_id); defender=get_country(chat_id,target_user_id)
        if not attacker or not defender:
            pending_attack.pop(key,None); pending_attack_type.pop(key,None); send_message(chat_id,"❌ اطلاعات کشور پیدا نشد."); return
        if defender["health"]<=0:
            pending_attack.pop(key,None); pending_attack_type.pop(key,None); send_message(chat_id,"❌ این کشور قبلاً فتح شده است."); return
        if drone_name not in DRONES:
            send_message(chat_id,"❌ این پهپاد وجود ندارد."); return
        if get_quantity("drones",attacker["id"],drone_name)<1:
            send_message(chat_id,"❌ موجودی این پهپاد کافی نیست."); return
        pending_attack.pop(key,None); pending_attack_type.pop(key,None)
        power=DRONES[drone_name][1]; probability=attack_probability(power,defender["health"])
        send_message(chat_id,f"🎯 آماده حمله\n\n🛩 پهپاد: {drone_name} ×1\n💥 قدرت: {power}\n📊 احتمال موفقیت: {probability}٪\n\n⚔ حمله در حال اجرا...")
        execute_drone_attack(chat_id,user_id,target_user_id,drone_name,1)
        return
# ============================================================
# پیام ها
# ============================================================

def handle_message(
    message
):

    text = message.get(
        "text"
    )

    if text is None:

        return

    chat = message.get(
        "chat",
        {}
    )

    chat_id = chat.get(
        "id"
    )

    user = get_user(
        message
    )

    user_id = user.get(
        "id"
    )

    message_id = message.get(
        "message_id"
    )

    if chat_id is None:

        return

    if user_id is None:

        return

    text = normalize(
        text
    )

    # ========================================================
    # START
    # ========================================================

    if text.lower() in (
        "/start",
        "start"
    ):

        send_message(
            chat_id,
            start_text(user),
            reply_to=message_id
        )

        return

    # ========================================================
    # فقط گروه
    # ========================================================

    if not is_group(message):

        send_message(
            chat_id,
            "❌ بازی جنگ جهانی شایسته ها "
            "فقط داخل گروه قابل استفاده است.",
            reply_to=message_id
        )

        return

    # ========================================================
    # حمله
    # ========================================================

    if text in (
        "حمله ی موشکی", "حمله موشکی", "حمله‌ی موشکی",
        "حمله ی پهپادی", "حمله پهپادی", "حمله‌ی پهپادی",
        "حمله با پهپاد", "حمله با پهباد", "حمله پهبادی", "حمله مهبادی", "حمله با مهباد"
    ):
        if group_phase(chat_id) != "war":
            phase = group_phase(chat_id)
            if phase == "prep":
                msg = "🛡️ دوره ۲۴ ساعته قدرت‌سازی فعال است.\n🚫 هیچ حمله‌ای تا پایان این زمان مجاز نیست."
            elif phase == "country":
                msg = "🌍 هنوز مرحله کشورگیری است.\n⚔️ جنگ جهانی بعد از دوره ۲۴ ساعته قدرت‌سازی آغاز می‌شود."
            else:
                msg = "⏳ هنوز زمان جنگ جهانی نرسیده است."
            send_message(chat_id, msg, reply_to=message_id)
            return
        attack_type = "drone" if ("پهپاد" in text or "پهباد" in text) else "missile"

        reply = (
            message.get(
                "reply_to_message"
            )
            or
            message.get(
                "replyToMessage"
            )
        )

        if not reply:

            send_message(
                chat_id,
                "❌ برای حمله باید به پیام "
                "صاحب کشور موردنظر ریپلای کنی.",
                reply_to=message_id
            )

            return

        target_user = get_user(
            reply
        )

        target_user_id = target_user.get(
            "id"
        )

        if not target_user_id:

            send_message(
                chat_id,
                "❌ صاحب پیام هدف پیدا نشد.",
                reply_to=message_id
            )

            return

        show_attack_menu(
            chat_id,
            user_id,
            target_user_id,
            attack_type=attack_type,
            reply_to=message_id
        )

        return

    # ========================================================
    # لیست تجهیزات
    # ========================================================

    if text == "لیست تجهیزات کشور":

        country = get_country(
            chat_id,
            user_id
        )

        if not country:

            send_message(
                chat_id,
                "❌ هنوز کشوری نداری.\n"
                "بنویس: خرید کشور",
                reply_to=message_id
            )

            return

        send_country_panel(
            chat_id,
            country,
            reply_to=message_id
        )

        return

    # ========================================================
    # لیست تجهیزات با نام کشور
    # ========================================================

    if text.startswith(
        "لیست تجهیزات کشور "
    ):

        requested = text[
            len("لیست تجهیزات کشور "):
        ].strip()

        my_country = get_country(
            chat_id,
            user_id
        )

        if my_country:

            my_name = (
                f"{my_country['country_name']} "
                f"{my_country['nickname']}"
            )

            if requested == my_name:

                send_country_panel(
                    chat_id,
                    my_country,
                    reply_to=message_id
                )

                return

        parts = requested.rsplit(
            " ",
            1
        )

        if len(parts) == 2:

            found = get_country_by_name(
                chat_id,
                parts[0],
                parts[1]
            )

            if found:

                send_message(
                    chat_id,
                    "❌ این پنل برای شما نیست.",
                    reply_to=message_id
                )

                return

        send_message(
            chat_id,
            "❌ کشور با این نام و لقب پیدا نشد.",
            reply_to=message_id
        )

        return

    # ========================================================
    # منوی معدن
    # ========================================================

    if text == "خرید معدن":

        send_message(
            chat_id,
            mine_menu(),
            reply_to=message_id
        )

        return

    # ========================================================
    # منوی موشک
    # ========================================================

    if text == "خرید موشک":

        send_message(
            chat_id,
            missile_menu(),
            reply_to=message_id
        )

        return

    # ========================================================
    # منوی پدافند
    # ========================================================

    if text in (
        "خرید پدافند",
        "خرید دفاع"
    ):

        send_message(
            chat_id,
            defense_menu(),
            reply_to=message_id
        )

        return

    # ========================================================
    # سلامت
    # ========================================================

    if text == "افزایش سلامت":

        health_info(
            chat_id,
            user_id,
            reply_to=message_id
        )

        return

    # ========================================================
    # خرید سلامت
    # ========================================================

    if buy_health(
        chat_id,
        user_id,
        text,
        reply_to=message_id
    ):

        return

    # ========================================================
    # خرید معدن
    # ========================================================

    if buy_mine(
        chat_id,
        user_id,
        text,
        reply_to=message_id
    ):

        return

    # ========================================================
    # انتخاب تجهیز برای حمله
    # ========================================================

    key=(chat_id,user_id)
    if key in pending_attack:
        target_user_id=pending_attack[key]
        attack_type=pending_attack_type.get(key,"missile")

        if attack_type == "drone":
            weapon_name,quantity=find_item(text,DRONES)
            if not weapon_name:
                weapon_name,quantity=find_item("پهپاد " + text,DRONES)
            if weapon_name:
                attacker=get_country(chat_id,user_id); defender=get_country(chat_id,target_user_id)
                if not attacker or not defender:
                    pending_attack.pop(key,None); pending_attack_type.pop(key,None); send_message(chat_id,"❌ اطلاعات کشور پیدا نشد.",reply_to=message_id); return
                if defender["health"]<=0:
                    pending_attack.pop(key,None); pending_attack_type.pop(key,None); send_message(chat_id,"❌ این کشور قبلاً فتح شده است.",reply_to=message_id); return
                available=get_quantity("drones",attacker["id"],weapon_name)
                if available<quantity:
                    send_message(chat_id,f"❌ موجودی این پهپاد کافی نیست.\n\n🛩 پهپاد: {weapon_name}\n📦 تعداد درخواستی: {quantity}\n📦 موجودی شما: {available}",reply_to=message_id); return
                pending_attack.pop(key,None); pending_attack_type.pop(key,None)
                power=DRONES[weapon_name][1]*quantity; probability=attack_probability(power,defender["health"])
                send_message(chat_id,f"🎯 آماده حمله\n\n🛩 پهپاد: {weapon_name} ×{quantity}\n💥 قدرت کل: {money(power)}\n📊 احتمال موفقیت: {probability}٪\n\n⚔ حمله در حال اجرا...",reply_to=message_id)
                execute_drone_attack(chat_id,user_id,target_user_id,weapon_name,quantity,reply_to=message_id); return
            send_message(chat_id,"🛩 شما در حالت حمله پهپادی هستید.\n\nنام پهپاد را وارد کن.\nمثال:\nپهپاد ابابیل\nپهپاد ابابیل 2",reply_to=message_id); return

        missile_name,quantity=find_item(text,MISSILES)
        if missile_name:
            attacker=get_country(chat_id,user_id); defender=get_country(chat_id,target_user_id)
            if not attacker or not defender:
                pending_attack.pop(key,None); pending_attack_type.pop(key,None); send_message(chat_id,"❌ اطلاعات کشور پیدا نشد.",reply_to=message_id); return
            if defender["health"]<=0:
                pending_attack.pop(key,None); pending_attack_type.pop(key,None); send_message(chat_id,"❌ این کشور قبلاً فتح شده است.",reply_to=message_id); return
            available=get_quantity("missiles",attacker["id"],missile_name)
            if available<quantity:
                send_message(chat_id,f"❌ موجودی این موشک کافی نیست.\n\n🚀 موشک: {missile_name}\n📦 تعداد درخواستی: {quantity}\n📦 موجودی شما: {available}",reply_to=message_id); return
            pending_attack.pop(key,None); pending_attack_type.pop(key,None)
            power=MISSILES[missile_name][1]*quantity; probability=attack_probability(power,defender["health"])
            send_message(chat_id,f"🎯 آماده حمله\n\n🚀 سلاح: {missile_name} ×{quantity}\n💥 قدرت کل: {money(power)}\n📊 احتمال موفقیت: {probability}٪\n\n⚔ حمله در حال اجرا...",reply_to=message_id)
            execute_attack(chat_id,user_id,target_user_id,missile_name,quantity,reply_to=message_id); return

        send_message(chat_id,"🎯 شما در حالت حمله هستید.\n\nنام تجهیز را وارد کن.\nمثال برای موشک: سجیل 2\nمثال برای پهپاد: پهپاد ابابیل 2",reply_to=message_id); return

    # ========================================================
    # خرید موشک / پدافند
    #
    # این قسمت بعد از pending_attack قرار گرفته.
    #
    # بنابراین:
    #
    # سجیل
    # سجیل 2
    #
    # دیگر خرید نمی‌کنند.
    #
    # فقط:
    #
    # خرید موشک سجیل
    # خرید موشک سجیل 2
    #
    # خرید انجام می‌دهد.
    # ========================================================

    if buy_weapon(
        chat_id,
        user_id,
        text,
        reply_to=message_id
    ):

        return

    # ========================================================
    # راهنما
    # ========================================================

    if text in (
        "راهنما",
        "کمک"
    ):

        send_message(
            chat_id,
            help_text(),
            reply_to=message_id
        )

        return


# ============================================================
# گرفتن Updates
# ============================================================

def get_updates(
    offset=None
):

    data = {
        "limit": 100,
        "timeout": 30
    }

    if offset is not None:

        data["offset"] = offset

    result = api(
        "getUpdates",
        data
    )

    if not result:

        return []

    if isinstance(
        result,
        dict
    ):

        if "result" in result:

            return result[
                "result"
            ]

        if "updates" in result:

            return result[
                "updates"
            ]

    if isinstance(
        result,
        list
    ):

        return result

    return []


# ============================================================
# پردازش Update
# ============================================================

def process_update(
    update
):

    try:

        callback = (
            update.get(
                "callback_query"
            )
            or
            update.get(
                "callbackQuery"
            )
        )

        if callback:

            handle_callback(
                callback
            )

            return

        message = update.get(
            "message"
        )

        if message:
            new_members = message.get("new_chat_members") or message.get("newChatMembers") or []
            if new_members and BOT_ID is not None:
                for member in new_members:
                    if member.get("id") == BOT_ID:
                        if handle_bot_added(message):
                            return
            handle_message(
                message
            )

            return

        if update.get(
            "text"
        ) is not None:

            handle_message(
                update
            )

    except Exception as error:

        print(
            "[HANDLER ERROR]",
            repr(error)
        )


# ============================================================
# MAIN
# ============================================================

def main():

    if TOKEN == "TOKEN_BOT_را_اینجا_بگذار":

        print(
            "❌ اول TOKEN ربات را داخل main.py وارد کن."
        )

        return

    create_tables()
    migrate_country_schema()

    cleanup_defeated_countries()
    get_bot_id()

    # ========================================================
    # راه اندازی سرور HTTP برای بیدار نگه داشتن Koyeb
    # ========================================================

    web_thread = threading.Thread(
        target=run_web,
        daemon=True
    )

    web_thread.start()

    print(
        "======================================"
    )

    print(
        "🌍 جنگ جهانی شایسته ها"
    )

    print(
        "🤖 Bale Direct API"
    )

    print(
        "🗄 Database:",
        DATABASE_NAME
    )

    print(
        "🌐 Web server started"
    )

    print(
        "======================================"
    )

    offset = None

    while True:

        try:

            process_group_timers()
            updates = get_updates(
                offset
            )

            for update in updates:

                update_id = update.get(
                    "update_id"
                )

                if update_id is not None:

                    offset = (
                        update_id + 1
                    )

                process_update(
                    update
                )

        except KeyboardInterrupt:

            print(
                "\n⛔ ربات متوقف شد."
            )

            break

        except Exception as error:

            print(
                "[MAIN ERROR]",
                repr(error)
            )

            time.sleep(
                2
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
