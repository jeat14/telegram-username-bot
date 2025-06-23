from app import app
import threading
import time
import logging
from telegram_polling import run_telegram_bot

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start_bot_polling():
    """Start the Telegram bot in a separate thread"""
    logger.info("Starting Telegram bot polling...")
    time.sleep(1)  # Brief wait for Flask to initialize
    try:
        run_telegram_bot()
    except Exception as e:
        logger.error(f"Bot polling error: {e}")

if __name__ == '__main__':
    logger.info("Starting Rare Username Generator Bot system...")
    
    # Start Telegram bot polling in background
    bot_thread = threading.Thread(target=start_bot_polling, daemon=True)
    bot_thread.start()
    logger.info("Bot polling thread started")
    
    # Start Flask app
    logger.info("Starting Flask web server...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
