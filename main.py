import os
import logging
import requests
import threading
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Configure database
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bot.db"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Initialize database tables
with app.app_context():
    import models
    db.create_all()

# Bot configuration
BOT_TOKEN = '7846959922:AAHtfU7tjgtaRnf1qogfsaxoy15_-UO_P4g'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_message(chat_id, text):
    try:
        response = requests.post(f'{BASE_URL}/sendMessage', json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }, timeout=15)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Send message error: {e}")
        return False

def handle_message(chat_id, text, user_data):
    user_id = user_data.get('id')
    username = user_data.get('username', 'Unknown')
    
    logger.info(f"Message from @{username} ({user_id}): {text}")
    
    if text.startswith('/start'):
        send_message(chat_id, '''🎯 <b>Welcome to Rare Username Generator!</b>

💎 <b>Crypto-Only Subscription Plans:</b>
• <b>Free:</b> 5 usernames/day
• <b>Premium ($9.99/month):</b> Unlimited + availability checking
• <b>VIP ($29.99/month):</b> Premium + priority support

📝 <b>Commands:</b>
/generate - Generate usernames
/subscribe - View subscription options
/help - All commands

<b>💰 All payments in crypto only!</b>''')
        
    elif text.startswith('/generate'):
        import random
        prefixes = ['Alpha', 'Beta', 'Cyber', 'Neo', 'Pro', 'Elite', 'Prime', 'Ultra', 'Quantum', 'Phoenix']
        suffixes = ['X', 'Pro', 'Elite', 'Max', 'Core', 'Tech', 'Lab', 'Hub', 'Zone', 'Base']
        words = ['Ghost', 'Storm', 'Fire', 'Ice', 'Thunder', 'Shadow', 'Light', 'Dark', 'Nova', 'Blaze']
        
        usernames = []
        for i in range(8):
            choice = random.randint(1, 4)
            if choice == 1:
                username = random.choice(prefixes) + random.choice(suffixes) + str(random.randint(10, 999))
            elif choice == 2:
                username = random.choice(words) + random.choice(suffixes)
            elif choice == 3:
                username = random.choice(prefixes) + random.choice(words)
            else:
                username = random.choice(words) + str(random.randint(100, 9999))
            usernames.append(username)
        
        response = '🎯 <b>Generated Usernames:</b>\n\n'
        for username in usernames:
            score = random.randint(65, 95)
            if score >= 90:
                icon, estimate = '💎', '$500-$5000+'
            elif score >= 80:
                icon, estimate = '🔥', '$100-$500'
            elif score >= 70:
                icon, estimate = '⭐', '$50-$200'
            else:
                icon, estimate = '📝', '$20-$100'
            response += f'{icon} <code>{username}</code> - Score: {score}/100 (Est: {estimate})\n'
        
        response += '\n💡 Use /subscribe for unlimited generations!'
        send_message(chat_id, response)
        
    elif text.startswith('/subscribe'):
        send_message(chat_id, '''💎 <b>Crypto-Only Subscription Plans</b>

🔥 <b>Premium - $9.99/month</b>
• Unlimited username generations
• Platform availability checking
• Priority support

💎 <b>VIP - $29.99/month</b>
• Everything in Premium + custom requests

<b>📱 Payment Methods:</b>
Bitcoin (BTC) • Litecoin (LTC) • Ethereum (ETH) • USDT

<b>💳 Payment Addresses:</b>
BTC: <code>bc1qygedkhjxaw0dfx85x232rdxdamp9hczac5fpc3</code>
LTC: <code>ltc1q5da462tgrmsdjt95n8lj66hwrdllrma8h0lnaa</code>
ETH/USDT: <code>0x020b47D9a3782B034ec8e8fa216B827aB253e3c3</code>

<b>📋 Instructions:</b>
1. Send exact amount to appropriate address above
2. Forward transaction hash to this bot
3. Subscription activates within 24 hours

<b>💰 Exact Amounts:</b>
Premium: $9.99 USD equivalent
VIP: $29.99 USD equivalent''')
        
    elif text.startswith('/help'):
        send_message(chat_id, '''🤖 <b>Available Commands:</b>

/start - Welcome message
/generate - Generate 8 random usernames
/premium - Get premium short usernames
/subscribe - View crypto subscription plans
/help - Show this help message

💰 Premium: Unlimited generations + availability checking
💎 VIP: Premium + custom requests + priority support''')
        
    elif text.startswith('/premium'):
        send_message(chat_id, '''🔒 <b>Premium Feature</b>

Ultra-rare short usernames available for Premium/VIP subscribers.

<b>Benefits:</b>
• 3-5 character premium usernames
• Unlimited generations
• Real-time availability checking
• Priority support

Use /subscribe to upgrade!''')
    
    elif text.startswith('/admin_users') and user_id == 7481885595:  # Your Telegram ID
        try:
            with app.app_context():
                from models import User
                users = User.query.all()
                
                if not users:
                    send_message(chat_id, '📊 <b>User Database</b>\n\nNo users found in database.')
                    return
                
                response = f'📊 <b>User Database ({len(users)} total)</b>\n\n'
                
                for user in users[:20]:  # Limit to first 20 users
                    username = user.username or 'No username'
                    name = f"{user.first_name or ''} {user.last_name or ''}".strip() or 'No name'
                    
                    response += f'👤 <b>@{username}</b>\n'
                    response += f'   ID: {user.telegram_id}\n'
                    response += f'   Name: {name}\n'
                    response += f'   Tier: {user.subscription_tier}\n'
                    response += f'   Generations: {user.total_generations}\n'
                    response += f'   Joined: {user.created_at.strftime("%Y-%m-%d")}\n\n'
                
                if len(users) > 20:
                    response += f'... and {len(users) - 20} more users'
                
                send_message(chat_id, response)
        except Exception as e:
            send_message(chat_id, f'❌ Error accessing user database: {str(e)}')
    
    elif text.startswith('/admin_stats') and user_id == 7481885595:  # Your Telegram ID
        try:
            with app.app_context():
                from models import User, UserInteraction
                
                total_users = User.query.count()
                premium_users = User.query.filter_by(subscription_tier='premium').count()
                vip_users = User.query.filter_by(subscription_tier='vip').count()
                total_interactions = UserInteraction.query.count()
                
                response = f'''📈 <b>Bot Statistics</b>

👥 <b>Users:</b>
• Total: {total_users}
• Free: {total_users - premium_users - vip_users}
• Premium: {premium_users}
• VIP: {vip_users}

📊 <b>Activity:</b>
• Total interactions: {total_interactions}

💰 <b>Revenue:</b>
• Premium subscriptions: ${premium_users * 9.99:.2f}/month
• VIP subscriptions: ${vip_users * 29.99:.2f}/month
• Total monthly: ${(premium_users * 9.99) + (vip_users * 29.99):.2f}'''
                
                send_message(chat_id, response)
        except Exception as e:
            send_message(chat_id, f'❌ Error accessing statistics: {str(e)}')
    
    elif text.startswith('/admin_upgrade') and user_id == 7481885595:  # Your Telegram ID
        try:
            parts = text.split(' ')
            if len(parts) < 3:
                send_message(chat_id, '''💼 <b>Admin Upgrade Command</b>

Usage: /admin_upgrade @username tier

<b>Examples:</b>
• /admin_upgrade @packoa premium
• /admin_upgrade @packoa vip
• /admin_upgrade @packoa free

<b>Available tiers:</b> free, premium, vip''')
                return
            
            target_username = parts[1].replace('@', '')
            tier = parts[2].lower()
            
            if tier not in ['free', 'premium', 'vip']:
                send_message(chat_id, '❌ Invalid tier. Use: free, premium, or vip')
                return
            
            with app.app_context():
                from models import User
                from datetime import datetime, timezone, timedelta
                
                user = User.query.filter_by(username=target_username).first()
                if not user:
                    send_message(chat_id, f'❌ User @{target_username} not found in database')
                    return
                
                old_tier = user.subscription_tier
                user.subscription_tier = tier
                
                if tier in ['premium', 'vip']:
                    # Set subscription to expire in 1 month
                    user.subscription_expires = datetime.now(timezone.utc) + timedelta(days=30)
                else:
                    user.subscription_expires = None
                
                db.session.commit()
                
                send_message(chat_id, f'''✅ <b>Subscription Updated</b>

👤 User: @{target_username}
📊 Changed: {old_tier} → {tier}
📅 Expires: {'1 month from now' if tier in ['premium', 'vip'] else 'N/A'}''')
                
        except Exception as e:
            send_message(chat_id, f'❌ Error upgrading user: {str(e)}')
    
    else:
        send_message(chat_id, 'Please use a command. Type /help for available commands.')

def run_telegram_polling():
    logger.info("Starting Telegram bot polling...")
    
    # Test connection
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

# Start bot in background thread
def start_bot():
    bot_thread = threading.Thread(target=run_telegram_polling, daemon=True)
    bot_thread.start()
    logger.info("Telegram bot started in background thread")

# Initialize bot when app starts
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
        <li>Username availability checking</li>
    </ul>
    '''

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "bot": "running"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
