import re
from typing import Dict, List


def format_content_preview(content: str, max_length: int = 100) -> str:
    """Format content for preview display"""
    if len(content) <= max_length:
        return content
    return content[:max_length] + "..."

def calculate_heat_rating(comments: List[Dict]) -> int:
    """Calculate a heat rating based on comment sentiment"""
    if not comments:
        return 0
    
    # Simple heuristic based on comment length and certain keywords
    total_heat = 0
    for comment in comments:
        text = comment['text'].lower()
        heat = 1  # Base heat
        
        # Increase heat for longer comments
        if len(text) > 100:
            heat += 1
        
        # Increase heat for emotional words
        emotional_words = ['amazing', 'terrible', 'love', 'hate', 'wow', 'omg', 'wtf', '!', '!!!']
        for word in emotional_words:
            if word in text:
                heat += 1
        
        total_heat += min(heat, 5)  # Cap individual comment heat at 5
    
    # Average and scale to 1-10
    avg_heat = total_heat / len(comments)
    return min(int(avg_heat * 2), 10)

def get_toxicity_level(heat_rating: int) -> str:
    """Convert heat rating to toxicity description"""
    if heat_rating <= 2:
        return "😊 Mild"
    elif heat_rating <= 5:
        return "🔥 Medium"
    elif heat_rating <= 8:
        return "🌶️ Spicy"
    else:
        return "💀 Savage"