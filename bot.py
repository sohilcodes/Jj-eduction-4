import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup

# ===== ENV TOKEN =====
TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# ===== TEXT =====

disclaimer = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in loss.
We do not provide financial advice, signals, or guaranteed results.

By continuing, you confirm that you understand and accept this.
"""

welcome = """Welcome to JJ Market Study Assistant 

This assistant is designed to help individuals
develop a better understanding of financial markets
through structured learning and simple explanations.

The focus here is on:

• Thinking before acting
• Understanding how markets behave
• Learning risk awareness
• Building a clear decision process

This is not a signal service or advisory platform.

All content is shared for educational purposes only.
Market outcomes are uncertain and not guaranteed.

Select a section below to begin.
"""

think_basics = """🧠 Think Basics

Before learning markets,
it is important to understand how to think clearly.

• Avoiding impulsive decisions
• Understanding patience
• Observing before reacting
• Staying consistent

Good decisions come from clear thinking,
not speed.

Educational content only.
"""

market_view = """📊 Market View

Markets move based on supply and demand.

• Direction (trends)
• Sideways movement (ranges)
• Key areas of reaction
• Changes in volatility

The goal is observation, not prediction.

For learning purposes only.
"""

risk = """⚖️ Risk Thinking

Risk is part of every financial decision.

• Managing exposure
• Avoiding over-risking
• Thinking in probabilities
• Protecting capital over time

Understanding risk matters more than outcomes.

Educational reference only.
"""

concepts = """📘 Learn Concepts

• Basic structure ideas
• Entry & exit theory
• Trend & reversal concepts
• Importance of consistency

No signals or live trades.

Conceptual learning only.
"""

mistakes = """📉 Mistake Awareness

• Acting without a plan
• Emotional reactions
• Overcomplicating decisions
• Expecting quick outcomes

Awareness improves decision quality.

Educational guidance only.
"""

support = """📩 Support

For learning clarification contact:

@your_support_username

Only educational discussion allowed.
"""


# ===== MENU =====

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🧠 Think Basics", "📊 Market View")
    kb.row("⚖️ Risk Thinking", "📘 Learn Concepts")
    kb.row("📉 Mistake Awareness", "📩 Support")
    return kb


# ===== START =====

@bot.message_handler(commands=['start'])
def start(msg):

    d = bot.send_message(msg.chat.id, disclaimer)

    try:
        bot.pin_chat_message(msg.chat.id, d.message_id)
    except:
        pass

    bot.send_message(msg.chat.id, welcome, reply_markup=menu())


# ===== BUTTONS =====

@bot.message_handler(func=lambda m: m.text == "🧠 Think Basics")
def b1(m):
    bot.send_message(m.chat.id, think_basics)

@bot.message_handler(func=lambda m: m.text == "📊 Market View")
def b2(m):
    bot.send_message(m.chat.id, market_view)

@bot.message_handler(func=lambda m: m.text == "⚖️ Risk Thinking")
def b3(m):
    bot.send_message(m.chat.id, risk)

@bot.message_handler(func=lambda m: m.text == "📘 Learn Concepts")
def b4(m):
    bot.send_message(m.chat.id, concepts)

@bot.message_handler(func=lambda m: m.text == "📉 Mistake Awareness")
def b5(m):
    bot.send_message(m.chat.id, mistakes)

@bot.message_handler(func=lambda m: m.text == "📩 Support")
def b6(m):
    bot.send_message(m.chat.id, support)


# ===== WEBHOOK =====

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok", 200


@app.route("/")
def home():
    return "JJ Bot Running"


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(
        url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN
    )
    app.run(host="0.0.0.0", port=10000)
