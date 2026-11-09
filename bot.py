import asyncio
import logging
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ChatAction
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("video-downloader")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip()
PORT = int(os.getenv("PORT", "10000"))
PUBLIC_URL = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
MAX_UPLOAD_BYTES = 45 * 1024 * 1024  # Keep below Telegram Bot API upload limit.

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required.")
if not WEBHOOK_SECRET:
    raise RuntimeError("WEBHOOK_SECRET environment variable is required.")
if not PUBLIC_URL:
    raise RuntimeError("RENDER_EXTERNAL_URL is missing. Deploy this project as a Render Web Service.")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

ALLOWED_HOSTS = {
    "tiktok.com", "www.tiktok.com", "vm.tiktok.com", "vt.tiktok.com",
    "x.com", "www.x.com", "twitter.com", "www.twitter.com", "t.co",
}

def valid_video_url(value: str) -> bool:
    try:
        parsed = urlparse(value.strip())
        host = (parsed.hostname or "").lower()
        return parsed.scheme in {"http", "https"} and host in ALLOWED_HOSTS
    except Exception:
        return False

def download_video(url: str, folder: str) -> Path:
    output = str(Path(folder) / "video.%(ext)s")
    opts = {
        "outtmpl": output,
        "format": "best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "remux_video": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 25,
        "retries": 2,
        "max_filesize": MAX_UPLOAD_BYTES,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if not info:
            raise RuntimeError("Video information could not be read.")
        requested = info.get("requested_downloads") or []
        candidates = [Path(item.get("filepath", "")) for item in requested if item.get("filepath")]
        candidates += list(Path(folder).glob("video.*"))
        candidates = [p for p in candidates if p.is_file() and p.suffix.lower() in {".mp4", ".mkv", ".webm", ".mov"}]
        if not candidates:
            raise RuntimeError("Downloaded video file was not found.")
        result = max(candidates, key=lambda p: p.stat().st_size)
        if result.stat().st_size > MAX_UPLOAD_BYTES:
            raise RuntimeError("ဒီဗီဒီယိုဖိုင်က Telegram ပို့နိုင်တဲ့ 45 MB ထက်ကြီးနေပါတယ်။")
        return result

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "မင်္ဂလာပါ။ ဒီ Bot က TikTok နဲ့ X (Twitter) ဗီဒီယို link တွေကို MP4 အဖြစ် Download လုပ်ပေးပါတယ်။\n\n"
        "အသုံးပြုပုံ - ဗီဒီယို link ကို ဒီ Chat ထဲ ပို့လိုက်ပါ။\n"
        "မှတ်ချက် - ကိုယ်ပိုင်ခွင့်ရှိတဲ့ သို့မဟုတ် Download လုပ်ခွင့်ရှိတဲ့ ဗီဒီယိုတွေကိုသာ အသုံးပြုပါ။"
    )

@dp.message(F.text)
async def handle_link(message: Message):
    url = (message.text or "").strip()
    if not valid_video_url(url):
        await message.answer("TikTok သို့မဟုတ် X (Twitter) ရဲ့ ဗီဒီယို link ကို ပို့ပေးပါ။")
        return

    status = await message.answer("⏳ ဗီဒီယိုကို ရှာဖွေပြီး Download လုပ်နေပါတယ်...")
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)
        with tempfile.TemporaryDirectory(prefix="tg-video-") as temp_dir:
            path = await asyncio.to_thread(download_video, url, temp_dir)
            await status.edit_text("✅ Download ပြီးပါပြီ။ Telegram ကို ပို့နေပါတယ်...")
            with path.open("rb") as video_file:
                await message.answer_video(
                    video=video_file,
                    caption="Downloaded by Telegram Video Downloader",
                    supports_streaming=True,
                )
        await status.delete()
    except Exception as exc:
        log.exception("Download failed")
        msg = str(exc)
        if len(msg) > 350:
            msg = msg[:350] + "..."
        await status.edit_text(
            "❌ Download မအောင်မြင်ပါ။ Link ကိုစစ်ပြီး ထပ်စမ်းကြည့်ပါ။\n"
            "အကြောင်းရင်း: " + msg
        )

async def health(request):
    return web.Response(text="Telegram Video Downloader is running.")

async def telegram_webhook(request):
    supplied = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if supplied != WEBHOOK_SECRET:
        raise web.HTTPUnauthorized(text="Invalid webhook secret")
    update = await request.json()
    from aiogram.types import Update
    await dp.feed_update(bot, Update.model_validate(update))
    return web.Response(text="OK")

async def on_startup(app):
    webhook_url = f"{PUBLIC_URL}/telegram-webhook"
    await bot.set_webhook(
        webhook_url,
        secret_token=WEBHOOK_SECRET,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    log.info("Webhook configured: %s", webhook_url)

async def on_cleanup(app):
    await bot.session.close()

app = web.Application(client_max_size=2 * 1024 * 1024)
app.router.add_get("/", health)
app.router.add_post("/telegram-webhook", telegram_webhook)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=PORT)
