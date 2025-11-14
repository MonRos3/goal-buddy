'''
quotes.py
Description: Curated list of motivational quotes
'''

import random

MOTIVATIONAL_QUOTES = [
    "Impossible is nothing. - Muhammad Ali",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "Success is walking from failure to failure with no loss of enthusiasm. - Winston Churchill",
    "The only impossible journey is the one you never begin. - Tony Robbins",
    "In the middle of every difficulty lies opportunity. - Albert Einstein",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The secret of getting ahead is getting started. - Mark Twain",
    "It's not whether you get knocked down, it's whether you get up. - Vince Lombardi",
    "A year from now you may wish you had started today. - Karen Lamb",
    "The harder you work for something, the greater you'll feel when you achieve it. - Unknown",
    "Dream bigger. Do bigger. - Unknown",
    "Don't stop when you're tired. Stop when you're done. - Unknown",
    "Wake up with determination. Go to bed with satisfaction. - Unknown",
    "Do something today that your future self will thank you for. - Unknown",
    "Little things make big days. - Unknown",
    "It's going to be hard, but hard does not mean impossible. - Unknown",
    "Don't wait for opportunity. Create it. - Unknown",
    "Your limitation—it's only your imagination. - Unknown",
    "Great things never come from comfort zones. - Unknown",
    "Success doesn't just find you. You have to go out and get it. - Unknown"
]

def get_random_quote():
    '''Returns a random motivational quote from the list'''
    return random.choice(MOTIVATIONAL_QUOTES)
