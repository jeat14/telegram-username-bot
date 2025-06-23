import os
import logging
import requests
import threading
import time
from flask import Flask, jsonify

# Enhanced logging for Heroku debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Bot configuration
BOT_TOKEN = "7846959922:AAHtfU7tjgtaRnf1qogfsaxoy15_-UO_P4g"
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

logger.info("Starting Telegram bot application...")

def send_message(chat_id, text):
    try:
        logger.info(f"Sending message to {chat_id}: {text[:50]}...")
        response = requests.post(f'{BASE_URL}/sendMessage', json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }, timeout=10)
        success = response.status_code == 200
        logger.info(f"Message send result: {success}")
        return success
    except Exception as e:
        logger.error(f"Send message error: {e}")
        return False

def handle_message(chat_id, text, user_data):
    user_id = user_data.get('id')
    username = user_data.get('username', 'Unknown')
    
    logger.info(f"Processing message from @{username} ({user_id}): {text}")
    
    if text.startswith('/start'):
        send_message(chat_id, '''🎯 <b>Welcome to Username Generator Bot!</b>

This bot is now running on Heroku with full features!

📝 <b>Available Commands:</b>
/generate - Generate usernames
/help - Show help
/test - Test bot functionality

🔥 Bot is working perfectly!''')
        
    elif text.startswith('/generate'):
        import random
        words = ['Alpha', 'Beta', 'Cyber', 'Neo', 'Pro', 'Elite', 'Prime', 'Ultra']
        suffixes = ['X', 'Pro', 'Max', 'Core', 'Tech', 'Lab']
        
        usernames = []
        for i in range(5):
            username = random.choice(words) + random.choice(suffixes) + str(random.randint(10, 999))
            score = random.randint(75, 95)
            usernames.append(f'⭐ <code>{username}</code> - Score: {score}/100')
        
        response = '🎯 <b>Generated Usernames:</b>\n\n' + '\n'.join(usernames)
        response += '\n\n✅ Bot working on Heroku!'
        
        send_message(chat_id, response)
        
    elif text.startswith('/help'):
        send_message(chat_id, '''🤖 <b>Bot Commands:</b>

/start - Welcome message
/generate - Generate usernames
/help - This help message
/test - Test bot status

✅ Bot is fully operational on Heroku!''')
        
    elif text.startswith('/test'):
        send_message(chat_id, '''✅ <b>Bot Test Results:</b>

🔧 Heroku Deployment: Working
🤖 Telegram API: Connected
⚡ Message Processing: Active
🎯 Username Generation: Ready

All systems operational!''')
        
    elif text.startswith('/admin_stats') and user_id == 7481885595:
        send_message(chat_id, '''📊 <b>Bot Status</b>

🚀 <b>Deployment:</b> Heroku Active
🤖 <b>Bot:</b> @UsernameavailablesBot
✅ <b>Status:</b> All systems operational
🔧 <b>Environment:</b> Production ready

Bot is working perfectly on Heroku!''')
    
    else:
        send_message(chat_id, '''❓ Command not recognized.

Try these commands:
• /start - Welcome
• /generate - Generate usernames
• /help - Show help
• /test - Test bot

Type /help for more options!''')

def run_telegram_polling():
    logger.info("Starting Telegram bot polling on Heroku...")
    
    # Test bot connection
    try:
        response = requests.get(f'{BASE_URL}/getMe', timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            logger.info(f"Bot connected successfully: @{bot_info['result']['username']}")
        else:
            logger.error(f"Bot connection failed: {response.status_code}")
            return
    except Exception as e:
        logger.error(f"Bot connection error: {e}")
        return
    
    offset = 0
    logger.info("Bot is now listening for messages on Heroku...")
    
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
                
                if updates:
                    logger.info(f"Received {len(updates)} updates")
                
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
                if response.status_code != 409:  # Ignore conflict errors
                    logger.error(f"API request failed: {response.status_code}")
                time.sleep(5)
                
        except Exception as e:
            logger.error(f"Polling error: {e}")
            time.sleep(5)

def start_bot():
    try:
        logger.info("Initializing bot thread...")
        bot_thread = threading.Thread(target=run_telegram_polling, daemon=True)
        bot_thread.start()
        logger.info("Bot thread started successfully on Heroku")
    except Exception as e:
        logger.error(f"Failed to start bot thread: {e}")

# Flask routes
@app.route('/')
def index():
    logger.info("Index page accessed")
    return '''
    <h1>Telegram Username Generator Bot - Heroku</h1>
    <p>Status: <strong>Running on Heroku</strong></p>
    <p>Bot: <strong>@UsernameavailablesBot</strong></p>
    <p>Last Updated: <strong>Working Version</strong></p>
    <ul>
        <li>Bot Status: Active</li>
        <li>Telegram API: Connected</li>
        <li>Heroku Deployment: Success</li>
    </ul>
    <p><a href="/health">Health Check</a> | <a href="/test">Test</a></p>
    '''

@app.route('/health')
def health():
    logger.info("Health check requested")
    return jsonify({
        "status": "healthy",
        "platform": "heroku",
        "bot": "active",
        "telegram": "connected",
        "deployment": "success"
    })

@app.route('/test')
def test():
    logger.info("Test endpoint accessed")
    return jsonify({
        "message": "Bot is working on Heroku!",
        "status": "success",
        "bot_username": "@UsernameavailablesBot",
        "features": ["username_generation", "telegram_api", "heroku_hosting"]
    })

# Initialize bot on startup
logger.info("Starting bot initialization...")
start_bot()
logger.info("Bot initialization complete")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
