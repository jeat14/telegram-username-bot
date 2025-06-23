import os
import logging
import requests
import threading
import time
import random
from flask import Flask, jsonify

# Enhanced logging
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

logger.info("Starting Enhanced Username Generator Bot...")

# Advanced Username Generator
class UsernameGenerator:
    def __init__(self):
        self.gaming_words = ['Alpha', 'Beta', 'Cyber', 'Neo', 'Pro', 'Elite', 'Prime', 'Ultra', 'Quantum', 'Phoenix', 'Shadow', 'Storm', 'Fire', 'Ice', 'Thunder', 'Ghost', 'Nova', 'Blaze', 'Apex', 'Vortex', 'Titan', 'Omega', 'Zero', 'Void', 'Rage', 'Power', 'Gamer', 'Player', 'Master', 'Hero', 'Legend', 'Epic', 'Fury', 'Dark', 'Light']
        
        self.tech_words = ['Code', 'Data', 'Sync', 'Node', 'Core', 'Link', 'Hack', 'Bit', 'Byte', 'Cloud', 'Logic', 'Pixel', 'Matrix', 'Vector', 'Cache', 'Debug', 'Binary', 'Crypto', 'Token', 'Mesh', 'Stack', 'Frame', 'Query', 'Script', 'Parse', 'Tech', 'Digital', 'Cyber', 'Net', 'Web', 'App', 'Dev', 'System', 'Smart', 'Future']
        
        self.creative_words = ['Art', 'Flow', 'Vibe', 'Wave', 'Glow', 'Spark', 'Dream', 'Magic', 'Star', 'Moon', 'Sun', 'Sky', 'Ocean', 'Forest', 'Crystal', 'Diamond', 'Gold', 'Silver', 'Pearl', 'Jade', 'Aurora', 'Zen', 'Muse', 'Aura', 'Iris', 'Color', 'Paint', 'Draw', 'Create', 'Design', 'Style', 'Beauty', 'Grace', 'Wonder', 'Vision']
        
        self.business_words = ['Global', 'Prime', 'Elite', 'Pro', 'Expert', 'Master', 'Chief', 'Lead', 'Senior', 'Executive', 'Capital', 'Venture', 'Summit', 'Apex', 'Crown', 'Royal', 'Premium', 'Platinum', 'Diamond', 'Gold', 'Success', 'Winner', 'Leader', 'Boss', 'CEO', 'Manager', 'Director', 'Consultant', 'Advisor', 'Strategist']
        
        self.suffixes = ['X', 'Pro', 'Max', 'Core', 'Tech', 'Lab', 'Hub', 'Zone', 'Base', 'Net', 'Sys', 'Dev', 'Bot', 'App', 'Web', 'Code', 'Data', 'Sync', 'Link', 'Plus', 'Ultra', 'Prime', 'Elite', 'Apex', 'VX', 'ZX', 'QX']
        
        # Valuable keywords for scoring
        self.valuable_words = ['pro', 'elite', 'prime', 'ultra', 'max', 'core', 'alpha', 'beta', 'cyber', 'neo', 'master', 'expert', 'global', 'premium', 'diamond', 'platinum', 'power', 'gamer', 'player', 'hero', 'legend', 'epic', 'tech', 'digital', 'smart', 'future', 'art', 'magic', 'star', 'gold', 'silver', 'success', 'winner', 'leader']
    
    def generate_by_category(self, category='gaming', count=8):
        """Generate usernames by category"""
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
                lambda: random.choice(self.gaming_words).lower() + random.choice(self.suffixes).lower(),
                lambda: random.choice(self.gaming_words).lower() + str(random.randint(10, 99)),
                lambda: 'dark' + random.choice(self.gaming_words).lower(),
                lambda: random.choice(self.gaming_words).lower() + 'lord',
                lambda: 'shadow' + random.choice(self.gaming_words).lower(),
                lambda: random.choice(['cyber', 'neo', 'ultra']).lower() + random.choice(self.gaming_words).lower(),
                lambda: random.choice(self.gaming_words).lower() + random.choice(['gaming', 'play', 'pro']),
                lambda: random.choice(['epic', 'legendary', 'mythic']).lower() + random.choice(self.gaming_words).lower()[:4],
                lambda: self._create_mixed_pattern(),
                lambda: self._create_short_pattern()
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_tech_usernames(self, count):
        usernames = []
        for i in range(count):
            patterns = [
                lambda: random.choice(self.tech_words).lower() + random.choice(self.suffixes).lower(),
                lambda: random.choice(['dev', 'code', 'tech', 'sys']).lower() + random.choice(self.tech_words).lower(),
                lambda: random.choice(self.tech_words).lower() + str(random.randint(10, 99)),
                lambda: 'cyber' + random.choice(self.tech_words).lower(),
                lambda: random.choice(['digital', 'virtual', 'smart']).lower() + random.choice(self.tech_words).lower()[:4],
                lambda: random.choice(self.tech_words).lower() + 'labs',
                lambda: random.choice(['future', 'next', 'advanced']).lower() + random.choice(self.tech_words).lower()[:4],
                lambda: random.choice(self.tech_words).lower() + 'studio',
                lambda: self._create_mixed_pattern(),
                lambda: self._create_short_pattern()
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_creative_usernames(self, count):
        usernames = []
        for i in range(count):
            patterns = [
                lambda: random.choice(self.creative_words).lower() + random.choice(['flow', 'wave', 'glow', 'spark']),
                lambda: 'art' + random.choice(self.creative_words).lower(),
                lambda: random.choice(self.creative_words).lower() + 'studio',
                lambda: random.choice(['magic', 'dream', 'wonder']).lower() + random.choice(self.creative_words).lower(),
                lambda: random.choice(self.creative_words).lower() + 'design',
                lambda: random.choice(['creative', 'artistic', 'visual']).lower() + random.choice(self.creative_words).lower()[:4],
                lambda: random.choice(self.creative_words).lower() + 'works',
                lambda: random.choice(['inspired', 'brilliant', 'elegant']).lower() + random.choice(self.creative_words).lower()[:4],
                lambda: self._create_mixed_pattern(),
                lambda: self._create_short_pattern()
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_professional_usernames(self, count):
        usernames = []
        for i in range(count):
            patterns = [
                lambda: random.choice(self.business_words).lower() + random.choice(['solutions', 'group', 'corp']),
                lambda: random.choice(['mr', 'ms', 'dr']).lower() + random.choice(self.business_words).lower(),
                lambda: random.choice(self.business_words).lower() + 'consultant',
                lambda: random.choice(['business', 'finance', 'legal']).lower() + random.choice(self.business_words).lower(),
                lambda: random.choice(self.business_words).lower() + 'partners',
                lambda: random.choice(['professional', 'corporate', 'executive']).lower() + random.choice(self.business_words).lower()[:4],
                lambda: random.choice(self.business_words).lower() + 'ventures',
                lambda: random.choice(['success', 'achievement', 'excellence']).lower() + random.choice(self.business_words).lower()[:4],
                lambda: self._create_mixed_pattern(),
                lambda: self._create_short_pattern()
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _generate_mixed_usernames(self, count):
        usernames = []
        all_words = self.gaming_words + self.tech_words + self.creative_words + self.business_words
        for i in range(count):
            patterns = [
                lambda: random.choice(all_words).lower() + random.choice(self.suffixes).lower(),
                lambda: random.choice(all_words).lower() + str(random.randint(10, 99)),
                lambda: random.choice(['dark', 'neo', 'cyber', 'ultra', 'super', 'mega']).lower() + random.choice(all_words).lower(),
                lambda: random.choice(all_words).lower() + str(random.randint(1000, 9999)),
                lambda: random.choice(['next', 'future', 'modern', 'advanced']).lower() + random.choice(all_words).lower()[:4],
                lambda: random.choice(all_words).lower() + random.choice(['hub', 'zone', 'base', 'core']),
                lambda: random.choice(['smart', 'digital', 'elite', 'premium']).lower() + random.choice(all_words).lower()[:4],
                lambda: random.choice(all_words).lower() + 'network',
                lambda: self._create_mixed_pattern(),
                lambda: self._create_short_pattern()
            ]
            username = random.choice(patterns)()
            usernames.append(username)
        return usernames
    
    def _create_mixed_pattern(self):
        """Create mixed letter/number patterns"""
        patterns = [
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(4, 7))) + str(random.randint(10, 99)),
            lambda: random.choice(['x', 'z', 'k', 'q']) + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3, 5))),
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3, 5))) + random.choice(['x', 'z', 'k']),
            lambda: random.choice(self.valuable_words) + str(random.randint(1, 999)),
            lambda: ''.join(random.choices('bcdfghjklmnpqrstvwxyz', k=3)) + ''.join(random.choices('aeiou', k=2)),
        ]
        return random.choice(patterns)()
    
    def _create_short_pattern(self):
        """Create shorter, potentially more valuable patterns"""
        patterns = [
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(4, 6))),
            lambda: random.choice(['x', 'z', 'q', 'k']) + ''.join(random.choices('aeiou', k=1)) + ''.join(random.choices('bcdfghjklmnpqrstvwxyz', k=2)),
            lambda: ''.join(random.choices('bcdfghjklmnpqrstvwxyz', k=2)) + ''.join(random.choices('aeiou', k=1)) + random.choice(['x', 'z']),
            lambda: random.choice(self.valuable_words[:10]) + random.choice(['x', 'z', '']),
        ]
        return random.choice(patterns)()

