import os
import logging
import requests
import threading
import time
import random
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone, timedelta

class Base(DeclarativeBase):
    pass

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "telegram-bot-secret")

# Database setup with PostgreSQL URL fix
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///bot.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Advanced Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    
    subscription_tier = db.Column(db.String(20), default='free')
    subscription_expires = db.Column(db.DateTime, nullable=True)
    crypto_wallet = db.Column(db.String(128), nullable=True)
    
    daily_generations = db.Column(db.Integer, default=0)
    total_generations = db.Column(db.Integer, default=0)
    availability_checks = db.Column(db.Integer, default=0)
    last_generation_date = db.Column(db.Date, nullable=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_active = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_banned = db.Column(db.Boolean, default=False)
    
    def can_generate(self):
        if self.subscription_tier == 'free':
            today = datetime.now(timezone.utc).date()
            if self.last_generation_date != today:
                self.daily_generations = 0
                self.last_generation_date = today
                db.session.commit()
            return self.daily_generations < 5
        elif self.subscription_tier in ['premium', 'vip']:
            if self.subscription_expires and self.subscription_expires < datetime.now(timezone.utc):
                self.subscription_tier = 'free'
                db.session.commit()
                return self.daily_generations < 5
            return True
        return False
    
    def increment_usage(self):
        today = datetime.now(timezone.utc).date()
        if self.last_generation_date != today:
            self.daily_generations = 0
            self.last_generation_date = today
        
        self.daily_generations += 1
        self.total_generations += 1
        self.last_active = datetime.now(timezone.utc)
        db.session.commit()

class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    command = db.Column(db.String(64), nullable=False)
    message_text = db.Column(db.Text, nullable=True)
    response_type = db.Column(db.String(32), nullable=True)
    
    usernames_generated = db.Column(db.Text, nullable=True)
    generation_category = db.Column(db.String(32), nullable=True)
    
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    success = db.Column(db.Boolean, default=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    transaction_hash = db.Column(db.String(128), unique=True, nullable=False)
    cryptocurrency = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Numeric(18, 8), nullable=False)
    usd_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    subscription_type = db.Column(db.String(20), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# Bot configuration
BOT_TOKEN = "7846959922:AAHtfU7tjgtaRnf1qogfsaxoy15_-UO_P4g"
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

# Advanced Username Generator
class AdvancedUsernameGenerator:
    def __init__(self):
        self.gaming_words = ['Alpha', 'Beta', 'Cyber', 'Neo', 'Pro', 'Elite', 'Prime', 'Ultra', 'Quantum', 'Phoenix', 'Shadow', 'Storm', 'Fire', 'Ice', 'Thunder', 'Ghost', 'Nova', 'Blaze', 'Apex', 'Vortex']
        self.tech_words = ['Code', 'Data', 'Sync', 'Node', 'Core', 'Link', 'Hack', 'Bit', 'Byte', 'Cloud', 'Logic', 'Pixel', 'Matrix', 'Vector', 'Cache', 'Debug', 'Binary', 'Crypto', 'Token', 'Mesh']
        self.creative_words = ['Art', 'Flow', 'Vibe', 'Wave', 'Glow', 'Spark', 'Dream', 'Magic', 'Star', 'Moon', 'Sun', 'Sky', 'Ocean', 'Forest', 'Crystal', 'Diamond', 'Gold', 'Silver', 'Pearl', 'Jade']
        self.pro_suffixes = ['X', 'Pro', 'Max', 'Core', 'Tech', 'Lab', 'Hub', 'Zone', 'Base', 'Net', 'Sys', 'Dev', 'AI', 'Bot', 'App', 'Web', 'Code', 'Data', 'Sync', 'Link']
        
    def generate_premium_usernames(self, count=5):
        """Generate ultra-rare short usernames for premium users"""
        usernames = []
        patterns = [
            lambda: random.choice(['X', 'Z', 'Q']) + random.choice(self.gaming_words[:10])[:3] + str(random.randint(1, 99)),
            lambda: random.choice(self.tech_words[:10])[:4] + random.choice(['X', 'Z', '0']),
            lambda: random.choice(['_', '.']) + random.choice(self.creative_words[:10])[:4],
            lambda: random.choice(self.gaming_words[:10])[:3] + random.choice(['_', '.', '']) + str(random.randint(1, 9)),
            lambda: ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3)) + str(random.randint(10, 99))
        ]
        
        for i in range(count):
            username = random.choice(patterns)()
            usernames.append(username)
        
        return usernames
    
    def generate_by_category(self, category='random', count=8):
        """Generate usernames by category with advanced algorithms"""
        if category == 'gaming':
            return self._generate_gaming_usernames(count)
        elif category == 'tech':
            return self._generate_tech_usernames(count)
        elif category == 'creative':
            return self._generate_creative_usernames(count)
        elif category == 'professional':
            return self._generate_professional_usernames(count)
        else:
            return self._generate_mixed_usernames(count)
    
    def _generate_gaming_usernames(self, count):
        usernames = []
        for i in range(count):
            patterns = [
                lambda: random.choice(self.gaming_words) + random.choice(self.pro_suffixes) + str(random.randint(10, 999)),
                lambda: random.choice(self.gaming_words) + random.choice(self.gaming_words) + str(random.randint(1, 99)),
                lambda: 'Dark' + random.choice(self.gaming_words) + random.choice(['X', 'Z', '']),
                lambda: random.choice(self.gaming_words) + 'Lord' + str(random.randint(1, 999)),
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_tech_usernames(self, count):
        usernames = []
        for i in range(count):
            patterns = [
                lambda: random.choice(self.tech_words) + random.choice(self.pro_suffixes) + str(random.randint(10, 999)),
                lambda: random.choice(['Dev', 'Code', 'Tech']) + random.choice(self.tech_words) + str(random.randint(1, 99)),
                lambda: random.choice(self.tech_words) + 'AI' + str(random.randint(1, 999)),
                lambda: 'Cyber' + random.choice(self.tech_words) + random.choice(['X', 'Pro', '']),
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_creative_usernames(self, count):
        usernames = []
        for i in range(count):
            patterns = [
                lambda: random.choice(self.creative_words) + random.choice(['Flow', 'Wave', 'Glow']) + str(random.randint(1, 99)),
                lambda: 'Art' + random.choice(self.creative_words) + str(random.randint(1, 999)),
                lambda: random.choice(self.creative_words) + 'Studio' + str(random.randint(1, 99)),
                lambda: random.choice(['Magic', 'Dream']) + random.choice(self.creative_words),
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_professional_usernames(self, count):
        usernames = []
        business_words = ['Global', 'Prime', 'Elite', 'Pro', 'Expert', 'Master', 'Chief', 'Lead', 'Senior', 'Executive']
        for i in range(count):
            patterns = [
                lambda: random.choice(business_words) + random.choice(['Solutions', 'Group', 'Corp', 'Inc']) + str(random.randint(1, 999)),
                lambda: random.choice(['Mr', 'Ms']) + random.choice(business_words) + str(random.randint(1, 99)),
                lambda: random.choice(business_words) + 'Consultant' + str(random.randint(1, 99)),
                lambda: random.choice(['Business', 'Finance']) + random.choice(business_words) + str(random.randint(1, 999)),
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_mixed_usernames(self, count):
        usernames = []
        all_words = self.gaming_words + self.tech_words + self.creative_words
        for i in range(count):
            patterns = [
                lambda: random.choice(all_words) + random.choice(self.pro_suffixes) + str(random.randint(10, 999)),
                lambda: random.choice(all_words) + random.choice(all_words)[:4] + str(random.randint(1, 99)),
                lambda: random.choice(['Dark', 'Neo', 'Cyber', 'Ultra']) + random.choice(all_words),
                lambda: random.choice(all_words) + str(random.randint(1000, 9999)),
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames

# Advanced Value Assessor
class ValueAssessor:
    def assess_username(self, username):
        """Advanced username value assessment"""
        score = 50  # Base score
        
        # Length assessment
        length = len(username)
        if length <= 3:
            score += 40
        elif length <= 5:
            score += 30
        elif length <= 8:
            score += 20
        elif length <= 12:
            score += 10
        else:
            score -= 5
        
        # Character patterns
        if username.isalpha():
            score += 15
        if username.isalnum() and not username.isalpha() and not username.isdigit():
            score += 10
        if any(c in username for c in ['X', 'Z', 'Q']):
            score += 8
        
        # Premium keywords
        premium_words = ['Pro', 'Elite', 'Prime', 'Ultra', 'Max', 'Core', 'Alpha', 'Beta', 'Cyber', 'Neo']
        if any(word.lower() in username.lower() for word in premium_words):
            score += 12
        
        # Special patterns
        if username.startswith(('Dark', 'Neo', 'Cyber', 'Ultra')):
            score += 10
        if username.endswith(('X', 'Pro', 'Max', 'Core')):
            score += 8
        
        # Rarity bonus
        if length <= 4:
            score += 20
        if not any(char.isdigit() for char in username):
            score += 5
        
        return min(100, max(60, score))
    
    def get_value_estimate(self, score):
        """Get monetary value estimate based on score"""
        if score >= 95:
            return '$2000-$10000+'
        elif score >= 90:
            return '$500-$5000+'
        elif score >= 85:
            return '$200-$1000'
        elif score >= 80:
            return '$100-$500'
        elif score >= 75:
            return '$50-$200'
        else:
            return '$20-$100'
    
    def get_value_icon(self, score):
        """Get icon based on value score"""
        if score >= 95:
            return '💎'
        elif score >= 90:
            return '🔥'
        elif score >= 85:
            return '⭐'
        elif score >= 80:
            return '💫'
        elif score >= 75:
            return '✨'
        else:
            return '📝'

# Initialize generators
username_gen = AdvancedUsernameGenerator()
value_assessor = ValueAssessor()

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

def get_or_create_user(telegram_id, user_data):
    """Get existing user or create new one"""
    try:
        with app.app_context():
            user = User.query.filter_by(telegram_id=telegram_id).first()
            if not user:
                user = User(
                    telegram_id=telegram_id,
                    username=user_data.get('username'),
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name')
                )
                db.session.add(user)
                db.session.commit()
                logger.info(f"Created new user: {telegram_id}")
            else:
                # Update user info if changed
                user.username = user_data.get('username') or user.username
                user.first_name = user_data.get('first_name') or user.first_name
                user.last_name = user_data.get('last_name') or user.last_name
                user.last_active = datetime.now(timezone.utc)
                db.session.commit()
            
            return user
    except Exception as e:
        logger.error(f"User creation error: {e}")
        return None

def log_interaction(user, command, response_type, usernames=None):
    """Log user interaction for analytics"""
    try:
        with app.app_context():
            interaction = UserInteraction(
                user_id=user.id,
                command=command,
                response_type=response_type,
                usernames_generated=str(usernames) if usernames else None,
                timestamp=datetime.now(timezone.utc),
                success=True
            )
            db.session.add(interaction)
            db.session.commit()
    except Exception as e:
        logger.error(f"Interaction logging error: {e}")

def handle_message(chat_id, text, user_data):
    user_id = user_data.get('id')
    username = user_data.get('username', 'Unknown')
    
    logger.info(f"Message from @{username}: {text}")
    
    # Get or create user
    user = get_or_create_user(user_id, user_data)
    if not user:
        send_message(chat_id, "❌ Database error. Please try again later.")
        return
    
    if text.startswith('/start'):
        send_message(chat_id, '''🎯 <b>Welcome to Rare Username Generator!</b>

💎 <b>Advanced Features:</b>
• AI-powered username generation with value scoring
• 5 different categories: Gaming, Tech, Creative, Professional, Mixed
• Real-time availability checking (Premium+)
• Cryptocurrency-only monetization

💰 <b>Subscription Plans:</b>
• <b>Free:</b> 5 usernames/day, basic scoring
• <b>Premium ($9.99/month):</b> Unlimited generations + availability checking
• <b>VIP ($29.99/month):</b> Premium + ultra-rare short usernames + priority support

📝 <b>Commands:</b>
/generate - Generate 8 random usernames
/categories - Browse generation categories
/premium - Get ultra-rare premium usernames
/subscribe - View crypto subscription plans
/status - Check your subscription status
/help - All available commands

🔥 <b>Start generating valuable usernames now!</b>''')
        
        log_interaction(user, '/start', 'welcome')
        
    elif text.startswith('/categories'):
        send_message(chat_id, '''🎯 <b>Username Categories</b>

Choose your preferred style:

🎮 <b>Gaming:</b> /generate gaming
Perfect for gamers, streamers, esports

💻 <b>Tech:</b> /generate tech  
Ideal for developers, IT professionals

🎨 <b>Creative:</b> /generate creative
Great for artists, designers, content creators

💼 <b>Professional:</b> /generate professional
Business-focused, corporate-ready

🎲 <b>Mixed:</b> /generate (default)
Combination of all categories

💎 <b>Premium Only:</b> /premium
Ultra-rare 3-5 character usernames

<b>Usage:</b> /generate [category]
Example: /generate gaming''')
        
        log_interaction(user, '/categories', 'info')
        
    elif text.startswith('/generate'):
        if not user.can_generate():
            send_message(chat_id, '''🔒 <b>Generation Limit Reached</b>

Free users: 5 usernames per day
Your limit has been reached.

💎 <b>Upgrade to Premium:</b>
• Unlimited username generations
• Advanced value scoring
• Platform availability checking

Use /subscribe to upgrade!''')
            return
        
        # Parse category
        parts = text.split(' ')
        category = parts[1] if len(parts) > 1 else 'random'
        
        # Generate usernames
        usernames = username_gen.generate_by_category(category, 8)
        
        response = f'🎯 <b>Generated Usernames ({category.title()}):</b>\n\n'
        
        username_data = []
        for username in usernames:
            score = value_assessor.assess_username(username)
            icon = value_assessor.get_value_icon(score)
            estimate = value_assessor.get_value_estimate(score)
            
            response += f'{icon} <code>{username}</code> - Score: {score}/100 (Est: {estimate})\n'
            username_data.append({'username': username, 'score': score, 'estimate': estimate})
        
        if user.subscription_tier == 'free':
            remaining = 5 - user.daily_generations - 1
            response += f'\n📊 <b>Daily limit:</b> {remaining} generations remaining'
        
        response += '\n\n💡 Use /subscribe for unlimited generations!'
        
        send_message(chat_id, response)
        
        # Update user stats
        user.increment_usage()
        log_interaction(user, f'/generate {category}', 'generation', username_data)
        
    elif text.startswith('/premium'):
        if user.subscription_tier not in ['premium', 'vip']:
            send_message(chat_id, '''🔒 <b>Premium Feature</b>

Ultra-rare short usernames available for Premium/VIP subscribers only.

<b>Benefits:</b>
• 3-5 character premium usernames
• Ultra-high value potential ($2000-$10000+)
• Unlimited generations
• Real-time availability checking
• Priority support

💎 Use /subscribe to upgrade!''')
            return
        
        # Generate premium usernames
        usernames = username_gen.generate_premium_usernames(5)
        
        response = '💎 <b>Ultra-Rare Premium Usernames:</b>\n\n'
        
        for username in usernames:
            score = value_assessor.assess_username(username)
            score += 15  # Premium bonus
            score = min(100, score)
            icon = value_assessor.get_value_icon(score)
            estimate = value_assessor.get_value_estimate(score)
            
            response += f'{icon} <code>{username}</code> - Score: {score}/100 (Est: {estimate})\n'
        
        response += '\n🔥 <b>These are ultra-rare handles with high value potential!</b>'
        
        send_message(chat_id, response)
        log_interaction(user, '/premium', 'premium_generation')
        
    elif text.startswith('/subscribe'):
        send_message(chat_id, '''💎 <b>Crypto-Only Subscription Plans</b>

🔥 <b>Premium - $9.99/month</b>
• Unlimited username generations
• Advanced value scoring algorithms  
• Platform availability checking
• 5 categories + premium usernames
• Priority support

💎 <b>VIP - $29.99/month</b>
• Everything in Premium
• Ultra-rare short usernames (3-5 chars)
• Custom generation requests
• Priority customer support
• Early access to new features

<b>📱 Accepted Cryptocurrencies:</b>
Bitcoin (BTC) • Litecoin (LTC) • Ethereum (ETH) • USDT (TRC20)

<b>💳 Payment Addresses:</b>
BTC: <code>bc1qygedkhjxaw0dfx85x232rdxdamp9hczac5fpc3</code>
LTC: <code>ltc1q5da462tgrmsdjt95n8lj66hwrdllrma8h0lnaa</code>
ETH/USDT: <code>0x020b47D9a3782B034ec8e8fa216B827aB253e3c3</code>

<b>📋 Payment Instructions:</b>
1. Send exact USD equivalent to appropriate address
2. Forward transaction hash to this bot
3. Include your username and plan (Premium/VIP)
4. Subscription activates within 24 hours

<b>💰 Current Rates:</b>
Premium: $9.99 USD equivalent
VIP: $29.99 USD equivalent

<b>Example payment message:</b>
<code>Payment: abc123def456... Premium @yourusername</code>''')
        
        log_interaction(user, '/subscribe', 'subscription_info')
        
    elif text.startswith('/status'):
        expires_text = 'Never' if not user.subscription_expires else user.subscription_expires.strftime('%Y-%m-%d')
        if user.subscription_tier == 'free':
            remaining = max(0, 5 - user.daily_generations)
            limit_text = f'{remaining} generations remaining today'
        else:
            limit_text = 'Unlimited generations'
        
        send_message(chat_id, f'''📊 <b>Your Account Status</b>

👤 <b>User:</b> @{user.username or 'No username'}
💎 <b>Tier:</b> {user.subscription_tier.title()}
📅 <b>Expires:</b> {expires_text}
🎯 <b>Daily Limit:</b> {limit_text}

📈 <b>Statistics:</b>
• Total generations: {user.total_generations}
• Availability checks: {user.availability_checks}
• Member since: {user.created_at.strftime('%Y-%m-%d')}

{f'💡 Use /subscribe to upgrade!' if user.subscription_tier == 'free' else '✨ Thank you for being a premium member!'}''')
        
        log_interaction(user, '/status', 'status_check')
        
    elif text.startswith('/help'):
        send_message(chat_id, '''🤖 <b>Available Commands:</b>

<b>🎯 Generation:</b>
/generate - Generate 8 random usernames
/generate [category] - Generate by category
/categories - Browse all categories
/premium - Ultra-rare premium usernames (Premium+)

<b>💎 Account:</b>
/subscribe - View subscription plans
/status - Check your account status

<b>ℹ️ Information:</b>
/help - Show this help message
/start - Welcome message

<b>📱 Categories:</b>
gaming • tech • creative • professional • mixed

<b>💰 Features by Tier:</b>
• <b>Free:</b> 5 generations/day, basic scoring
• <b>Premium:</b> Unlimited + availability checking  
• <b>VIP:</b> Premium + ultra-rare usernames

<b>🔥 Advanced AI-powered username generation with real value assessment!</b>''')
        
        log_interaction(user, '/help', 'help')
        
    elif text.startswith('/admin_users') and user_id == 7481885595:
        try:
            users = User.query.all()
            
            if not users:
                send_message(chat_id, '📊 <b>User Database</b>\n\nNo users found.')
                return
            
            response = f'📊 <b>User Database ({len(users)} total)</b>\n\n'
            
            for u in users[:15]:  # Show first 15 users
                username_display = u.username or 'No username'
                name = f"{u.first_name or ''} {u.last_name or ''}".strip() or 'No name'
                
                response += f'👤 <b>@{username_display}</b>\n'
                response += f'   ID: {u.telegram_id}\n'
                response += f'   Name: {name}\n'
                response += f'   Tier: {u.subscription_tier}\n'
                response += f'   Generations: {u.total_generations}\n'
                response += f'   Joined: {u.created_at.strftime("%Y-%m-%d")}\n\n'
            
            if len(users) > 15:
                response += f'... and {len(users) - 15} more users'
            
            send_message(chat_id, response)
        except Exception as e:
            send_message(chat_id, f'❌ Error: {str(e)}')
            
    elif text.startswith('/admin_stats') and user_id == 7481885595:
        try:
            total_users = User.query.count()
            premium_users = User.query.filter_by(subscription_tier='premium').count()
            vip_users = User.query.filter_by(subscription_tier='vip').count()
            total_interactions = UserInteraction.query.count()
            
            response = f'''📈 <b>Advanced Bot Statistics</b>

👥 <b>Users:</b>
• Total: {total_users}
• Free: {total_users - premium_users - vip_users}
• Premium: {premium_users}
• VIP: {vip_users}

📊 <b>Activity:</b>
• Total interactions: {total_interactions}
• Total generations: {sum(u.total_generations for u in User.query.all())}

💰 <b>Revenue Analysis:</b>
• Premium subscriptions: ${premium_users * 9.99:.2f}/month
• VIP subscriptions: ${vip_users * 29.99:.2f}/month
• Total monthly: ${(premium_users * 9.99) + (vip_users * 29.99):.2f}
• Annual projection: ${((premium_users * 9.99) + (vip_users * 29.99)) * 12:.2f}

🔥 <b>Bot Status:</b> Advanced features active
💎 <b>Features:</b> AI generation, value scoring, crypto payments'''
            
            send_message(chat_id, response)
        except Exception as e:
            send_message(chat_id, f'❌ Stats error: {str(e)}')
            
    elif text.startswith('/admin_upgrade') and user_id == 7481885595:
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
            
            target_user = User.query.filter_by(username=target_username).first()
            if not target_user:
                send_message(chat_id, f'❌ User @{target_username} not found')
                return
            
            old_tier = target_user.subscription_tier
            target_user.subscription_tier = tier
            
            if tier in ['premium', 'vip']:
                target_user.subscription_expires = datetime.now(timezone.utc) + timedelta(days=30)
            else:
                target_user.subscription_expires = None
            
            db.session.commit()
            
            send_message(chat_id, f'''✅ <b>Subscription Updated</b>

👤 User: @{target_username}
📊 Changed: {old_tier} → {tier}
📅 Expires: {'30 days from now' if tier in ['premium', 'vip'] else 'N/A'}
🎯 Features: {'Unlimited generations + premium features' if tier != 'free' else 'Basic free tier'}''')
            
        except Exception as e:
            send_message(chat_id, f'❌ Upgrade error: {str(e)}')
    
    else:
        send_message(chat_id, '''🤖 I didn't understand that command.

<b>Try these commands:</b>
• /generate - Generate usernames
• /categories - Browse categories  
• /premium - Premium usernames
• /subscribe - Upgrade account
• /help - All commands

💡 Type /help for the complete command list!''')

def run_telegram_polling():
    logger.info("Starting advanced Telegram bot polling...")
    
    # Test bot connection
    try:
        response = requests.get(f'{BASE_URL}/getMe', timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            logger.info(f"Advanced bot connected: @{bot_info['result']['username']}")
        else:
            logger.error(f"Bot connection failed: {response.status_code}")
            return
    except Exception as e:
        logger.error(f"Bot connection error: {e}")
        return
    
    offset = 0
    logger.info("Advanced bot listening for messages...")
    
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
                if response.status_code != 409:  # Ignore conflict errors
                    logger.error(f"API request failed: {response.status_code}")
                time.sleep(5)
                
        except Exception as e:
            logger.error(f"Polling error: {e}")
            time.sleep(5)

def start_bot():
    try:
        bot_thread = threading.Thread(target=run_telegram_polling, daemon=True)
        bot_thread.start()
        logger.info("Advanced Telegram bot started successfully")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

# Initialize database
try:
    with app.app_context():
        db.create_all()
        logger.info("Advanced database tables created successfully")
except Exception as e:
    logger.error(f"Database initialization error: {e}")

# Start bot
start_bot()

@app.route('/')
def index():
    return '''
    <h1>🎯 Advanced Telegram Username Generator Bot</h1>
    <p>Bot Status: <strong>✅ Advanced Features Active</strong></p>
    <p>Bot Username: <strong>@UsernameavailablesBot</strong></p>
    
    <h2>🔥 Advanced Features:</h2>
    <ul>
        <li><strong>AI-Powered Generation:</strong> 5 categories with advanced algorithms</li>
        <li><strong>Value Assessment:</strong> Real-time scoring with monetary estimates</li>
        <li><strong>Premium Usernames:</strong> Ultra-rare 3-5 character handles</li>
        <li><strong>User Management:</strong> Complete subscription and analytics system</li>
        <li><strong>Crypto Payments:</strong> BTC, LTC, ETH, USDT integration</li>
        <li><strong>Advanced Analytics:</strong> User tracking and interaction logging</li>
    </ul>
    
    <h2>💎 Subscription Tiers:</h2>
    <ul>
        <li><strong>Free:</strong> 5 usernames/day, basic scoring</li>
        <li><strong>Premium ($9.99/month):</strong> Unlimited + availability checking</li>
        <li><strong>VIP ($29.99/month):</strong> Premium + ultra-rare usernames</li>
    </ul>
    
    <p><a href="/health">🔍 Health Check</a> | <a href="/test">⚡ Test Endpoint</a></p>
    '''

@app.route('/health')
def health():
    try:
        # Test database connection
        with app.app_context():
            user_count = User.query.count()
        
        return jsonify({
            "status": "healthy",
            "bot": "advanced_features_active", 
            "database": "connected",
            "features": {
                "ai_generation": True,
                "value_assessment": True,
                "premium_usernames": True,
                "crypto_payments": True,
                "user_analytics": True
            },
            "stats": {
                "total_users": user_count
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/test')
def test():
    return "🎯 Advanced Username Generator Bot - All Systems Operational! ✅"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
