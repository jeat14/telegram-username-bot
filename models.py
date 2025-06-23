from app import db
from datetime import datetime, timezone
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    
    # Subscription info
    subscription_tier = db.Column(db.String(20), default='free')  # free, premium, vip
    subscription_expires = db.Column(db.DateTime, nullable=True)
    crypto_wallet = db.Column(db.String(128), nullable=True)
    
    # Usage tracking
    daily_generations = db.Column(db.Integer, default=0)
    total_generations = db.Column(db.Integer, default=0)
    availability_checks = db.Column(db.Integer, default=0)
    last_generation_date = db.Column(db.Date, nullable=True)
    
    # Account info
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_active = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_banned = db.Column(db.Boolean, default=False)
    
    # Relationships
    interactions = db.relationship('UserInteraction', backref='user', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.telegram_id}>'
    
    def can_generate(self):
        """Check if user can generate usernames based on subscription"""
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
    
    def can_check_availability(self):
        """Check if user can use availability checking"""
        return self.subscription_tier in ['premium', 'vip'] and self.subscription_expires > datetime.now(timezone.utc)
    
    def increment_usage(self):
        """Increment generation counter"""
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
    
    # Interaction details
    command = db.Column(db.String(64), nullable=False)
    message_text = db.Column(db.Text, nullable=True)
    response_type = db.Column(db.String(32), nullable=True)  # generation, help, error, etc.
    
    # Generated content
    usernames_generated = db.Column(db.Text, nullable=True)  # JSON array
    generation_category = db.Column(db.String(32), nullable=True)
    
    # Metadata
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ip_address = db.Column(db.String(45), nullable=True)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Interaction {self.user_id}: {self.command}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Payment details
    transaction_hash = db.Column(db.String(128), unique=True, nullable=False)
    cryptocurrency = db.Column(db.String(10), nullable=False)  # BTC, ETH, USDT, etc.
    amount = db.Column(db.Numeric(18, 8), nullable=False)
    usd_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Subscription details
    subscription_type = db.Column(db.String(20), nullable=False)  # premium, vip
    duration_months = db.Column(db.Integer, nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, failed
    confirmations = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    confirmed_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Payment {self.transaction_hash}: {self.amount} {self.cryptocurrency}>'

class AvailabilityCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Check details
    username = db.Column(db.String(64), nullable=False)
    platforms_checked = db.Column(db.Text, nullable=False)  # JSON array
    results = db.Column(db.Text, nullable=False)  # JSON object with platform:available pairs
    
    # Metadata
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    check_type = db.Column(db.String(20), nullable=False)  # basic, comprehensive
    
    def __repr__(self):
        return f'<AvailabilityCheck {self.username}>'

class BotStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    
    # Daily stats
    total_users = db.Column(db.Integer, default=0)
    new_users = db.Column(db.Integer, default=0)
    active_users = db.Column(db.Integer, default=0)
    total_generations = db.Column(db.Integer, default=0)
    premium_conversions = db.Column(db.Integer, default=0)
    revenue_usd = db.Column(db.Numeric(10, 2), default=0)
    
    # Command usage
    command_stats = db.Column(db.Text, nullable=True)  # JSON object
    
    def __repr__(self):
        return f'<BotStats {self.date}>'