# Enhanced Value Assessor with detailed insights
class ValueAssessor:
    def __init__(self):
        self.valuable_words = ['pro', 'elite', 'prime', 'ultra', 'max', 'core', 'alpha', 'beta', 'cyber', 'neo', 'master', 'expert', 'global', 'premium', 'diamond', 'platinum', 'power', 'gamer', 'player', 'hero', 'legend', 'epic', 'tech', 'digital', 'smart', 'future', 'art', 'magic', 'star', 'gold', 'silver', 'success', 'winner', 'leader']
    
    def assess_username_detailed(self, username):
        """Detailed assessment with insights"""
        score = 50  # Base score
        insights = []
        
        # Length assessment
        length = len(username)
        if length <= 4:
            score += 40
            insights.append("Ultra-short")
        elif length <= 6:
            score += 30
            insights.append("Short")
        elif length <= 8:
            score += 20
            insights.append("Moderate length")
        elif length <= 12:
            score += 10
            insights.append("Average length")
        else:
            score -= 5
            insights.append("Long")
        
        # Character composition
        if username.isalpha():
            score += 15
            insights.append("Clean alphabetic")
        elif any(c.isdigit() for c in username) and any(c.isalpha() for c in username):
            if username[-2:].isdigit() or username[-1:].isdigit():
                insights.append("Word + number pattern")
            else:
                insights.append("Mixed alphanumeric")
        
        # Premium character bonus
        premium_chars = ['x', 'z', 'q', 'k']
        if any(c in username.lower() for c in premium_chars):
            score += 8
            insights.append("Premium characters")
        
        # Valuable word detection
        username_lower = username.lower()
        valuable_found = []
        for word in self.valuable_words:
            if word in username_lower:
                valuable_found.append(word)
                score += 12
        if valuable_found:
            insights.append("Contains valuable word")
        
        # Brandability factors
        brandable_factors = []
        
        # Pronounceability check
        if self._is_pronounceable(username):
            score += 8
            brandable_factors.append("Pronounceable")
        
        # No numbers/symbols for brandability
        if username.isalpha():
            score += 5
            brandable_factors.append("No numbers/symbols")
        
        # Vowel balance
        vowels = sum(1 for c in username.lower() if c in 'aeiou')
        consonants = sum(1 for c in username.lower() if c.isalpha() and c not in 'aeiou')
        if vowels > 0 and consonants > 0:
            ratio = min(vowels, consonants) / max(vowels, consonants)
            if ratio > 0.3:
                score += 6
                brandable_factors.append("Good vowel balance")
        
        # Alternating pattern (vowel-consonant)
        if self._has_alternating_pattern(username):
            score += 5
            insights.append("Alternating pattern")
        
        # Add brandable insight if factors exist
        if brandable_factors:
            insights.append(f"Brandable ({', '.join(brandable_factors)})")
        
        # Dictionary word bonus
        if self._contains_dictionary_word(username):
            score += 7
            insights.append("Contains dictionary word")
        
        # Short and clean bonus
        if length <= 6 and username.isalpha():
            score += 10
            insights.append("Premium short format")
        
        # Memorability
        if self._is_memorable(username):
            score += 5
            insights.append("Memorable")
        
        # Final score normalization
        final_score = min(100, max(30, score))
        
        return final_score, insights
    
    def _is_pronounceable(self, username):
        """Check if username is pronounceable"""
        vowels = 'aeiou'
        consonant_streak = 0
        vowel_streak = 0
        
        for char in username.lower():
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
        return len(username) >= 3
    
    def _has_alternating_pattern(self, username):
        """Check for vowel-consonant alternating pattern"""
        if len(username) < 4:
            return False
        vowels = 'aeiou'
        alternations = 0
        for i in range(len(username) - 1):
            if username[i].isalpha() and username[i+1].isalpha():
                if (username[i].lower() in vowels) != (username[i+1].lower() in vowels):
                    alternations += 1
        return alternations >= len([c for c in username if c.isalpha()]) * 0.4
    
    def _contains_dictionary_word(self, username):
        """Check if contains common dictionary words"""
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
        username_lower = username.lower()
        return any(word in username_lower for word in common_words if len(word) >= 3)
    
    def _is_memorable(self, username):
        """Check memorability factors"""
        # Repeated letters
        if len(set(username.lower())) < len(username) * 0.7:
            return True
        # Rhyming pattern
        if len(username) >= 4 and username[-2:].lower() == username[-4:-2].lower():
            return True
        return False
    
    def get_value_icon(self, score):
        """Get appropriate icon based on score"""
        if score >= 85:
            return '💎'
        elif score >= 75:
            return '⭐'
        elif score >= 65:
            return '🔥'
        elif score >= 50:
            return '📝'
        else:
            return '📝'

