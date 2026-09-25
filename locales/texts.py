TEXTS = {
    "uz": {
        "bot_bio": "⭐ Do'stlarni taklif qilib Telegram Stars ishlang! Rasmiy Stars boti.",
        "bot_description": (
            "🌟 <b>Telegram Stars Ishlash Botiga xush kelibsiz!</b>\n\n"
            "Bu bot orqali siz do'stlaringizni taklif qilib, har bir do'stingiz uchun Telegram Stars ishlashingiz mumkin! 💫\n\n"
            "Boshlash uchun 'Start' tugmasini bosing 👇"
        ),
        "welcome": (
            "🌟 <b>Assalomu alaykum, {name}!</b>\n\n"
            "<b>Telegram Stars</b> botiga xush kelibsiz! 🚀\n\n"
            "💎 <b>Sizning balansingiz:</b> <code>{balance}</code> ⭐ Stars\n\n"
            "Stars ishlash uchun quyidagi <b>«⭐ Stars ishlash»</b> tugmasini bosing 👇"
        ),
        "btn_referral": "⭐ Stars ishlash",
        "btn_profile": "👤 Profil & Hamyon",
        "btn_leaderboard": "🏆 Reyting",
        "btn_language": "🌐 Tilni o'zgartirish",
        "btn_help": "ℹ️ Yordam",
        "btn_admin": "🛠 Admin Panel",
        "btn_back": "⬅️ Orqaga",
        
        # Mandatory Subscription
        "must_subscribe": (
            "⚠️ <b>Botdan foydalanish uchun rasmiy kanalimizga a'zo bo'ling!</b>\n\n"
            "Kanalga a'zo bo'lgach, <b>«✅ Tasdiqlash / Tekshirish»</b> tugmasini bosing:"
        ),
        "btn_channel_link": "📢 Kanalga a'zo bo'lish",
        "btn_check_sub": "✅ Tasdiqlash / Tekshirish",
        "sub_not_completed": "❌ Siz hali barcha majburiy kanallarga a'zo bo'lmadingiz! Iltimos, a'zo bo'lib qayta tekshiring.",
        "sub_success": "✅ <b>Obuna muvaffaqiyatli tasdiqlandi!</b> Botdan foydalanishingiz mumkin.",

        # Referral System (Stars Ishlash)
        "referral_title": (
            "⭐ <b>Stars Ishlash & Do'stlarni Taklif Qilish</b>\n\n"
            "Har bir taklif qilgan do'stingiz uchun sizga <b>+{reward} ⭐ Stars</b> beriladi! 🌟\n\n"
            "📊 <b>Siz taklif qilgan do'stlar:</b> <code>{ref_count}</code> ta\n"
            "💎 <b>Sizning balansingiz:</b> <code>{balance}</code> ⭐ Stars\n\n"
            "🔗 <b>Sizning taklif havolangiz:</b>\n"
            "<code>{ref_link}</code>\n\n"
            "<i>Ushbu havolani do'stlaringiz va guruhlarga yuboring!</i>"
        ),
        "btn_share_ref": "🚀 Do'stlarga ulashish",
        "share_text": "🌟 Do'stlarni taklif qilib Telegram Stars ishlang! Botga kiring: 👇",
        "new_referral_notify": "🎉 <b>Yangi do'stingiz qo'shildi!</b>\nSizga taklifnoma uchun <b>+{reward} ⭐ Stars</b> balansingizga qo'shildi! 🌟",

        # Profile
        "profile_text": (
            "👤 <b>Sizning Profilingiz</b>\n\n"
            "🆔 <b>Telegram ID:</b> <code>{user_id}</code>\n"
            "👤 <b>Ism:</b> {name}\n"
            "💎 <b>Stars Balansi:</b> <code>{balance}</code> ⭐ Stars\n"
            "👥 <b>Taklif qilingan do'stlar:</b> <code>{ref_count}</code> ta\n"
            "📅 <b>Ro'yxatdan o'tgan sana:</b> {created_at}\n\n"
            "🔗 <b>Sizning taklif havolangiz:</b>\n"
            "<code>{ref_link}</code>"
        ),
        "btn_my_history": "📜 Tranzaksiyalar tarixi",
        "no_history": "ℹ️ Sizda hali hech qanday Stars tranzaksiyalari mavjud emas.",
        "history_title": "📜 <b>Tranzaksiyalar Tarixi:</b>\n\n{history}",

        # Leaderboard
        "leaderboard_title": (
            "🏆 <b>Eng Ko'p Stars Ishlaganlar Reytingi</b>\n\n"
            "Eng ko'p do'st taklif qilib Stars ishlagan faol foydalanuvchilar:\n\n"
            "{leaderboard}\n\n"
            "<i>Siz ham do'stlaringizni taklif qilib Top 10 talikka kiring! ⭐</i>"
        ),
        "no_donors": "Hozircha reyting shakllanmagan. Birinchi bo'lib do'stlaringizni taklif qiling!",

        # Language
        "lang_select": "🌐 <b>Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please select language:</b>",
        "lang_changed": "✅ <b>Til muvaffaqiyatli o'zgartirildi!</b>",

        # Help
        "help_text": (
            "ℹ️ <b>Bot haqida ma'lumot va Telegram Stars ishlash</b>\n\n"
            "🌟 <b>Telegram Stars nima?</b>\n"
            "Telegram Stars — bu Telegram ichidagi rasmiy raqamli valyuta.\n\n"
            "⭐ <b>Stars ishlash qanday amalga oshiriladi?</b>\n"
            "1. «⭐ Stars ishlash» bo'limiga kiring.\n"
            "2. O'zingizning maxsus havolangizni do'stlaringizga yuboring.\n"
            "3. Do'stingiz botga kirishi bilan sizning balansingizga Stars qo'shiladi!\n\n"
            "📞 <b>Qo'llab-quvvatlash:</b> Savollaringiz bo'lsa adminga murojaat qiling."
        ),

        # Admin
        "admin_title": (
            "🛠 <b>Admin Boshqaruv Paneli</b>\n\n"
            "👥 <b>Jami foydalanuvchilar:</b> <code>{total_users}</code> ta\n"
            "⭐️ <b>Referal mukofoti:</b> <code>{ref_reward}</code> ⭐ Stars\n"
            "📦 <b>Jami tranzaksiyalar:</b> <code>{total_txs}</code> ta\n"
            "📢 <b>Majburiy kanallar:</b> <code>{channel_count}</code> ta"
        ),
        "btn_admin_stats": "📊 Statistika",
        "btn_users_list": "👥 Foydalanuvchilar",
        "btn_export_excel": "📥 Excel (.xlsx) yuklab olish",
        "btn_set_ref_reward": "⚙️ Referal narxi ({reward} ⭐)",
        "btn_broadcast": "📢 Xabar tarqatish",
        "btn_manage_channels": "📢 Majburiy kanallar",
        "broadcast_prompt": "✍️ Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing (matn, rasm yoki video):",
        "broadcast_started": "🚀 Xabar tarqatish boshlandi...",
        "broadcast_finished": "✅ Xabar yuborish yakunlandi!\n\n📊 Yuborildi: {success} ta foydalanuvchiga\n❌ Xatolik: {failed} ta",
        
        "prompt_set_ref_reward": "✍️ 1 ta referal taklif qilganda beriladigan <b>Stars miqdorini</b> kiriting (butun son, masalan: <code>1</code>, <code>2</code>, <code>5</code>):",
        "ref_reward_updated": "✅ <b>Referal mukofoti yangilandi!</b>\n\n⭐️ Har bir referal uchun: <b>{reward} ⭐ Stars</b> beriladi.",
        "ref_reward_invalid": "❌ Noto'g'ri qiymat kiritildi. Iltimos, 1 yoki undan katta butun son kiriting!",
        "admin_users_title": "👥 <b>Foydalanuvchilar Ro'yxati</b> (Jami: <code>{total_count}</code> ta | Sahifa: <code>{page}/{total_pages}</code>):\n\n{users_list}",
        "excel_caption": "📊 <b>Telegram Stars Bot - Foydalanuvchilar To'liq Bazasi</b>\n\n👥 <b>Jami foydalanuvchilar:</b> {total_count} ta\n📅 <b>Yuklangan sana:</b> {date}",
        "excel_generating": "⏳ Excel fayli shakllantirilmoqda, iltimos kuting...",
    },

    "ru": {
        "bot_bio": "⭐ Приглашайте друзей и зарабатывайте Telegram Stars!",
        "bot_description": (
            "🌟 <b>Добро пожаловать в бот по заработку Telegram Stars!</b>\n\n"
            "Приглашайте друзей по своей ссылке и получайте Telegram Stars за каждого приглашенного! 💫\n\n"
            "Нажмите 'Start' для начала 👇"
        ),
        "welcome": (
            "🌟 <b>Здравствуйте, {name}!</b>\n\n"
            "Добро пожаловать в бот <b>Telegram Stars</b>! 🚀\n\n"
            "💎 <b>Ваш баланс:</b> <code>{balance}</code> ⭐ Stars\n\n"
            "Чтобы заработать Stars, нажмите <b>«⭐ Заработать Stars»</b> 👇"
        ),
        "btn_referral": "⭐ Заработать Stars",
        "btn_profile": "👤 Профиль и Кошелек",
        "btn_leaderboard": "🏆 Рейтинг",
        "btn_language": "🌐 Сменить язык",
        "btn_help": "ℹ️ Помощь",
        "btn_admin": "🛠 Админ-панель",
        "btn_back": "⬅️ Назад",

        # Mandatory Subscription
        "must_subscribe": (
            "⚠️ <b>Для использования бота необходимо подписаться на наш официальный канал!</b>\n\n"
            "После подписки нажмите кнопку <b>«✅ Проверить подписку»</b>:"
        ),
        "btn_channel_link": "📢 Подписаться на канал",
        "btn_check_sub": "✅ Проверить подписку",
        "sub_not_completed": "❌ Вы еще не подписались на обязательные каналы! Пожалуйста, подпишитесь и проверьте снова.",
        "sub_success": "✅ <b>Подписка успешно подтверждена!</b> Приятного использования.",

        # Referral System
        "referral_title": (
            "⭐ <b>Заработок Stars & Приглашение Друзей</b>\n\n"
            "За каждого приглашенного друга вы получаете <b>+{reward} ⭐ Stars</b>! 🌟\n\n"
            "📊 <b>Приглашено друзей:</b> <code>{ref_count}</code> чел.\n"
            "💎 <b>Ваш баланс:</b> <code>{balance}</code> ⭐ Stars\n\n"
            "🔗 <b>Ваша персональная реферальная ссылка:</b>\n"
            "<code>{ref_link}</code>\n\n"
            "<i>Отправьте эту ссылку друзьям и в группы!</i>"
        ),
        "btn_share_ref": "🚀 Поделиться с друзьями",
        "share_text": "🌟 Заходи в бот Telegram Stars и зарабатывай Stars за друзей! 👇",
        "new_referral_notify": "🎉 <b>По вашей ссылке зарегистрировался новый друг!</b>\nВам начислено <b>+{reward} ⭐ Stars</b>! 🌟",

        # Profile
        "profile_text": (
            "👤 <b>Ваш Профиль</b>\n\n"
            "🆔 <b>Telegram ID:</b> <code>{user_id}</code>\n"
            "👤 <b>Имя:</b> {name}\n"
            "💎 <b>Баланс Stars:</b> <code>{balance}</code> ⭐ Stars\n"
            "👥 <b>Приглашено друзей:</b> <code>{ref_count}</code> чел.\n"
            "📅 <b>Дата регистрации:</b> {created_at}\n\n"
            "🔗 <b>Ваша реферальная ссылка:</b>\n"
            "<code>{ref_link}</code>"
        ),
        "btn_my_history": "📜 История транзакций",
        "no_history": "ℹ️ У вас пока нет истории транзакций.",
        "history_title": "📜 <b>История транзакций:</b>\n\n{history}",

        # Leaderboard
        "leaderboard_title": (
            "🏆 <b>Рейтинг Топ Рефералов</b>\n\n"
            "Самые активные участники по приглашению друзей:\n\n"
            "{leaderboard}\n\n"
            "<i>Приглашайте друзей и войдите в Топ 10! ⭐</i>"
        ),
        "no_donors": "Рейтинг пока пуст. Будьте первыми!",

        # Language
        "lang_select": "🌐 <b>Выберите язык / Tilni tanlang / Select language:</b>",
        "lang_changed": "✅ <b>Язык успешно изменен!</b>",

        # Help
        "help_text": (
            "ℹ️ <b>О боте и заработке Telegram Stars</b>\n\n"
            "🌟 <b>Как зарабатывать Stars?</b>\n"
            "1. Перейдите в раздел «⭐ Заработать Stars».\n"
            "2. Скопируйте персональную ссылку.\n"
            "3. За каждого друга вы мгновенно получаете Stars на баланс!\n\n"
            "📞 <b>Поддержка:</b> По всем вопросам обращайтесь к администратору."
        ),

        # Admin
        "admin_title": (
            "🛠 <b>Панель Администратора</b>\n\n"
            "👥 <b>Всего пользователей:</b> <code>{total_users}</code>\n"
            "⭐️ <b>Награда за реферала:</b> <code>{ref_reward}</code> ⭐ Stars\n"
            "📦 <b>Всего транзакций:</b> <code>{total_txs}</code>\n"
            "📢 <b>Обязательных каналов:</b> <code>{channel_count}</code>"
        ),
        "btn_admin_stats": "📊 Статистика",
        "btn_users_list": "👥 Пользователи",
        "btn_export_excel": "📥 Скачать Excel (.xlsx)",
        "btn_set_ref_reward": "⚙️ Цена реферала ({reward} ⭐)",
        "btn_broadcast": "📢 Рассылка",
        "btn_manage_channels": "📢 Обяз. каналы",
        "broadcast_prompt": "✍️ Введите сообщение для рассылки всем пользователям (текст, фото или видео):",
        "broadcast_started": "🚀 Рассылка началась...",
        "broadcast_finished": "✅ Рассылка завершена!\n\n📊 Отправлено: {success}\n❌ Ошибок: {failed}",
        
        "prompt_set_ref_reward": "✍️ Введите <b>количество Stars</b> за 1 приглашенного реферала (целое число, например: <code>1</code>, <code>2</code>, <code>5</code>):",
        "ref_reward_updated": "✅ <b>Награда за реферала обновлена!</b>\n\n⭐️ За каждого реферала: <b>{reward} ⭐ Stars</b>.",
        "ref_reward_invalid": "❌ Введено неверное число. Введите целое положительное число!",
        "admin_users_title": "👥 <b>Список Пользователей</b> (Всего: <code>{total_count}</code> | Стр: <code>{page}/{total_pages}</code>):\n\n{users_list}",
        "excel_caption": "📊 <b>База Пользователей (Excel)</b>\n\n👥 <b>Всего пользователей:</b> {total_count}\n📅 <b>Дата выгрузки:</b> {date}",
        "excel_generating": "⏳ Формирование Excel файла, пожалуйста подождите...",
    },

    "en": {
        "bot_bio": "⭐ Invite friends and earn Telegram Stars! Official Stars bot.",
        "bot_description": (
            "🌟 <b>Welcome to the Telegram Stars Earning Bot!</b>\n\n"
            "Invite friends using your unique referral link and earn Telegram Stars for each friend! 💫\n\n"
            "Tap 'Start' to begin 👇"
        ),
        "welcome": (
            "🌟 <b>Welcome, {name}!</b>\n\n"
            "Welcome to the <b>Telegram Stars</b> bot! 🚀\n\n"
            "💎 <b>Your Balance:</b> <code>{balance}</code> ⭐ Stars\n\n"
            "Tap <b>«⭐ Earn Stars»</b> below to start earning Stars 👇"
        ),
        "btn_referral": "⭐ Earn Stars",
        "btn_profile": "👤 Profile & Wallet",
        "btn_leaderboard": "🏆 Leaderboard",
        "btn_language": "🌐 Change Language",
        "btn_help": "ℹ️ Help",
        "btn_admin": "🛠 Admin Panel",
        "btn_back": "⬅️ Back",

        # Mandatory Subscription
        "must_subscribe": (
            "⚠️ <b>Please subscribe to our official channel to continue using the bot!</b>\n\n"
            "After joining, tap <b>«✅ Check Subscription»</b>:"
        ),
        "btn_channel_link": "📢 Join Channel",
        "btn_check_sub": "✅ Check Subscription",
        "sub_not_completed": "❌ You haven't subscribed to all required channels yet! Please join and verify again.",
        "sub_success": "✅ <b>Subscription confirmed!</b> Enjoy using the bot.",

        # Referral System
        "referral_title": (
            "⭐ <b>Earn Stars & Invite Friends</b>\n\n"
            "For every invited friend, you get <b>+{reward} ⭐ Stars</b>! 🌟\n\n"
            "📊 <b>Referred friends:</b> <code>{ref_count}</code>\n"
            "💎 <b>Your Balance:</b> <code>{balance}</code> ⭐ Stars\n\n"
            "🔗 <b>Your exclusive invite link:</b>\n"
            "<code>{ref_link}</code>\n\n"
            "<i>Share this link with your friends and groups!</i>"
        ),
        "btn_share_ref": "🚀 Share with friends",
        "share_text": "🌟 Check out this awesome Telegram Stars bot and earn Stars! 👇",
        "new_referral_notify": "🎉 <b>A new friend joined using your link!</b>\nYou earned <b>+{reward} ⭐ Stars</b> to your balance! 🌟",

        # Profile
        "profile_text": (
            "👤 <b>Your Profile</b>\n\n"
            "🆔 <b>Telegram ID:</b> <code>{user_id}</code>\n"
            "👤 <b>Name:</b> {name}\n"
            "💎 <b>Stars Balance:</b> <code>{balance}</code> ⭐ Stars\n"
            "👥 <b>Referred Friends:</b> <code>{ref_count}</code>\n"
            "📅 <b>Joined:</b> {created_at}\n\n"
            "🔗 <b>Your Referral Link:</b>\n"
            "<code>{ref_link}</code>"
        ),
        "btn_my_history": "📜 Transaction History",
        "no_history": "ℹ️ You don't have any transactions yet.",
        "history_title": "📜 <b>Transaction History:</b>\n\n{history}",

        # Leaderboard
        "leaderboard_title": (
            "🏆 <b>Top Referrers Leaderboard</b>\n\n"
            "Most active referrers earning Telegram Stars:\n\n"
            "{leaderboard}\n\n"
            "<i>Invite friends to reach the Top 10! ⭐</i>"
        ),
        "no_donors": "Leaderboard is empty. Be the first to invite friends!",

        # Language
        "lang_select": "🌐 <b>Select language / Tilni tanlang / Выберите язык:</b>",
        "lang_changed": "✅ <b>Language successfully changed!</b>",

        # Help
        "help_text": (
            "ℹ️ <b>About & Telegram Stars Earning Guide</b>\n\n"
            "🌟 <b>How to earn Stars?</b>\n"
            "1. Go to «⭐ Earn Stars» section.\n"
            "2. Share your personal invite link.\n"
            "3. Earn Stars directly into your balance for each friend!\n\n"
            "📞 <b>Support:</b> Contact admin for questions or inquiries."
        ),

        # Admin
        "admin_title": (
            "🛠 <b>Admin Control Panel</b>\n\n"
            "👥 <b>Total Users:</b> <code>{total_users}</code>\n"
            "⭐️ <b>Referral Reward:</b> <code>{ref_reward}</code> ⭐ Stars\n"
            "📦 <b>Total Transactions:</b> <code>{total_txs}</code>\n"
            "📢 <b>Required Channels:</b> <code>{channel_count}</code>"
        ),
        "btn_admin_stats": "📊 Statistics",
        "btn_users_list": "👥 Users List",
        "btn_export_excel": "📥 Download Excel (.xlsx)",
        "btn_set_ref_reward": "⚙️ Ref Reward ({reward} ⭐)",
        "btn_broadcast": "📢 Broadcast",
        "btn_manage_channels": "📢 Req. Channels",
        "broadcast_prompt": "✍️ Enter the broadcast message (text, photo, or video):",
        "broadcast_started": "🚀 Broadcast started...",
        "broadcast_finished": "✅ Broadcast completed!\n\n📊 Sent: {success}\n❌ Failed: {failed}",
        
        "prompt_set_ref_reward": "✍️ Enter the <b>Stars reward amount</b> for 1 invited friend (e.g. <code>1</code>, <code>2</code>, <code>5</code>):",
        "ref_reward_updated": "✅ <b>Referral reward updated!</b>\n\n⭐️ Reward per referral: <b>{reward} ⭐ Stars</b>.",
        "ref_reward_invalid": "❌ Invalid number. Please enter a positive integer!",
        "admin_users_title": "👥 <b>Users List</b> (Total: <code>{total_count}</code> | Page: <code>{page}/{total_pages}</code>):\n\n{users_list}",
        "excel_caption": "📊 <b>Telegram Stars Bot - Users Database (Excel)</b>\n\n👥 <b>Total Users:</b> {total_count}\n📅 <b>Export Date:</b> {date}",
        "excel_generating": "⏳ Generating Excel file, please wait...",
    }
}

def t(key: str, lang: str = "uz", **kwargs) -> str:
    lang_dict = TEXTS.get(lang, TEXTS["uz"])
    text_template = lang_dict.get(key, TEXTS["uz"].get(key, f"[{key}]"))
    if kwargs:
        try:
            return text_template.format(**kwargs)
        except Exception:
            return text_template
    return text_template
