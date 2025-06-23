import os
import logging
import requests
import threading
import time
import random
from flask import Flask, jsonify

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "telegram-bot-secret")

# Bot configuration
BOT_TOKEN = "7846959922:AAHtfU7tjgtaRnf1qogfsaxoy15_-UO_P4g"
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

# Advanced Username Generator (no database dependencies)
class AdvancedUsernameGenerator:
    def __init__(self):
        self.gaming_words = ['Alpha', 'Beta', 'Cyber', 'Neo', 'Pro', 'Elite', 'Prime', 'Ultra', 'Quantum', 'Phoenix', 'Shadow', 'Storm', 'Fire', 'Ice', 'Thunder', 'Ghost', 'Nova', 'Blaze', 'Apex', 'Vortex']
        self.tech_words = ['Code', 'Data', 'Sync', 'Node', 'Core', 'Link', 'Hack', 'Bit', 'Byte', 'Cloud', 'Logic', 'Pixel', 'Matrix', 'Vector', 'Cache', 'Debug', 'Binary', 'Crypto', 'Token', 'Mesh']
        self.creative_words = ['Art', 'Flow', 'Vibe', 'Wave', 'Glow', 'Spark', 'Dream', 'Magic', 'Star', 'Moon', 'Sun', 'Sky', 'Ocean', 'Forest', 'Crystal', 'Diamond', 'Gold', 'Silver', 'Pearl', 'Jade']
        self.pro_suffixes = ['X', 'Pro', 'Max', 'Core', 'Tech', 'Lab', 'Hub', 'Zone', 'Base', 'Net', 'Sys', 'Dev', 'AI', 'Bot', 'App', 'Web', 'Code', 'Data', 'Sync', 'Link']