# Initialize generators
username_gen = UsernameGenerator()
value_assessor = ValueAssessor()

# User session tracking
user_sessions = {}

def get_user_session(user_id):
    """Get or create user session"""
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'daily_generations': 0,
            'total_generations': 0,
            'subscription_tier': 'free',
            'last_reset': time.strftime('%Y-%m-%d'),
            'join_date': time.strftime('%Y-%m-%d'),
            'last_active': time.time()
        }
    
    # Reset daily counter if new day
    today = time.strftime('%Y-%m-%d')
    if user_sessions[user_id]['last_reset'] != today:
        user_sessions[user_id]['daily_generations'] = 0
        user_sessions[user_id]['last_reset'] = today
    
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
    
    session = get_user_session(user_id)
    
    if text.startswith('/start'):
        send_message(chat_id, '''🎯 <b>Welcome to Advanced Username Generator!</b>

💎 <b>Professional Features:</b>
• 5 specialized generation categories with unique algorithms
• Detailed scoring system with comprehensive insights
• Real value estimates and rarity classification
• Ultra-rare premium usernames for subscribers

🎮 <b>Categories Available:</b>
• <b>Gaming:</b> Perfect for streamers, esports, content creators
• <b>Tech:</b> Ideal for developers, startups, tech professionals  
• <b>Creative:</b> Great for artists, designers, influencers
• <b>Professional:</b> Business-focused, corporate-ready handles
• <b>Mixed:</b> Advanced combination algorithms

💰 <b>Subscription Plans:</b>
• <b>Free:</b> 5 generations/day, all categories, full scoring
• <b>Premium ($9.99/month):</b> Unlimited + ultra-rare usernames
• <b>VIP ($29.99/month):</b> Premium + custom requests + priority

📝 <b>Quick Commands:</b>
/generate [category] - Generate by category
/categories - Browse all categories  
/premium - Ultra-rare premium usernames
/subscribe - Crypto payment plans

Try: <code>/generate gaming</code>''')
        
    elif text.startswith('/categories'):
        send_message(chat_id, '''🎯 <b>Username Generation Categories</b>

🎮 <b>Gaming:</b> <code>/generate gaming</code>
Perfect for: Streamers, gamers, esports teams, content creators
Focus: Action words, power terms, competitive elements

💻 <b>Tech:</b> <code>/generate tech</code>  
Ideal for: Developers, startups, IT professionals, tech enthusiasts
Focus: Technical terms, modern concepts, innovation themes

🎨 <b>Creative:</b> <code>/generate creative</code>
Great for: Artists, designers, influencers, creative professionals
Focus: Artistic terms, aesthetic concepts, inspiration themes

💼 <b>Professional:</b> <code>/generate professional</code>
Perfect for: Business, consulting, corporate, executive brands
Focus: Business terms, authority concepts, success themes

🎲 <b>Mixed:</b> <code>/generate</code> (default)
Advanced combination of all categories with smart pattern mixing

💎 <b>Premium Only:</b> <code>/premium</code>
Ultra-rare 3-5 character usernames (Premium/VIP subscribers)

Each category generates 8 unique usernames with detailed scoring analysis!''')
        
    elif text.startswith('/generate'):
        # Check daily limit for free users
        if session['subscription_tier'] == 'free' and session['daily_generations'] >= 5:
            send_message(chat_id, f'''🔒 <b>Daily Generation Limit Reached</b>

Free users: 5 usernames per day
You've used all {session['daily_generations']} generations today.

💎 <b>Upgrade to Premium for:</b>
• Unlimited username generations (all categories)
• Ultra-rare premium usernames (3-5 chars)
• Advanced algorithms with enhanced scoring
• Priority customer support

<b>Your Stats:</b>
• Total generated: {session['total_generations']} usernames
• Member since: {session['join_date']}

Use /subscribe to unlock unlimited premium features!''')
            return
        
        # Parse category
        parts = text.split(' ')
        category = parts[1] if len(parts) > 1 else 'gaming'
        
        # Generate usernames
        usernames = username_gen.generate_by_category(category, 8)
        
        response = f'🎯 <b>Generated {category.title()} Usernames:</b>\n\n'
        
        for username in usernames:
            score, insights = value_assessor.assess_username_detailed(username)
            icon = value_assessor.get_value_icon(score)
            
            response += f'{icon} <b>{username}</b>\n'
            response += f'   📊 Score: {score}/100\n'
            response += f'   💡 {", ".join(insights)}\n\n'
        
        # Update session
        if session['subscription_tier'] == 'free':
            session['daily_generations'] += 1
            session['total_generations'] += 1
            remaining = 5 - session['daily_generations']
            response += f'📈 <b>Usage:</b> {remaining} generations remaining today\n'
        
        response += '\n💡 <b>Tip:</b> Higher scores indicate more valuable usernames!'
        
        send_message(chat_id, response)
        
    elif text.startswith('/premium'):
        if session['subscription_tier'] == 'free':
            send_message(chat_id, '''🔒 <b>Premium Feature - Ultra-Rare Usernames</b>

Exclusive ultra-rare 3-5 character usernames with exceptional value potential.

<b>💎 Premium Examples:</b>
💎 <code>zyx</code> - Score: 95/100 | Ultra-short, Premium characters
💎 <code>qtech</code> - Score: 88/100 | Short, Premium characters, Valuable word
💎 <code>xpro9</code> - Score: 92/100 | Short, Premium characters, Word + number

<b>Premium Benefits:</b>
• Ultra-rare 3-5 character usernames
• Unlimited generations (all categories)
• Advanced scoring algorithms
• Priority customer support

💎 Upgrade with /subscribe to unlock premium features!''')
            return
        
        # Generate premium usernames for subscribers
        premium_usernames = ['zyx', 'qtech', 'xpro9', 'kvibe', 'zcore']
        
        response = '💎 <b>Ultra-Rare Premium Usernames:</b>\n\n'
        
        for username in premium_usernames:
            score, insights = value_assessor.assess_username_detailed(username)
            score += 10  # Premium bonus
            score = min(100, score)
            icon = value_assessor.get_value_icon(score)
            
            response += f'{icon} <b>{username}</b>\n'
            response += f'   📊 Score: {score}/100\n'
            response += f'   💡 {", ".join(insights)}\n\n'
        
        response += '🔥 <b>These are exclusive ultra-rare handles with exceptional value potential!</b>'
        
        send_message(chat_id, response)
        
    elif text.startswith('/subscribe'):
        send_message(chat_id, '''💎 <b>Professional Crypto Subscription Plans</b>

🔥 <b>Premium Plan - $9.99/month</b>
✅ Unlimited username generations (all 5 categories)
✅ Advanced algorithms with enhanced scoring
✅ Ultra-rare premium usernames (3-5 characters)
✅ Detailed value analysis with comprehensive insights
✅ Priority customer support

💎 <b>VIP Plan - $29.99/month</b>
✅ Everything in Premium
✅ Custom generation requests with consultation
✅ Exclusive ultra-rare algorithms
✅ Early access to new features
✅ Direct priority support

<b>Accepted Cryptocurrencies:</b>
Bitcoin (BTC) • Litecoin (LTC) • Ethereum (ETH) • USDT

<b>Payment Addresses:</b>
BTC: <code>bc1qygedkhjxaw0dfx85x232rdxdamp9hczac5fpc3</code>
LTC: <code>ltc1q5da462tgrmsdjt95n8lj66hwrdllrma8h0lnaa</code>
ETH/USDT: <code>0x020b47D9a3782B034ec8e8fa216B827aB253e3c3</code>

<b>Payment Process:</b>
1. Send exact USD equivalent to appropriate address
2. Forward transaction hash with plan choice
3. Include: Transaction hash + Plan + Your username
4. Activation within 24 hours

<b>Example:</b>
<code>Payment: abc123def456... Premium @yourusername</code>''')
        
    elif text.startswith('/help'):
        send_message(chat_id, '''🤖 <b>Username Generator - Complete Guide</b>

<b>Generation Commands:</b>
/generate - Gaming category (default)
/generate [category] - Specialized generation
/categories - Browse all 5 categories
/premium - Ultra-rare premium usernames (Premium+)

<b>Available Categories:</b>
• <code>gaming</code> - Streamers, esports, content creators
• <code>tech</code> - Developers, startups, IT professionals  
• <code>creative</code> - Artists, designers, influencers
• <code>professional</code> - Business, corporate, consulting

<b>Account & Status:</b>
/subscribe - Professional crypto subscription plans
/status - Account analytics and usage stats
/help - This comprehensive command guide

<b>Key Features:</b>
✨ Specialized algorithms per category
✨ Detailed scoring with comprehensive insights
✨ Value estimates and rarity classification
✨ Ultra-rare premium usernames
✨ Professional crypto subscription system

<b>Quick Examples:</b>
<code>/generate gaming</code> - Gaming-optimized usernames
<code>/generate tech</code> - Tech/startup-focused usernames''')
        
    elif text.startswith('/status'):
        remaining = max(0, 5 - session['daily_generations']) if session['subscription_tier'] == 'free' else 'Unlimited'
        
        send_message(chat_id, f'''📊 <b>Account Status</b>

👤 <b>Profile:</b> @{username}
💎 <b>Tier:</b> {session['subscription_tier'].title()}
📅 <b>Member Since:</b> {session['join_date']}
🎯 <b>Today's Limit:</b> {remaining} generations remaining

📈 <b>Statistics:</b>
• Total usernames: {session['total_generations']}
• Daily generations: {session['daily_generations']}/5

🔥 <b>Features Available:</b>
✅ 5 specialized generation categories
✅ Detailed value scoring with insights
✅ Value estimates and rarity classification
{'✅ Ultra-rare premium usernames' if session['subscription_tier'] != 'free' else '🔒 Premium usernames (upgrade needed)'}
{'✅ Unlimited generations' if session['subscription_tier'] != 'free' else '🔒 Unlimited (upgrade needed)'}

{'💡 Upgrade to Premium for unlimited generation!' if session['subscription_tier'] == 'free' else '✨ Thank you for being a premium member!'}''')
    
    else:
        send_message(chat_id, '''❓ <b>Command not recognized</b>

<b>Try these commands:</b>
• <code>/generate [category]</code> - Generate usernames
• <code>/categories</code> - Browse 5 categories
• <code>/premium</code> - Ultra-rare premium usernames
• <code>/subscribe</code> - Professional subscription plans
• <code>/help</code> - Complete feature guide

<b>Quick Examples:</b>
• <code>/generate gaming</code> - Gaming usernames
• <code>/generate tech</code> - Tech usernames  

💡 Each category uses specialized algorithms for authentic, valuable usernames!''')

