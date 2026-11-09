TELEGRAM VIDEO DOWNLOADER (TikTok + X/Twitter)
==============================================

ပါဝင်တဲ့ဖိုင်များ
- bot.py             : Telegram Bot အလုပ်လုပ်မည့် Python code
- requirements.txt   : လိုအပ်သော Python packages
- render.yaml        : Render Free Web Service setting
- Dockerfile         : FFmpeg ပါဝင်သော deployment image
- .gitignore         : မတင်သင့်သောဖိုင်များကို ကာကွယ်ရန်

အရေးကြီး
ဒီ Bot သည် TikTok နှင့် X (Twitter) link များကိုသာ လက်ခံရန် သတ်မှတ်ထားသည်။
အကောင်းဆုံးရရှိနိုင်သည့် quality ကို ရွေးချယ်ရန် yt-dlp ကို အသုံးပြုသည်။
Telegram သို့ တိုက်ရိုက်ပို့ရာတွင် 45 MB ထက်ကြီးသောဖိုင်ကို ပယ်ချမည်။
Platform များ၏ ပြောင်းလဲမှုကြောင့် အချို့ link များ Download မရနိုင်ပါ။
ကိုယ်ပိုင်ခွင့်ရှိသော သို့မဟုတ် Download လုပ်ခွင့်ရှိသော content ကိုသာ အသုံးပြုပါ။

GitHub သို့ Upload လုပ်နည်း
1. ZIP ကို Extract လုပ်ပါ။
2. GitHub မှာ ဖန်တီးထားတဲ့ Repository ကိုဖွင့်ပါ။
3. Add file > Upload files ကိုနှိပ်ပါ။
4. Extract လုပ်ထားတဲ့ folder ထဲက ဖိုင်အားလုံးကို ရွေးပြီး Upload လုပ်ပါ။
   (ZIP ဖိုင်ကိုယ်တိုင်ကို မတင်ပါနှင့်။)
5. Commit changes ကိုနှိပ်ပါ။

Render Free မှာ Deploy လုပ်နည်း
1. https://render.com ကိုဖွင့်ပြီး GitHub နဲ့ Sign in လုပ်ပါ။
2. New > Blueprint ကိုရွေးပါ။
3. ဒီ Bot ရဲ့ GitHub Repository ကိုချိတ်ပါ။
4. Render က render.yaml ကိုဖတ်ပြီး Service တည်ဆောက်ပေးမည်။
5. Environment Variables မှာ BOT_TOKEN ကိုထည့်ပါ။
   - Telegram မှာ @BotFather ကိုဖွင့်ပါ။
   - /newbot ကိုပို့ပြီး ညွှန်ကြားချက်အတိုင်း Bot ဖန်တီးပါ။
   - ရလာတဲ့ token ကို BOT_TOKEN နေရာမှာ ထည့်ပါ။
   - WEBHOOK_SECRET ကို Render က အလိုအလျောက်ထုတ်ပေးမည်။
6. Deploy ပြီးရင် Telegram မှာ Bot ကိုဖွင့်ပြီး /start ပို့ပါ။

သတိပြုရန်
- BOT_TOKEN ကို ဘယ်သူ့ကိုမှ မမျှဝေပါနှင့်။
- GitHub Repository ထဲ token ကို မထည့်ပါနှင့်။
- Render Free Service သည် အသုံးမပြုချိန်တွင် အိပ်သွားနိုင်ပြီး ပြန်နိုးရန်
  အချိန်အနည်းငယ်ကြာနိုင်သည်။
- Free plan ၏ resource/availability စည်းမျဉ်းများသည် အချိန်နှင့်အမျှ ပြောင်းနိုင်သည်။
