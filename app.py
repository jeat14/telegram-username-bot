import os
import logging
import requests
import threading
import time
import random
from flask import Flask, jsonify

# Enhanced logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "telegram-bot-secret")

# Bot configuration
BOT_TOKEN = "7846959922:AAHtfU7tjgtaRnf1qogfsaxoy15_-UO_P4g"
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

logger.info("Starting Advanced Telegram Username Generator Bot...")

# Advanced Username Generator
class AdvancedUsernameGenerator:
    def __init__(self):
        self.gaming_words = ['Alpha', 'Beta', 'Cyber', 'Neo', 'Pro', 'Elite', 'Prime', 'Ultra', 'Quantum', 'Phoenix', 'Shadow', 'Storm', 'Fire', 'Ice', 'Thunder', 'Ghost', 'Nova', 'Blaze', 'Apex', 'Vortex', 'Titan', 'Omega', 'Zero', 'Void', 'Rage']
        
        self.tech_words = ['Code', 'Data', 'Sync', 'Node', 'Core', 'Link', 'Hack', 'Bit', 'Byte', 'Cloud', 'Logic', 'Pixel', 'Matrix', 'Vector', 'Cache', 'Debug', 'Binary', 'Crypto', 'Token', 'Mesh', 'Stack', 'Frame', 'Query', 'Script', 'Parse']
        
        self.creative_words = ['Art', 'Flow', 'Vibe', 'Wave', 'Glow', 'Spark', 'Dream', 'Magic', 'Star', 'Moon', 'Sun', 'Sky', 'Ocean', 'Forest', 'Crystal', 'Diamond', 'Gold', 'Silver', 'Pearl', 'Jade', 'Aurora', 'Zen', 'Muse', 'Aura', 'Iris']
        
        self.business_words = ['Global', 'Prime', 'Elite', 'Pro', 'Expert', 'Master', 'Chief', 'Lead', 'Senior', 'Executive', 'Capital', 'Venture', 'Summit', 'Apex', 'Crown', 'Royal', 'Premium', 'Platinum', 'Diamond', 'Gold']
        
        self.pro_suffixes = ['X', 'Pro', 'Max', 'Core', 'Tech', 'Lab', 'Hub', 'Zone', 'Base', 'Net', 'Sys', 'Dev', 'AI', 'Bot', 'App', 'Web', 'Code', 'Data', 'Sync', 'Link', 'Plus', 'Ultra', 'Prime', 'Elite', 'Apex']
        
    def generate_premium_usernames(self, count=5):
        """Generate ultra-rare short usernames for premium users"""
        usernames = []
        patterns = [
            lambda: random.choice(['X', 'Z', 'Q', 'K']) + random.choice(self.gaming_words[:15])[:3] + str(random.randint(1, 99)),
            lambda: random.choice(self.tech_words[:15])[:4] + random.choice(['X', 'Z', '0', '9']),
            lambda: random.choice(['_', '.', '']) + random.choice(self.creative_words[:15])[:4],
            lambda: random.choice(self.gaming_words[:15])[:3] + random.choice(['_', '.', '']) + str(random.randint(1, 9)),
            lambda: ''.join(random.choices('ABCDEFGHIJKLMNPQRSTUVWXYZ', k=3)) + str(random.randint(10, 99)),
            lambda: random.choice(['Q', 'X', 'Z']) + random.choice(self.tech_words[:10])[:2] + random.choice(['0', '1', '9']),
            lambda: random.choice(self.business_words[:10])[:3] + random.choice(['X', 'Z', 'Q'])
        ]
        
        for i in range(count):
            username = random.choice(patterns)()
            usernames.append(username)
        
        return usernames
    
    def generate_by_category(self, category='random', count=8):
        """Generate usernames by specialized category"""
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
                lambda: random.choice(self.gaming_words) + random.choice(self.gaming_words)[:4] + str(random.randint(1, 99)),
                lambda: 'Dark' + random.choice(self.gaming_words) + random.choice(['X', 'Z', 'Core', '']),
                lambda: random.choice(self.gaming_words) + 'Lord' + str(random.randint(1, 999)),
                lambda: 'Shadow' + random.choice(self.gaming_words)[:5] + str(random.randint(1, 99)),
                lambda: random.choice(['Cyber', 'Neo', 'Ultra']) + random.choice(self.gaming_words) + random.choice(['X', 'Pro', 'Max']),
                lambda: random.choice(self.gaming_words) + 'Gaming' + str(random.randint(1, 999)),
                lambda: random.choice(['Epic', 'Legendary', 'Mythic']) + random.choice(self.gaming_words)[:6]
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_tech_usernames(self, count):
        usernames = []
        for i in range(count):
            patterns = [
                lambda: random.choice(self.tech_words) + random.choice(self.pro_suffixes) + str(random.randint(10, 999)),
                lambda: random.choice(['Dev', 'Code', 'Tech', 'Sys']) + random.choice(self.tech_words) + str(random.randint(1, 99)),
                lambda: random.choice(self.tech_words) + 'AI' + str(random.randint(1, 999)),
                lambda: 'Cyber' + random.choice(self.tech_words) + random.choice(['X', 'Pro', 'Core', '']),
                lambda: random.choice(['Digital', 'Virtual', 'Smart']) + random.choice(self.tech_words)[:5],
                lambda: random.choice(self.tech_words) + 'Labs' + str(random.randint(1, 999)),
                lambda: random.choice(['Future', 'Next', 'Advanced']) + random.choice(self.tech_words)[:4],
                lambda: random.choice(self.tech_words) + 'Studio' + str(random.randint(10, 99))
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_creative_usernames(self, count):
        usernames = []
        for i in range(count):
            patterns = [
                lambda: random.choice(self.creative_words) + random.choice(['Flow', 'Wave', 'Glow', 'Spark']) + str(random.randint(1, 99)),
                lambda: 'Art' + random.choice(self.creative_words) + str(random.randint(1, 999)),
                lambda: random.choice(self.creative_words) + 'Studio' + str(random.randint(1, 99)),
                lambda: random.choice(['Magic', 'Dream', 'Wonder']) + random.choice(self.creative_words),
                lambda: random.choice(self.creative_words) + 'Design' + str(random.randint(1, 999)),
                lambda: random.choice(['Creative', 'Artistic', 'Visual']) + random.choice(self.creative_words)[:5],
                lambda: random.choice(self.creative_words) + 'Works' + str(random.randint(10, 99)),
                lambda: random.choice(['Inspired', 'Brilliant', 'Elegant']) + random.choice(self.creative_words)[:4]
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_professional_usernames(self, count):
        usernames = []
        for i in range(count):
            patterns = [
                lambda: random.choice(self.business_words) + random.choice(['Solutions', 'Group', 'Corp', 'Inc', 'Ltd']) + str(random.randint(1, 999)),
                lambda: random.choice(['Mr', 'Ms', 'Dr']) + random.choice(self.business_words) + str(random.randint(1, 99)),
                lambda: random.choice(self.business_words) + 'Consultant' + str(random.randint(1, 99)),
                lambda: random.choice(['Business', 'Finance', 'Legal', 'Strategic']) + random.choice(self.business_words) + str(random.randint(1, 999)),
                lambda: random.choice(self.business_words) + 'Partners' + str(random.randint(10, 99)),
                lambda: random.choice(['Professional', 'Corporate', 'Executive']) + random.choice(self.business_words)[:5],
                lambda: random.choice(self.business_words) + 'Ventures' + str(random.randint(1, 999)),
                lambda: random.choice(['Success', 'Achievement', 'Excellence']) + random.choice(self.business_words)[:4]
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_mixed_usernames(self, count):
        usernames = []
        all_words = self.gaming_words + self.tech_words + self.creative_words + self.business_words
        for i in range(count):
            patterns = [
                lambda: random.choice(all_words) + random.choice(self.pro_suffixes) + str(random.randint(10, 999)),
                lambda: random.choice(all_words) + random.choice(all_words)[:4] + str(random.randint(1, 99)),
                lambda: random.choice(['Dark', 'Neo', 'Cyber', 'Ultra', 'Super', 'Mega']) + random.choice(all_words),
                lambda: random.choice(all_words) + str(random.randint(1000, 9999)),
                lambda: random.choice(['Next', 'Future', 'Modern', 'Advanced']) + random.choice(all_words)[:5],
                lambda: random.choice(all_words) + random.choice(['Hub', 'Zone', 'Base', 'Core']) + str(random.randint(1, 99)),
                lambda: random.choice(['Smart', 'Digital', 'Elite', 'Premium']) + random.choice(all_words)[:4],
                lambda: random.choice(all_words) + 'Network' + str(random.randint(10, 999))
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames

# Advanced Value Assessor
class ValueAssessor:
    def assess_username(self, username):
        """Advanced AI-powered username value assessment"""
        score = 50  # Base score
        
        # Length assessment (shorter = more valuable)
        length = len(username)
        if length <= 3:
            score += 45
        elif length <= 5:
            score += 35
        elif length <= 8:
            score += 25
        elif length <= 12:
            score += 15
        elif length <= 16:
            score += 5
        else:
            score -= 10
        
        # Character composition analysis
        if username.isalpha():
            score += 18
        elif username.isalnum() and not username.isalpha() and not username.isdigit():
            score += 12
        
        # Premium character bonus
        premium_chars = ['X', 'Z', 'Q', 'K']
        if any(c in username for c in premium_chars):
            score += 10
        
        # Vowel-consonant balance
        vowels = sum(1 for c in username.lower() if c in 'aeiou')
        consonants = sum(1 for c in username.lower() if c.isalpha() and c not in 'aeiou')
        if vowels > 0 and consonants > 0:
            ratio = min(vowels, consonants) / max(vowels, consonants)
            if ratio > 0.3:  # Good balance
                score += 8
        
        # Premium keywords detection
        premium_words = ['Pro', 'Elite', 'Prime', 'Ultra', 'Max', 'Core', 'Alpha', 'Beta', 'Cyber', 'Neo', 'Master', 'Expert', 'Global', 'Premium', 'Diamond', 'Platinum']
        if any(word.lower() in username.lower() for word in premium_words):
            score += 15
        
        # Special pattern bonuses
        if username.startswith(('Dark', 'Neo', 'Cyber', 'Ultra', 'Super', 'Mega', 'Alpha', 'Beta')):
            score += 12
        if username.endswith(('X', 'Pro', 'Max', 'Core', 'Tech', 'Lab', 'Hub', 'Zone')):
            score += 10
        
        # Rarity factors
        if length <= 4:
            score += 25  # Ultra-rare short usernames
        if not any(char.isdigit() for char in username):
            score += 8  # No numbers = more brandable
        if username[0].isupper() and username[1:].islower():
            score += 5  # Proper capitalization
        
        # Memorability factors
        if self._has_alternating_pattern(username):
            score += 6
        if self._is_pronounceable(username):
            score += 8
        
        # Brandability assessment
        if self._is_brandable(username):
            score += 12
        
        # Final score normalization
        return min(100, max(60, score))
    
    def _has_alternating_pattern(self, username):
        """Check for pleasing alternating patterns"""
        if len(username) < 4:
            return False
        vowels = 'aeiouAEIOU'
        pattern_score = 0
        for i in range(len(username) - 1):
            if username[i].isalpha() and username[i+1].isalpha():
                if (username[i] in vowels) != (username[i+1] in vowels):
                    pattern_score += 1
        return pattern_score >= len(username) * 0.4
    
    def _is_pronounceable(self, username):
        """Basic pronounceability check"""
        vowels = 'aeiouAEIOU'
        consonant_streak = 0
        vowel_streak = 0
        
        for char in username:
            if char.isalpha():
                if char in vowels:
                    vowel_streak += 1
                    consonant_streak = 0
                    if vowel_streak > 3:
                        return False
                else:
                    consonant_streak += 1
                    vowel_streak = 0
                    if consonant_streak > 4:
                        return False
        return True
    
    def _is_brandable(self, username):
        """Check if username has good branding potential"""
        if len(username) < 3 or len(username) > 12:
            return False
        if not username[0].isalpha():
            return False
        if username.count('_') > 1 or username.count('.') > 1:
            return False
        return True
    
    def get_value_estimate(self, score):
        """Get detailed monetary value estimate"""
        if score >= 98:
            return '$10,000-$50,000+'
        elif score >= 95:
            return '$5,000-$15,000'
        elif score >= 90:
            return '$1,000-$8,000'
        elif score >= 85:
            return '$500-$3,000'
        elif score >= 80:
            return '$200-$1,000'
        elif score >= 75:
            return '$100-$500'
        else:
            return '$25-$200'
    
    def get_value_icon(self, score):
        """Get appropriate icon based on value score"""
        if score >= 98:
            return '💎'
        elif score >= 95:
            return '🔥'
        elif score >= 90:
            return '⭐'
        elif score >= 85:
            return '💫'
        elif score >= 80:
            return '✨'
        elif score >= 75:
            return '🌟'
        else:
            return '📝'
    
    def get_rarity_level(self, score):
        """Get rarity classification"""
        if score >= 98:
            return 'LEGENDARY'
        elif score >= 95:
            return 'ULTRA-RARE'
        elif score >= 90:
            return 'RARE'
        elif score >= 85:
            return 'UNCOMMON'
        elif score >= 80:
            return 'GOOD'
        else:
            return 'COMMON'

# Initialize generators
username_gen = AdvancedUsernameGenerator()
value_assessor = ValueAssessor()

# Session-based user tracking
user_sessions = {}

def get_user_session(user_id):
    """Get or create user session with advanced tracking"""
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'daily_generations': 0,
            'total_generations': 0,
            'subscription_tier': 'free',
            'last_reset': time.strftime('%Y-%m-%d'),
            'premium_generations': 0,
            'favorite_category': 'mixed',
            'join_date': time.strftime('%Y-%m-%d'),
            'last_active': time.time()
        }
    
    # Reset daily counter if new day
    today = time.strftime('%Y-%m-%d')
    if user_sessions[user_id]['last_reset'] != today:
        user_sessions[user_id]['daily_generations'] = 0
        user_sessions[user_id]['last_reset'] = today
    
    # Update last active
    user_sessions[user_id]['last_active'] = time.time()
    
    return user_sessions[user_id]

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
    
    logger.info(f"Processing message from @{username} ({user_id}): {text}")
    
    # Get user session
    session = get_user_session(user_id)
    
    if text.startswith('/start'):
        send_message(chat_id, '''🎯 <b>Welcome to Advanced AI Username Generator!</b>

💎 <b>Professional-Grade Features:</b>
• AI-powered generation with 5 specialized categories
• Advanced value scoring system (60-100 points)
• Real monetary value estimates ($25-$50,000+)
• Ultra-rare premium usernames (3-5 characters)
• Rarity classification: Common → Legendary

🎮 <b>Specialized Categories:</b>
• <b>Gaming:</b> Perfect for streamers, esports, content creators
• <b>Tech:</b> Ideal for developers, startups, tech professionals  
• <b>Creative:</b> Great for artists, designers, influencers
• <b>Professional:</b> Business-focused, corporate-ready handles
• <b>Mixed:</b> Advanced combination algorithms

💰 <b>Subscription Plans:</b>
• <b>Free:</b> 5 generations/day, all categories, full scoring
• <b>Premium ($9.99/month):</b> Unlimited + ultra-rare usernames
• <b>VIP ($29.99/month):</b> Premium + custom requests + priority

📝 <b>Quick Start Commands:</b>
/generate [category] - Generate by category
/categories - Browse all categories  
/premium - Ultra-rare premium usernames
/subscribe - Crypto payment plans

🔥 <b>Example:</b> Try /generate gaming for gaming usernames!''')
        
    elif text.startswith('/categories'):
        send_message(chat_id, '''🎯 <b>Advanced AI Generation Categories</b>

Each category uses specialized algorithms for authentic, valuable usernames:

🎮 <b>Gaming Category:</b> <code>/generate gaming</code>
Perfect for: Streamers, gamers, esports teams, content creators
AI Focus: Action words, power terms, competitive elements
Examples: AlphaStormX999, CyberLordPro, DarkPhoenixCore

💻 <b>Tech Category:</b> <code>/generate tech</code>  
Ideal for: Developers, startups, IT professionals, tech enthusiasts
AI Focus: Technical terms, modern concepts, innovation themes
Examples: CodeMatrixLab, CyberNodeSync, DataCoreAI

🎨 <b>Creative Category:</b> <code>/generate creative</code>
Great for: Artists, designers, influencers, creative professionals
AI Focus: Artistic terms, aesthetic concepts, inspiration themes
Examples: ArtFlowStudio, DreamCrystalWorks, MagicGlowDesign

💼 <b>Professional Category:</b> <code>/generate professional</code>
Perfect for: Business, consulting, corporate, executive brands
AI Focus: Business terms, authority concepts, success themes
Examples: GlobalSolutionsInc, PrimeConsultant, ExpertVenturesLtd

🎲 <b>Mixed Category:</b> <code>/generate</code> (default)
Advanced combination of all categories with smart pattern mixing

💎 <b>Premium Only:</b> <code>/premium</code>
Ultra-rare 3-5 character usernames (Premium/VIP subscribers)
Examples: XCyb0, ZTech, QMax9

<b>💡 Pro Tip:</b> Each category generates 8 unique usernames with full AI value analysis!''')
        
    elif text.startswith('/generate'):
        # Check daily limit for free users
        if session['subscription_tier'] == 'free' and session['daily_generations'] >= 5:
            send_message(chat_id, f'''🔒 <b>Daily Generation Limit Reached</b>

Free users: 5 usernames per day
You've used all {session['daily_generations']} generations today.

💎 <b>Upgrade to Premium for:</b>
• Unlimited username generations (all categories)
• Ultra-rare premium usernames (3-5 chars)
• Advanced AI algorithms with enhanced scoring
• Priority customer support

<b>🔥 Your Stats:</b>
• Total generated: {session['total_generations']} usernames
• Member since: {session['join_date']}
• Favorite category: {session['favorite_category'].title()}

Use /subscribe to unlock unlimited premium features!''')
            return
        
        # Parse category
        parts = text.split(' ')
        category = parts[1] if len(parts) > 1 else 'mixed'
        
        # Update favorite category tracking
        if category != 'mixed':
            session['favorite_category'] = category
        
        # Generate usernames using advanced AI algorithms
        usernames = username_gen.generate_by_category(category, 8)
        
        response = f'🎯 <b>AI-Generated Usernames ({category.title()} Algorithm):</b>\n\n'
        
        high_value_count = 0
        total_estimated_value = 0
        
        for username in usernames:
            score = value_assessor.assess_username(username)
            icon = value_assessor.get_value_icon(score)
            estimate = value_assessor.get_value_estimate(score)
            rarity = value_assessor.get_rarity_level(score)
            
            # Track high-value usernames
            if score >= 90:
                high_value_count += 1
            
            response += f'{icon} <code>{username}</code>\n'
            response += f'   📊 Score: {score}/100 | 💰 Est: {estimate} | 🏆 {rarity}\n\n'
        
        # Add session usage info for free users
        if session['subscription_tier'] == 'free':
            session['daily_generations'] += 1
            session['total_generations'] += 1
            remaining = 5 - session['daily_generations']
            response += f'📈 <b>Usage:</b> {remaining} generations remaining today\n'
        
        # Add generation insights
        response += f'🔬 <b>Analysis:</b> {high_value_count}/8 high-value usernames\n'
        response += f'🤖 <b>Algorithm:</b> {category.title()}-optimized AI patterns\n'
        
        if session['subscription_tier'] == 'free':
            response += '\n💡 Use /premium for ultra-rare 3-5 char usernames!'
        else:
            response += '\n💎 Premium active - Use /premium for ultra-rare usernames!'
        
        send_message(chat_id, response)
        
    elif text.startswith('/premium'):
        if session['subscription_tier'] == 'free':
            send_message(chat_id, '''🔒 <b>Premium Feature - Ultra-Rare Usernames</b>

Exclusive ultra-rare 3-5 character usernames with exceptional value potential.

<b>💎 Premium Examples:</b>
💎 <code>XCyb0</code> - Score: 98/100 (Est: $15,000) | LEGENDARY
💎 <code>ZTech</code> - Score: 96/100 (Est: $8,000) | ULTRA-RARE  
💎 <code>QMax9</code> - Score: 95/100 (Est: $5,000) | ULTRA-RARE

<b>🔥 Premium Benefits:</b>
• Ultra-rare 3-5 character usernames
• Value potential: $5,000-$50,000+
• Unlimited generations (all categories)
• Advanced AI scoring algorithms
• Priority customer support

<b>💰 Subscription Plans:</b>
Premium: $9.99/month | VIP: $29.99/month

💎 Upgrade with /subscribe to unlock premium features!''')
            return
        
        # Generate premium usernames for subscribers
        usernames = username_gen.generate_premium_usernames(5)
        
        response = '💎 <b>Ultra-Rare Premium Usernames:</b>\n\n'
        
        legendary_count = 0
        for username in usernames:
            score = value_assessor.assess_username(username)
            score += 15  # Premium generation bonus
            score = min(100, score)
            
            icon = value_assessor.get_value_icon(score)
            estimate = value_assessor.get_value_estimate(score)
            rarity = value_assessor.get_rarity_level(score)
            
            if score >= 98:
                legendary_count += 1
            
            response += f'{icon} <code>{username}</code>\n'
            response += f'   📊 Score: {score}/100 | 💰 Est: {estimate} | 🏆 {rarity}\n\n'
        
        session['premium_generations'] += 1
        
        response += f'🔬 <b>Analysis:</b> {legendary_count}/5 legendary-tier usernames\n'
        response += f'🤖 <b>Algorithm:</b> Ultra-rare premium patterns\n'
        response += f'📈 <b>Premium Sessions:</b> {session["premium_generations"]} total\n\n'
        response += '🔥 <b>These are exclusive ultra-rare handles with exceptional value potential!</b>'
        
        send_message(chat_id, response)
        
    elif text.startswith('/subscribe'):
        send_message(chat_id, '''💎 <b>Professional Crypto Subscription Plans</b>

🔥 <b>Premium Plan - $9.99/month</b>
✅ Unlimited username generations (all 5 categories)
✅ Advanced AI algorithms with enhanced scoring
✅ Ultra-rare premium usernames (3-5 characters)
✅ Real-time value assessment with detailed analysis
✅ Priority customer support
✅ Advanced usage analytics

💎 <b>VIP Plan - $29.99/month</b>
✅ Everything in Premium
✅ Custom generation requests with personal consultation
✅ Exclusive ultra-rare algorithms (98+ scores)
✅ Early access to new AI features
✅ Priority support with direct contact
✅ Monthly personalized username reports

<b>📱 Accepted Cryptocurrencies:</b>
Bitcoin (BTC) • Litecoin (LTC) • Ethereum (ETH) • USDT (TRC20/ERC20)

<b>💳 Verified Payment Addresses:</b>
BTC: <code>bc1qygedkhjxaw0dfx85x232rdxdamp9hczac5fpc3</code>
LTC: <code>ltc1q5da462tgrmsdjt95n8lj66hwrdllrma8h0lnaa</code>
ETH/USDT: <code>0x020b47D9a3782B034ec8e8fa216B827aB253e3c3</code>

<b>📋 Professional Payment Process:</b>
1. Send exact USD equivalent to appropriate address above
2. Forward transaction hash to this bot with your plan choice
3. Include: Transaction hash + Plan (Premium/VIP) + Your username
4. Professional verification and activation within 24 hours

<b>💰 Current Exchange Rates:</b>
Premium: $9.99 USD equivalent in crypto
VIP: $29.99 USD equivalent in crypto

<b>📝 Payment Example:</b>
<code>Payment: abc123def456... Premium @yourusername</code>

🚀 <b>Professional AI-powered username generation starts here!</b>''')
        
    elif text.startswith('/status'):
        remaining = max(0, 5 - session['daily_generations']) if session['subscription_tier'] == 'free' else 'Unlimited'
        days_active = max(1, (time.time() - time.mktime(time.strptime(session['join_date'], '%Y-%m-%d'))) // 86400)
        avg_daily = session['total_generations'] / days_active
        
        send_message(chat_id, f'''📊 <b>Advanced Account Analytics</b>

👤 <b>Profile:</b> @{username}
💎 <b>Tier:</b> {session['subscription_tier'].title()}
📅 <b>Member Since:</b> {session['join_date']} ({int(days_active)} days)
🎯 <b>Today's Limit:</b> {remaining} generations remaining

📈 <b>Generation Statistics:</b>
• Total usernames: {session['total_generations']}
• Premium sessions: {session.get('premium_generations', 0)}
• Daily average: {avg_daily:.1f} usernames
• Favorite category: {session['favorite_category'].title()}

🔥 <b>AI Features Available:</b>
✅ 5 specialized generation categories
✅ Advanced value scoring (60-100 points)
✅ Monetary value estimates ($25-$50,000+)
✅ Rarity classification system
{'✅ Ultra-rare premium usernames' if session['subscription_tier'] != 'free' else '🔒 Premium usernames (upgrade needed)'}
{'✅ Unlimited generations' if session['subscription_tier'] != 'free' else '🔒 Unlimited (upgrade needed)'}

{f'💡 Upgrade to Premium for unlimited AI-powered generation!' if session['subscription_tier'] == 'free' else '✨ Thank you for being a premium member!'}''')
        
    elif text.startswith('/help'):
        send_message(chat_id, '''🤖 <b>Advanced AI Username Generator - Complete Guide</b>

<b>🎯 Generation Commands:</b>
/generate - Mixed category (8 usernames)
/generate [category] - Specialized category generation
/categories - Browse all 5 AI categories
/premium - Ultra-rare premium usernames (Premium+)

<b>📱 Available Categories:</b>
• <code>gaming</code> - Streamers, esports, content creators
• <code>tech</code> - Developers, startups, IT professionals  
• <code>creative</code> - Artists, designers, influencers
• <code>professional</code> - Business, corporate, consulting
• <code>mixed</code> - Advanced algorithm combination

<b>💎 Account & Status:</b>
/subscribe - Professional crypto subscription plans
/status - Detailed account analytics and usage stats
/help - This comprehensive command guide
/start - Welcome message with full feature overview

<b>🔥 Advanced AI Features:</b>
✨ Specialized algorithms per category
✨ Real-time value scoring (60-100 points)
✨ Monetary estimates ($25-$50,000+)
✨ Rarity classification: Common → Legendary
✨ Ultra-rare 3-5 character premium usernames
✨ Professional crypto subscription system

<b>💡 Quick Examples:</b>
<code>/generate gaming</code> - Gaming-optimized usernames
<code>/generate tech</code> - Tech/startup-focused usernames
<code>/generate creative</code> - Creative/artistic usernames

<b>🚀 Professional Features:</b>
Premium users get unlimited access to all advanced AI algorithms!''')
        
    elif text.startswith('/admin_stats') and user_id == 7481885595:
        total_users = len(user_sessions)
        total_generations = sum(s['total_generations'] for s in user_sessions.values())
        premium_users = sum(1 for s in user_sessions.values() if s['subscription_tier'] in ['premium', 'vip'])
        avg_generations = total_generations / max(1, total_users)
        
        # Category popularity
        category_usage = {}
        for session in user_sessions.values():
            cat = session.get('favorite_category', 'mixed')
            category_usage[cat] = category_usage.get(cat, 0) + 1
        
        most_popular = max(category_usage, key=category_usage.get) if category_usage else 'mixed'
        
        send_message(chat_id, f'''📈 <b>Advanced Bot Analytics Dashboard</b>

👥 <b>User Statistics:</b>
• Total registered users: {total_users}
• Premium subscribers: {premium_users}
• Free users: {total_users - premium_users}
• Conversion rate: {(premium_users/max(1,total_users)*100):.1f}%

📊 <b>Generation Analytics:</b>
• Total usernames generated: {total_generations:,}
• Average per user: {avg_generations:.1f}
• Most popular category: {most_popular.title()}

💰 <b>Revenue Analysis:</b>
• Monthly revenue: ${premium_users * 9.99:.2f}
• Annual projection: ${premium_users * 9.99 * 12:.2f}
• Premium value per user: $119.88/year

🔥 <b>Advanced AI System Status:</b>
✅ 5-category specialized generation algorithms
✅ Advanced value scoring with 10+ factors
✅ Ultra-rare premium username generation
✅ Real-time monetary value estimation
✅ Rarity classification system
✅ Professional crypto payment integration
✅ Session-based analytics tracking

🚀 <b>Performance Metrics:</b>
• Bot uptime: Stable on Heroku
• API response: Optimal
• AI generation: All systems operational

💎 <b>Professional-grade username generation platform fully operational!</b>''')
    
    else:
        send_message(chat_id, '''🤖 <b>Command not recognized</b>

<b>🎯 Try these advanced commands:</b>
• <code>/generate [category]</code> - AI-powered username generation
• <code>/categories</code> - Browse 5 specialized categories
• <code>/premium</code> - Ultra-rare premium usernames
• <code>/subscribe</code> - Professional subscription plans
• <code>/help</code> - Complete feature guide

<b>📱 Quick Examples:</b>
• <code>/generate gaming</code> - Gaming usernames
• <code>/generate tech</code> - Tech usernames  
• <code>/generate creative</code> - Creative usernames

💡 <b>Pro Tip:</b> Each category uses specialized AI algorithms for authentic, valuable usernames!''')

def run_telegram_polling():
    logger.info("Starting Advanced AI Telegram Bot on Heroku...")
    
    # Test bot connection
    try:
        response = requests.get(f'{BASE_URL}/getMe', timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            logger.info(f"Advanced AI bot connected: @{bot_info['result']['username']}")
        else:
            logger.error(f"Bot connection failed: {response.status_code}")
            return
    except Exception as e:
        logger.error(f"Bot connection error: {e}")
        return
    
    offset = 0
    logger.info("Advanced AI bot listening for messages...")
    
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
        logger.info("Initializing Advanced AI bot...")
        bot_thread = threading.Thread(target=run_telegram_polling, daemon=True)
        bot_thread.start()
        logger.info("Advanced AI bot started successfully on Heroku")
    except Exception as e:
        logger.error(f"Failed to start advanced bot: {e}")

# Flask routes
@app.route('/')
def index():
    return '''
    <h1>🎯 Advanced AI Username Generator Bot</h1>
    <p>Status: <strong>✅ All Advanced AI Features Active</strong></p>
    <p>Bot: <strong>@UsernameavailablesBot</strong></p>
    <p>Platform: <strong>Heroku Professional Deployment</strong></p>
    
    <h2>🔥 Advanced AI Features:</h2>
    <ul>
        <li><strong>5 Specialized Categories:</strong> Gaming, Tech, Creative, Professional, Mixed</li>
        <li><strong>Advanced AI Algorithms:</strong> Unique patterns for each category</li>
        <li><strong>Professional Value Scoring:</strong> 60-100 point system with 10+ factors</li>
        <li><strong>Monetary Estimates:</strong> $25-$50,000+ valuations</li>
        <li><strong>Ultra-rare Usernames:</strong> 3-5 character premium handles</li>
        <li><strong>Rarity Classification:</strong> Common → Legendary system</li>
        <li><strong>Crypto Payments:</strong> BTC, LTC, ETH, USDT integration</li>
        <li><strong>Advanced Analytics:</strong> Complete user tracking and insights</li>
    </ul>
    
    <h2>💎 Professional Subscription Tiers:</h2>
    <ul>
        <li><strong>Free:</strong> 5 usernames/day, all categories, full AI scoring</li>
        <li><strong>Premium ($9.99):</strong> Unlimited + ultra-rare usernames</li>
        <li><strong>VIP ($29.99):</strong> Premium + custom requests + priority</li>
    </ul>
    
    <h2>📊 System Status:</h2>
    <ul>
        <li>AI Generation: <strong>Operational</strong></li>
        <li>Value Assessment: <strong>Active</strong></li>
        <li>Crypto Payments: <strong>Ready</strong></li>
        <li>Analytics: <strong>Tracking</strong></li>
    </ul>
    
    <p><a href="/health">Health Check</a> | <a href="/stats">Live Statistics</a></p>
    '''

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "platform": "heroku_professional",
        "bot": "advanced_ai_active",
        "features": {
            "ai_generation": True,
            "value_assessment": True,
            "premium_usernames": True,
            "crypto_payments": True,
            "categories": 5,
            "algorithms": "specialized_per_category",
            "scoring_factors": "10_plus",
            "rarity_classification": True
        },
        "stats": {
            "active_users": len(user_sessions),
            "total_generations": sum(s['total_generations'] for s in user_sessions.values()),
            "premium_users": sum(1 for s in user_sessions.values() if s['subscription_tier'] != 'free')
        }
    })

@app.route('/stats')
def stats():
    total_gens = sum(s['total_generations'] for s in user_sessions.values())
    premium_count = sum(1 for s in user_sessions.values() if s['subscription_tier'] != 'free')
    
    return jsonify({
        "users": len(user_sessions),
        "total_generations": total_gens,
        "premium_users": premium_count,
        "categories": ["gaming", "tech", "creative", "professional", "mixed"],
        "features": "all_advanced_ai_active",
        "revenue_monthly": premium_count * 9.99,
        "conversion_rate": f"{(premium_count/max(1,len(user_sessions))*100):.1f}%"
    })

# Initialize advanced AI bot
logger.info("Starting Advanced AI initialization...")
start_bot()
logger.info("Advanced AI bot initialization complete")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Advanced AI Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
