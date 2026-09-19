import telebot, requests

BOT_TOKEN = '8801159306:AAGopW0Ecg9wROzTRkfV8ijjm3AIYOus0i0'
bot = telebot.TeleBot(BOT_TOKEN)

WIN_PCT_FIXED = 0.1
BASE_PROFIT = 0.02
current_profit = BASE_PROFIT

def get_price():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
        return float(r['price'])
    except:
        return None

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"🔒 الخاص - إشارة ثابتة {WIN_PCT_FIXED}%\nالربح الحالي ${current_profit:.2f}\n\n /signal")

@bot.message_handler(commands=['signal'])
def signal(m):
    global current_profit
    price = get_price()
    if not price:
        bot.send_message(m.chat.id, "❌ السوق مش راد")
        return
    target = price * (1 + WIN_PCT_FIXED/100)
    stop = price - 10000
    bot.send_message(m.chat.id, f"🚀 دخول @ ${price:.2f}\n🎯 هدف ثابت +{WIN_PCT_FIXED}% = ${target:.2f}\n💰 ربح الصفقة = ${current_profit:.2f}\n🛑 وقف بعيد {stop:.2f}\n\nتحقق؟ /win  ما تحقق؟ /loss")

@bot.message_handler(commands=['win'])
def win(m):
    global current_profit
    bot.send_message(m.chat.id, f"✅ ربح ثابت {WIN_PCT_FIXED}% +${current_profit:.2f}")
    current_profit = current_profit * 2
    bot.send_message(m.chat.id, f"🔥 الجاي مضاعف = ${current_profit:.2f} - الإشارة ثابتة {WIN_PCT_FIXED}%")

@bot.message_handler(commands=['loss'])
def loss(m):
    global current_profit
    current_profit = BASE_PROFIT
    bot.send_message(m.chat.id, f"❌ خسارة بعيدة - رجعنا ${BASE_PROFIT}")

print(f"Bot running FIXED {WIN_PCT_FIXED}%")
bot.infinity_polling()
