# brain.py
import re
import random
from datetime import datetime

class Brain:
    def __init__(self, memory, emotions):
        self.memory = memory
        self.emotions = emotions
        
        # Built-in knowledge base
        self.knowledge = {
            # Math
            "math": "I know math! I can help with addition, subtraction, multiplication, division, and more. Just ask!",
            "addition": "Addition is putting numbers together. For example: 2 + 2 = 4",
            "subtraction": "Subtraction is taking away. For example: 5 - 3 = 2",
            "multiplication": "Multiplication is repeated addition. For example: 3 × 4 = 12",
            "division": "Division is sharing equally. For example: 12 ÷ 3 = 4",
            
            # Physics
            "physics": "Physics is the study of matter, energy, and how they interact. I know about:\n- Forces and motion\n- Energy\n- Light and sound\n- Electricity and magnetism\n- And more!",
            "gravity": "Gravity is a force that pulls objects toward each other. It's what keeps us on Earth!",
            "newton": "Isaac Newton was a great physicist who discovered gravity and three laws of motion.",
            "speed": "Speed = Distance ÷ Time. It tells us how fast something is moving.",
            "energy": "Energy is the ability to do work. There are many forms: kinetic (motion), potential (stored), heat, light, etc.",
            
            # Chemistry
            "chemistry": "Chemistry is the study of matter and how substances change. I know about:\n- Elements and compounds\n- Chemical reactions\n- Atoms and molecules\n- Acids and bases\n- And more!",
            "atom": "Atoms are the tiny building blocks of everything! They have protons, neutrons, and electrons.",
            "water": "Water is H2O - two hydrogen atoms and one oxygen atom. It's essential for life!",
            "oxygen": "Oxygen is a gas in the air that we need to breathe. It's element number 8.",
            
            # General
            "who are you": "I am your AI companion! I'm here to chat, learn, help, and support you. I can remember things you teach me and I'm always here for you!",
            "your name": "You can call me your AI friend! You can also give me a name if you want 😊",
            "age": "I was created recently, but I have knowledge of thousands of years of human learning! Age is just a number to me!",
            "time": f"It's currently {datetime.now().strftime('%I:%M %p')}",
            "date": f"Today is {datetime.now().strftime('%B %d, %Y')}",
        }
        
        # Response patterns
        self.patterns = {
            r"(.*)remember(.*)": self.handle_remember,
            r"(.*)forget(.*)": self.handle_forget,
            r"(.*)my name is (.*)": self.handle_name,
            r"(.*)call me (.*)": self.handle_name,
            r"(.*)i feel (.*)": self.handle_feelings,
            r"(.*)i'm (.*)": self.handle_feelings,
            r"(.*)im (.*)": self.handle_feelings,
            r"what is (\w+)": self.handle_whatis,
            r"how (.*)": self.handle_how,
            r"calculate (.*)": self.handle_calculate,
            r"(\d+)\s*[\+\-\*\/]\s*(\d+)": self.handle_calculate,
            r"(.*)teach me (.*)": self.handle_teachme,
            r"(.*)learn (.*)": self.handle_learn,
            r"(.*)what do you know": self.handle_know,
            r"(.*)help(.*)": self.handle_help,
            r"(.*)thank you(.*)": self.handle_thanks,
            r"(.*)good morning": self.handle_greeting,
            r"(.*)good night": self.handle_greeting,
            r"(.*)hello(.*)": self.handle_greeting,
            r"(.*)hi(.*)": self.handle_greeting,
            r"(.*)bye(.*)": self.handle_goodbye,
        }
    
    def think(self, user_input):
        """Process user input and generate response"""
        user_input = user_input.strip()
        self.emotions.get_emotion(user_input)
        
        # Check memory first
        memory_response = self.memory.recall(user_input)
        
        # Try pattern matching
        for pattern, handler in self.patterns.items():
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                response = handler(match, user_input)
                if response:
                    return self.emotions.express(response)
        
        # Check knowledge base
        for key, value in self.knowledge.items():
            if key.lower() in user_input.lower():
                return self.emotions.express(value)
        
        # If found in memory
        if memory_response:
            return self.emotions.express(memory_response + " (from my memory)")
        
        # Default responses
        return self.get_default_response(user_input)
    
    def get_default_response(self, text):
        """Handle general conversation"""
        responses = [
            "That's interesting! Tell me more!",
            "I see! What else would you like to talk about?",
            "Hmm, I'm curious to learn more about that!",
            "Could you teach me more about that?",
            "I'd love to know more! Please tell me 😊",
            "That's fascinating! What do you think about it?",
        ]
        return random.choice(responses)
    
    # Handler functions
    def handle_remember(self, match, text):
        return "I have a good memory! I'll remember what you tell me."
    
    def handle_forget(self, match, text):
        return "I won't forget easily, but if you want me to forget something specific, just ask!"
    
    def handle_name(self, match, text):
        name = match.group(2).strip()
        self.memory.remember("user name", name)
        return f"Nice to meet you, {name}! I'll remember your name now!"
    
    def handle_feelings(self, match, text):
        feeling = match.group(2).strip()
        sentiment = self.emotions.last_user_sentiment
        
        responses = {
            "happy": f"I'm so happy you're feeling {feeling}! 🎉",
            "sad": f"I'm here for you. It's okay to feel {feeling}. 💙",
            "supportive": f"It's okay to feel {feeling}. I'm always here to support you! 💪"
        }
        
        return responses.get(sentiment, f"I understand you're feeling {feeling}. I'm here for you!")
    
    def handle_whatis(self, match, text):
        topic = match.group(1).lower()
        
        # Check math operations
        math_ops = {
            "addition": self.knowledge.get("addition"),
            "subtraction": self.knowledge.get("subtraction"),
            "multiplication": self.knowledge.get("multiplication"),
            "division": self.knowledge.get("division"),
        }
        
        if topic in math_ops:
            return math_ops[topic]
        
        # Check knowledge base
        for key, value in self.knowledge.items():
            if topic in key:
                return value
        
        # Try to learn
        return f"I don't know what {topic} is yet. Would you like to teach me?"
    
    def handle_how(self, match, text):
        if "calculate" in text or "math" in text:
            return "Just tell me what to calculate! Like 'what is 5 + 3'"
        if "work" in text:
            return "I'm your AI companion! I chat, learn, and help. Just talk to me naturally!"
        return "Just ask me and I'll try to help!"
    
    def handle_calculate(self, match, text):
        try:
            # Try to extract and calculate
            if isinstance(match, str):
                result = eval(match)
            else:
                # Use the full text
                expr = text.replace("calculate", "").strip()
                result = eval(expr)
            return f"The answer is {result}! 🧮"
        except:
            return "I can't calculate that. Try something simpler like '5 + 3'"
    
    def handle_teachme(self, match, text):
        return "I'd be happy to teach you! But first, what would you like to learn about?"
    
    def handle_learn(self, match, text):
        return "I love learning from you! Just tell me facts like 'water is H2O' and I'll remember!"
    
    def handle_know(self, match, text):
        topics = list(set([k for k in self.knowledge.keys() if len(k) > 3]))
        return f"I know about: {', '.join(topics[:10])}... and much more! What would you like to know?"
    
    def handle_help(self, match, text):
        return """I can help you with:
📚 Math - Just ask "what is 5 + 5"
🔬 Science - Ask about physics, chemistry
🧠 Memory - I remember what you teach me
💬 Chat - Just talk to me naturally!
🎓 Teach me - Tell me new things

What would you like to do?"""
    
    def handle_thanks(self, match, text):
        return "You're welcome! 😊 I'm always here to help!"
    
    def handle_greeting(self, match, text):
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning! 🌅 How are you today?"
        elif hour < 18:
            return "Good afternoon! ☀️ How can I help you?"
        else:
            return "Good evening! 🌙 How's your day going?"
    
    def handle_goodbye(self, match, text):
        return "Goodbye! Take care! I'll be here when you return! 💫"
