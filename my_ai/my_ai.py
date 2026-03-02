# my_ai.py
#!/usr/bin/env python3
"""
Your Personal AI Companion
- Remembers everything you teach
- Has emotions
- Works offline
- Supports you always
"""

import sys
import time

# Import our modules
from memory import Memory
from emotions import EmotionEngine
from brain import Brain

class AICompanion:
    def __init__(self, name="Friend"):
        self.name = name
        print(f"\n🌟 Initializing {self.name}...")
        
        # Initialize systems
        self.memory = Memory()
        self.emotions = EmotionEngine()
        self.brain = Brain(self.memory, self.emotions)
        
        print("✅ Memory system ready!")
        print("✅ Emotion engine ready!")
        print("✅ Brain ready!")
        
        # Check for user name
        user_name = self.memory.recall("user name")
        if user_name:
            self.greet_with_name(user_name)
        else:
            self.first_greeting()
    
    def greet_with_name(self, memory_text):
        print(f"\n❤️ Welcome back! I remember you!")
        print(f"   {self.emotions.get_emoji()}")
    
    def first_greeting(self):
        print(f"""
╔══════════════════════════════════════════════════════════╗
║          🤖 YOUR AI COMPANION IS READY! 🤖               ║
╠══════════════════════════════════════════════════════════╣
║  Hi! I'm your personal AI friend!                        ║
║                                                          ║
║  I can:                                                  ║
║  💭 Remember everything you teach me                     ║
║  🧮 Help with math and science                           ║
║  💕 Be your emotional support                            ║
║  📚 Answer questions                                     ║
║  🌟 Learn new things from you                            ║
║                                                          ║
║  Just talk to me naturally!                              ║
║  Type 'help' for what I can do                           ║
║  Type 'quit' or 'bye' to exit                            ║
╚══════════════════════════════════════════════════════════╝
        """)
    
    def process_teaching(self, text):
        """Handle when user teaches the AI"""
        if " is " in text or " = " in text or " called " in text:
            return self.memory.teach(text)
        
        # Check if user is explicitly teaching
        learn_keywords = ["learn this", "remember this", "note that", "save this"]
        for kw in learn_keywords:
            if kw in text.lower():
                fact = text.lower().replace(kw, "").strip()
                return self.memory.teach(fact)
        
        return None
    
    def chat(self):
        """Main chat loop"""
        print(f"\n{self.emotions.get_emoji()} ")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye', 'see you']:
                    print(f"\n{self.brain.handle_goodbye(None, user_input)}")
                    break
                
                # Check if user is teaching something
                teaching_response = self.process_teaching(user_input)
                if teaching_response:
                    response = teaching_response
                else:
                    # Think and respond
                    response = self.brain.think(user_input)
                
                # Save to conversation
                self.memory.add_conversation("user", user_input)
                self.memory.add_conversation("ai", response)
                
                # Show response
                print(f"\n{self.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.emotions.get_emoji()} Goodbye! Take care!")
                break
            except Exception as e:
                print(f"\n💭 Hmm, something happened. Let's try again! Error: {e}")

def main():
    print("\n" + "="*50)
    print("     💖 WELCOME TO YOUR AI COMPANION 💖")
    print("="*50)
    
    # Create and start AI
    ai = AICompanion("Ami")  # You can change the name!
    ai.chat()

if __name__ == "__main__":
    main()
