# 🌟 Telegram Stars Ishlash Boti (24/7 Hosting Qo'llanmasi)

Ushbu bot orqali foydalanuvchilar o'z do'stlarini taklif qilib, har bir taklif qilingan do'st uchun **Telegram Stars** ishlab olishlari mumkin.

---

## 📌 Asosiy Xususiyatlar

- ⭐ **Stars Ishlash (Referal tizimi)**: Har bir yangi do'st uchun Stars mukofoti avtomatik tarzda foydalanuvchi hisobiga tushadi.
- ⚙️ **Admin Panel**:
  - Referal narxini istalgan vaqt o'zgartirish (masalan: `1`, `2`, `5`, `10` Stars).
  - Foydalanuvchilar ro'yxati va umumiy sonini ko'rish (sahifalangan).
  - Barcha foydalanuvchilar bazasini **Excel (.xlsx)** formatida yuklab olish.
  - Xabar tarqatish (Rassilka - matn, rasm, video).
  - Majburiy obuna kanallarini boshqarish.
- 🌐 **3 ta til**: O'zbekcha, Ruscha, Inglizcha.
- 🏆 **Reyting**: Eng ko'p Stars ishlaganlar jadvali.

---

## 🚀 1-QADAM: GitHub'ga Yuklash (Buyruqlar)

1. [GitHub.com](https://github.com) saytida yangi bo'sh repository (masalan `telegram-stars-bot`) yarating.
2. Kompyuteringizdagi terminalda quyidagi buyruqlarni ketma-ket bajaring:

```bash
git init
git add .
git commit -m "Initial commit: Telegram Stars Bot"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NOMI.git
git push -u origin main
```
*(Eslatma: `USERNAME` va `REPO_NOMI` o'rniga o'zingizning GitHub username va repository nomingizni yozasiz)*

---

## ☁️ 2-QADAM: Render.com da 24/7 Bepul Ishga Tushirish

1. [Render.com](https://render.com) ga kiring va GitHub orqali ro'yxatdan o'ting.
2. **Dashboard** bo'limida **«New +»** tugmasini bosing va **«Web Service»** ni tanlang.
3. GitHub repositoryingizni (`telegram-stars-bot`) tanlang va **«Connect»** bosing.
4. Quyidagi sozlamalarni kiriting:
   - **Name**: `telegram-stars-bot` (yoki istalgan nom)
   - **Region**: Frankfurt (yoki eng yaqin region)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: `Free` ($0/oy)

5. **Environment Variables** (Maxfiy o'zgaruvchilar) bo'limiga quyidagilarni qo'shing:
   - `BOT_TOKEN` = `8985537152:AAGwr18aMa9oj1s5J6zEO0hE4ytLXurO6_I`
   - `ADMIN_IDS` = `6781163470`
   - `DB_PATH` = `data/bot.db`

6. **«Deploy Web Service»** tugmasini bosing.
   Bot bir necha daqiqada avtomatik ishga tushadi va 24/7 uzluksiz ishlaydi! 🎉

---

## 💡 Botni Ishlatish va Boshqarish

- `/start` — Botni ishga tushirish.
- `/admin` — Admin panelga kirish (Faqat `6781163470` va qo'shilgan adminlar uchun).
