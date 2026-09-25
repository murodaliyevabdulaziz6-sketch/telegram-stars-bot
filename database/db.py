import aiosqlite
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from config import DB_PATH, REQUIRED_CHANNELS

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)

    async def get_connection(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        return conn

    async def init_db(self):
        """Initialize database schema and seed default items."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    balance_stars INTEGER DEFAULT 0,
                    total_spent INTEGER DEFAULT 0,
                    total_donated INTEGER DEFAULT 0,
                    bonus_points INTEGER DEFAULT 0,
                    vip_level TEXT DEFAULT 'Oddiy',
                    vip_until TIMESTAMP,
                    lang TEXT DEFAULT 'uz',
                    referrer_id INTEGER,
                    daily_streak INTEGER DEFAULT 0,
                    last_daily_bonus TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                );
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price_stars INTEGER NOT NULL,
                    category TEXT DEFAULT 'digital',
                    content TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1
                );
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    charge_id TEXT,
                    amount INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT NOT NULL UNIQUE,
                    title TEXT,
                    invite_link TEXT,
                    is_active INTEGER DEFAULT 1
                );
            """)

            await db.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES ('referral_reward_stars', '1');"
            )

            await db.commit()

            # Seed channels from config if any
            for ch in REQUIRED_CHANNELS:
                link = f"https://t.me/{ch.lstrip('@')}" if ch.startswith("@") else ch
                await db.execute(
                    "INSERT OR IGNORE INTO channels (channel_id, title, invite_link) VALUES (?, ?, ?);",
                    (ch, ch, link)
                )
            await db.commit()

            # Check if default products exist
            cursor = await db.execute("SELECT COUNT(*) FROM products;")
            row = await cursor.fetchone()
            if row and row[0] == 0:
                default_products = [
                    (
                        "👑 VIP Pro Status (1 oy)",
                        "Botdagi barcha VIP funksiyalar, xizmatlarga 20% chegirma va yopiq guruhga taklifnoma.",
                        50,
                        "vip",
                        "Tabriklaymiz! Sizning VIP Pro maqomingiz 1 oyga faollashtirildi.\nMaxsus havola: https://t.me/+vip_sample_link\nQo'llab-quvvatlash uchun: @admin_username"
                    ),
                    (
                        "💎 VIP Ultra Status (3 oy)",
                        "Cheksiz imtiyozlar, shaxsiy menejer va qo'shimcha imtiyozlar!",
                        120,
                        "vip",
                        "Tabriklaymiz! VIP Ultra maqomingiz 3 oyga faollashtirildi.\nBarcha funksiyalar cheklovsiz ochildi!"
                    ),
                    (
                        "🚀 Telegram Stars & Bot Yaratish Qo'llanmasi",
                        "Aiogram 3 va Telegram Stars to'lov tizimini 0 dan professional darajada ulash bo'yicha video darsliklar to'plami.",
                        75,
                        "course",
                        "📚 Darslik materiali va GitHub kodi havolasi:\nhttps://github.com/example/telegram-stars-guide\nParol: STARS_VIP_2026"
                    ),
                    (
                        "🔐 Yopiq Kanalga Doimiy A'zolik",
                        "Eksklyuziv yangiliklar, signallar va foydali insaydlar berib boriladigan yopiq kanal.",
                        30,
                        "channel",
                        "🔐 Yopiq kanalga kirish bir martalik havolasi:\nhttps://t.me/+private_community_join_link"
                    ),
                    (
                        "🎟 Omadli Chipta (Lotereya)",
                        "Telegram Stars o'yinida ishtirok etish chiptasi. 1 oylik Telegram Premium yoki 100 Stars yutib olish imkoniyati!",
                        15,
                        "lottery",
                        "🎟 Chipta raqamingiz: #STARS-" + datetime.now().strftime("%d%H%M") + "\nNatijalar har yakshanba e'lon qilinadi!"
                    )
                ]
                await db.executemany(
                    "INSERT INTO products (title, description, price_stars, category, content) VALUES (?, ?, ?, ?, ?);",
                    default_products
                )
                await db.commit()

    # Settings Methods
    async def get_setting(self, key: str, default: Any = None) -> Any:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT value FROM settings WHERE key = ?;", (key,))
            row = await cursor.fetchone()
            return row[0] if row else default

    async def set_setting(self, key: str, value: Any):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?);", (key, str(value)))
            await db.commit()

    async def get_referral_reward(self) -> int:
        val = await self.get_setting("referral_reward_stars", "1")
        try:
            return max(1, int(val))
        except Exception:
            return 1

    async def set_referral_reward(self, amount: int):
        await self.set_setting("referral_reward_stars", str(max(1, amount)))

    # User Methods
    async def get_or_create_user(self, user_id: int, username: Optional[str] = None, full_name: Optional[str] = None, referrer_id: Optional[int] = None) -> tuple[Dict[str, Any], bool, int]:
        """
        Returns: (user_dict, is_new_user, referral_reward_given)
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,))
            user = await cursor.fetchone()
            is_new = False
            reward_given = 0
            if not user:
                is_new = True
                valid_ref = referrer_id if referrer_id and referrer_id != user_id else None
                await db.execute(
                    """
                    INSERT INTO users (user_id, username, full_name, referrer_id, created_at)
                    VALUES (?, ?, ?, ?, ?);
                    """,
                    (user_id, username or "", full_name or "", valid_ref, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                await db.commit()

                # Reward referrer directly with Stars
                if valid_ref:
                    reward_cursor = await db.execute("SELECT value FROM settings WHERE key = 'referral_reward_stars';")
                    reward_row = await reward_cursor.fetchone()
                    try:
                        reward_amount = int(reward_row[0]) if reward_row and reward_row[0].isdigit() else 1
                    except Exception:
                        reward_amount = 1
                    
                    reward_given = reward_amount

                    await db.execute(
                        "UPDATE users SET balance_stars = balance_stars + ? WHERE user_id = ?;",
                        (reward_amount, valid_ref)
                    )
                    await db.execute(
                        """
                        INSERT INTO transactions (user_id, charge_id, amount, type, description, created_at)
                        VALUES (?, ?, ?, 'referral_reward', ?, ?);
                        """,
                        (valid_ref, f"ref_{user_id}", reward_amount, f"Referal taklifi bonusi (+{reward_amount} ⭐)", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                    await db.commit()

                cursor = await db.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,))
                user = await cursor.fetchone()
            else:
                await db.execute(
                    "UPDATE users SET username = ?, full_name = ? WHERE user_id = ?;",
                    (username or user["username"], full_name or user["full_name"], user_id)
                )
                await db.commit()

            return dict(user), is_new, reward_given

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,))
            user = await cursor.fetchone()
            return dict(user) if user else None

    async def set_user_lang(self, user_id: int, lang: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE users SET lang = ? WHERE user_id = ?;", (lang, user_id))
            await db.commit()

    async def add_spent_stars(self, user_id: int, amount: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET total_spent = total_spent + ? WHERE user_id = ?;",
                (amount, user_id)
            )
            await db.commit()

    async def add_donated_stars(self, user_id: int, amount: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET total_donated = total_donated + ?, total_spent = total_spent + ? WHERE user_id = ?;",
                (amount, amount, user_id)
            )
            await db.commit()

    async def set_user_vip(self, user_id: int, vip_level: str, days: int = 30):
        vip_until = datetime.now() + timedelta(days=days)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET vip_level = ?, vip_until = ? WHERE user_id = ?;",
                (vip_level, vip_until.strftime("%Y-%m-%d %H:%M:%S"), user_id)
            )
            await db.commit()

    async def get_referrals_count(self, user_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM users WHERE referrer_id = ?;", (user_id,))
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def get_referral_users(self, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT user_id, username, full_name, created_at FROM users WHERE referrer_id = ? ORDER BY user_id DESC LIMIT ?;",
                (user_id, limit)
            )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def get_all_users_detailed(self) -> List[Dict[str, Any]]:
        """Fetch all users sorted by date with their referral count."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            query = """
                SELECT 
                    u.user_id,
                    u.username,
                    u.full_name,
                    u.balance_stars,
                    u.total_spent,
                    u.total_donated,
                    u.referrer_id,
                    u.vip_level,
                    u.lang,
                    u.created_at,
                    (SELECT COUNT(*) FROM users r WHERE r.referrer_id = u.user_id) AS referrals_count
                FROM users u
                ORDER BY u.created_at DESC;
            """
            cursor = await db.execute(query)
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def get_users_paginated(self, page: int = 1, page_size: int = 8) -> tuple[List[Dict[str, Any]], int, int]:
        """
        Returns: (users_list, total_users_count, total_pages)
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            count_cursor = await db.execute("SELECT COUNT(*) FROM users;")
            total_count = (await count_cursor.fetchone())[0]

            total_pages = max(1, (total_count + page_size - 1) // page_size)
            page = max(1, min(page, total_pages))
            offset = (page - 1) * page_size

            query = """
                SELECT 
                    u.user_id,
                    u.username,
                    u.full_name,
                    u.balance_stars,
                    u.total_spent,
                    u.total_donated,
                    u.referrer_id,
                    u.vip_level,
                    u.lang,
                    u.created_at,
                    (SELECT COUNT(*) FROM users r WHERE r.referrer_id = u.user_id) AS referrals_count
                FROM users u
                ORDER BY u.created_at DESC
                LIMIT ? OFFSET ?;
            """
            cursor = await db.execute(query, (page_size, offset))
            rows = await cursor.fetchall()
            return [dict(r) for r in rows], total_count, total_pages

    async def get_top_referrers(self, limit: int = 10) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            query = """
                SELECT 
                    u.user_id,
                    u.username,
                    u.full_name,
                    u.balance_stars,
                    (SELECT COUNT(*) FROM users r WHERE r.referrer_id = u.user_id) AS referrals_count
                FROM users u
                WHERE u.balance_stars > 0 OR (SELECT COUNT(*) FROM users r WHERE r.referrer_id = u.user_id) > 0
                ORDER BY u.balance_stars DESC, referrals_count DESC
                LIMIT ?;
            """
            cursor = await db.execute(query, (limit,))
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    # Mandatory Channels Methods
    async def get_active_channels(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM channels WHERE is_active = 1;")
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def add_channel(self, channel_id: str, title: str = "", invite_link: str = "") -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                link = invite_link or (f"https://t.me/{channel_id.lstrip('@')}" if channel_id.startswith("@") else channel_id)
                await db.execute(
                    "INSERT INTO channels (channel_id, title, invite_link, is_active) VALUES (?, ?, ?, 1);",
                    (channel_id, title or channel_id, link)
                )
                await db.commit()
                return True
            except Exception:
                return False

    async def delete_channel(self, channel_id: str) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM channels WHERE channel_id = ?;", (channel_id,))
            await db.commit()
            return True

    # Transaction Methods
    async def add_transaction(self, user_id: int, charge_id: str, amount: int, tx_type: str, description: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO transactions (user_id, charge_id, amount, type, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (user_id, charge_id, amount, tx_type, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            await db.commit()

    async def get_user_transactions(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM transactions WHERE user_id = ? ORDER BY id DESC LIMIT ?;",
                (user_id, limit)
            )
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    # Product Methods
    async def get_products(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM products WHERE is_active = 1 ORDER BY price_stars ASC;")
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM products WHERE id = ? AND is_active = 1;", (product_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    # Admin Statistics
    async def get_admin_stats(self) -> Dict[str, Any]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM users;")
            total_users = (await cursor.fetchone())[0]

            cursor = await db.execute("SELECT SUM(total_spent) FROM users;")
            total_stars_spent = (await cursor.fetchone())[0] or 0

            cursor = await db.execute("SELECT COUNT(*) FROM transactions;")
            total_txs = (await cursor.fetchone())[0]

            cursor = await db.execute("SELECT COUNT(*) FROM users WHERE vip_level != 'Oddiy';")
            vip_users = (await cursor.fetchone())[0]

            cursor = await db.execute("SELECT COUNT(*) FROM channels WHERE is_active = 1;")
            channel_count = (await cursor.fetchone())[0]

            ref_reward = await self.get_referral_reward()

            return {
                "total_users": total_users,
                "total_stars": total_stars_spent,
                "total_txs": total_txs,
                "vip_users": vip_users,
                "channel_count": channel_count,
                "ref_reward": ref_reward
            }

    async def get_all_user_ids(self) -> List[int]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT user_id FROM users;")
            rows = await cursor.fetchall()
            return [r[0] for r in rows]


db = Database()
