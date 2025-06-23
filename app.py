import os
import logging
import requests
import threading
import time
from flask import Flask, jsonify

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Bot configuration
BOT_TOKEN = "7846959922:AAHtfU7tjgtaRnf1qogfsaxoy15_-UO_P4g"
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_message(chat_id, text):
    try:
        response = requests.post(f'{BASE_URL}/sendMessage', json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Send message error: {e}")
        return False

def handle_message(chat_id, text, user_data):
    user_id = user_data.get('id')
    username = user_data.get('username', 'Unknown')
    
    logger.info(f"Message from @{username}: {text}")
    
    if text.startswith('/start'):
        send_message(chat_id, '''🎯 <b>Welcome to Rare Username Generator!</b>

💎 <b>Crypto-Only Subscription Plans:</b>
• <b>Free:</b> 5 usernames/day
• <b>Premium ($9.99/month):</b> Unlimited + availability checking
• <b>VIP ($29.99/month):</b> Premium + priority support

📝 <b>Commands:</b>
/generate - Generate usernames
/subscribe - View subscription options
/help - All commands''')
        
    elif text.startswith('/generate'):
        import random
        prefixes = ['Alpha', 'Beta', 'Cyber', 'Neo', 'Pro', 'Elite', 'Prime', 'Ultra']
        suffixes = ['X', 'Pro', 'Max', 'Core', 'Tech', 'Lab', 'Hub', 'Zone']
        
        usernames = []
        for i in range(8):
            username = random.choice(prefixes) + random.choice(suffixes) + str(random.randint(10, 999))
            score = random.randint(70, 95)
            if score >= 90:
                icon = '💎'
            elif score >= 80:
                icon = '🔥'
            else:
                icon = '⭐'
            usernames.append(f'{icon} <code>{username}</code> - Score: {score}/100')
        
        response = '🎯 <b>Generated Usernames:</b>\n\n' + '\n'.join(usernames)
        send_message(chat_id, response)
        
    elif text.startswith('/subscribe'):
        send_message(chat_id, '''💎 <b>Crypto-Only Subscription Plans</b>

🔥 <b>Premium - $9.99/month</b>
• Unlimited username generations
• Platform availability checking

💎 <b>VIP - $29.99/month</b>
• Everything in Premium + custom requests

<b>Payment Addresses:</b>
BTC: <code>bc1qygedkhjxaw0dfx85x232rdxdamp9hczac5fpc3</code>
LTC: <code>ltc1q5da462tgrmsdjt95n8lj66hwrdllrma8h0lnaa</code>
ETH/USDT: <code>0x020b47D9a3782B034ec8e8fa216B827aB253e3c3</code>

<b>Instructions:</b>
1. Send exact amount to appropriate address
2. Forward transaction hash to this bot
3. Subscription activates within 24 hours''')
        
    elif text.startswith('/help'):
        send_message(chat_id, '''🤖 <b>Available Commands:</b>

/start - Welcome message
/generate - Generate 8 usernames
/subscribe - View crypto subscription plans
/help - Show this help message''')
        
    elif text.startswith('/admin_stats') and user_id == 7481885595:
        send_message(chat_id, '''📊 <b>Bot Statistics</b>

👥 <b>Status:</b> Running on Heroku
🤖 <b>Bot:</b> @UsernameavailablesBot
💰 <b>Payments:</b> BTC, LTC, ETH, USDT accepted''')
    
    else:
        send_message(chat_id, 'Please use a command. Type /help for available commands.')

def run_telegram_polling():
    logger.info("Starting Telegram bot polling...")
    
    # Test bot connection
    try:
        response = requests.get(f'{BASE_URL}/getMe', timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            logger.info(f"Bot connected: @{bot_info['result']['username']}")
        else:
            logger.error(f"Bot connection failed: {response.status_code}")
            return
    except Exception as e:
        logger.error(f"Bot connection error: {e}")
        return
    
    offset = 0
    logger.info("Bot listening for messages...")
    
    while True:
        try:
            response = requests.get(f'{BASE_URL}/getUpdates', params={
                'offset': offset,
                'timeout': 30,
                'allowed_updates': ['message']
            }, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                updates = data.get('result', [])
                
                for update in updates:
                    try:
                        if 'message' in update:
                            message = update['message']
                            chat_id = message['chat']['id']
                            text = message.get('text', '')
                            user_data = message.get('from', {})
                            
                            if text:
                                handle_message(chat_id, text, user_data)
                        
                        offset = max(offset, update['update_id'] + 1)
                        
                    except Exception as msg_error:
                        logger.error(f"Message processing error: {msg_error}")
                        offset = max(offset, update.get('update_id', 0) + 1)
                        
            else:
                logger.error(f"API request failed: {response.status_code}")
                time.sleep(5)
                
        except Exception as e:
            logger.error(f"Polling error: {e}")
            time.sleep(5)

def start_bot():
    try:
        bot_thread = threading.Thread(target=run_telegram_polling, daemon=True)
        bot_thread.start()
        logger.info("Telegram bot started successfully")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

# Start bot immediately
start_bot()

@app.route('/')
def index():
    return '''
    <h1>Telegram Username Generator Bot</h1>
    <p>Bot Status: <strong>Active</strong></p>
    <p>Bot Username: <strong>@UsernameavailablesBot</strong></p>
    <p>Features:</p>
    <ul>
        <li>Rare username generation with value scoring</li>
        <li>Crypto-only subscriptions (BTC, LTC, ETH, USDT)</li>
        <li>Premium ($9.99/month) and VIP ($29.99/month) tiers</li>
    </ul>
    <p><a href="/health">Health Check</a></p>
    '''

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "bot": "running",
        "service": "telegram-username-generator"
    })

@app.route('/test')
def test():
    return "Bot is working! ✅"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