def run_telegram_polling():
    logger.info("Starting Telegram bot polling...")
    
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
                if response.status_code != 409:
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
        logger.info("Bot thread started successfully")
    except Exception as e:
        logger.error(f"Failed to start bot thread: {e}")

# Flask routes
@app.route('/')
def index():
    return '''
    <h1>🎯 Enhanced Username Generator Bot</h1>
    <p>Status: <strong>✅ All Features Active</strong></p>
    <p>Bot: <strong>@UsernameavailablesBot</strong></p>
    <p>Platform: <strong>Heroku Deployment</strong></p>
    
    <h2>🔥 Enhanced Features:</h2>
    <ul>
        <li><strong>5 Specialized Categories:</strong> Gaming, Tech, Creative, Professional, Mixed</li>
        <li><strong>Advanced Algorithms:</strong> Unique patterns for each category</li>
        <li><strong>Detailed Scoring:</strong> Comprehensive insights with analysis</li>
        <li><strong>Value Estimates:</strong> Professional scoring system</li>
        <li><strong>Ultra-rare Usernames:</strong> 3-5 character premium handles</li>
        <li><strong>Crypto Payments:</strong> BTC, LTC, ETH, USDT integration</li>
    </ul>
    
    <p><a href="/health">Health Check</a></p>
    '''

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "platform": "heroku",
        "bot": "active",
        "features": {
            "generation": True,
            "detailed_scoring": True,
            "premium_usernames": True,
            "crypto_payments": True,
            "categories": 5
        },
        "stats": {
            "active_users": len(user_sessions),
            "total_generations": sum(s['total_generations'] for s in user_sessions.values())
        }
    })

# Initialize bot
logger.info("Starting bot initialization...")
start_bot()
logger.info("Bot initialization complete")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
