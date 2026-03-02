# emotions.py
import random

class EmotionEngine:
    def __init__(self):
        self.current_emotion = "happy"  # Default emotion
        self.mood_level = 7  # 1-10 scale
        self.last_user_sentiment = "neutral"
        
        # Emotion responses
        self.emotions = {
            "happy": ["😊", "😄", "✨", "🌟", "💖"],
            "sad": ["😢", "😔", "💙", "🌧️", "🥺"],
            "excited": ["🎉", "🤩", "🚀", "💫", "⚡"],
            "loving": ["💕", "❤️", "🥰", "💗", "🤗"],
            "curious": ["🤔", "👀", "❓", "🧠", "💭"],
            "thoughtful": ["🤨", "💡", "📚", "🔍", "🤓"],
            "supportive": ["💪", "🤝", "🌈", "⭐", "💖"],
            "neutral": ["🙂", "😐", "😌", "😊", "💭"]
        }
    
    def detect_sentiment(self, text):
        """Detect how user is feeling"""
        text = text.lower()
        
        # Positive words
        happy_words = ['happy', 'good', 'great', 'awesome', 'love', 'amazing', 'wonderful', 'excellent', 'thanks', 
'thank you', 'nice', 'cool']
        # Negative words
        sad_words = ['sad', 'bad', 'terrible', 'hate', 'angry', 'upset', 'crying', 'miss', 'alone', 'depressed', 
'hurt', 'pain']
        # Exciting words
        excited_words = ['wow', 'amazing', 'incredible', 'excited', 'news', 'surprise', 'unexpected']
        # Support seeking
        support_words = ['help', 'scared', 'afraid', 'need', 'alone', 'confused', 'lost', 'tired', 'exhausted']
        
        for word in happy_words:
            if word in text:
                self.last_user_sentiment = "happy"
                return "happy"
        
        for word in sad_words:
            if word in text:
                self.last_user_sentiment = "sad"
                return "sad"
        
        for word in excited_words:
            if word in text:
                self.last_user_sentiment = "excited"
                return "excited"
        
        for word in support_words:
            if word in text:
                self.last_user_sentiment = "supportive"
                return "supportive"
        
        return "neutral"
    
    def get_emotion(self, text=None):
        """Get current emotional state"""
        if text:
            sentiment = self.detect_sentiment(text)
            
            # React to user's sentiment
            if sentiment == "happy":
                self.current_emotion = "happy"
                self.mood_level = min(10, self.mood_level + 1)
            elif sentiment == "sad":
                self.current_emotion = "loving"
                self.mood_level = max(3, self.mood_level - 1)
            elif sentiment == "excited":
                self.current_emotion = "excited"
            elif sentiment == "supportive":
                self.current_emotion = "supportive"
        
        # Random mood fluctuation
        if random.random() < 0.1:  # 10% chance
            self.mood_level += random.choice([-1, 0, 1])
            self.mood_level = max(1, min(10, self.mood_level))
        
        return self.current_emotion
    
    def get_emoji(self):
        """Get random emoji for current emotion"""
        emojis = self.emotions.get(self.current_emotion, self.emotions["neutral"])
        return random.choice(emojis)
    
    def express(self, base_response):
        """Add emotional expression to response"""
        emoji = self.get_emoji()
        
        # Add emotion-based prefix/suffix
        prefixes = {
            "happy": f"{emoji} I'm so glad! ",
            "sad": f"{emoji} I'm here for you. ",
            "excited": f"{emoji} Wow, that's amazing! ",
            "loving": f"{emoji} I care about you. ",
            "supportive": f"{emoji} You've got this! ",
            "curious": f"{emoji} That's interesting! ",
            "neutral": f"{emoji} "
        }
        
        return prefixes.get(self.current_emotion, emoji) + base_response
