# memory.py
import json
import os
from datetime import datetime

class Memory:
    def __init__(self):
        self.data_dir = "data"
        self.memories_file = os.path.join(self.data_dir, "memories.json")
        self.conversation_file = os.path.join(self.data_dir, "conversation.json")
        self.facts_file = os.path.join(self.data_dir, "facts.json")
        
        # Create data directory if not exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load existing memories
        self.memories = self.load_json(self.memories_file, {})
        self.conversation = self.load_json(self.conversation_file, [])
        self.facts = self.load_json(self.facts_file, {})
    
    def load_json(self, filepath, default):
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def save_json(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Remember new things user teaches
    def remember(self, key, value):
        """Store a new fact or memory"""
        self.memories[key.lower()] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self.save_json(self.memories_file, self.memories)
        print(f"💭 Memory saved: {key}")
    
    # Remember conversation
    def add_conversation(self, role, message):
        """Add to conversation history"""
        self.conversation.append({
            "role": role,
            "message": message,
            "time": datetime.now().strftime("%H:%M")
        })
        # Keep last 100 messages
        if len(self.conversation) > 100:
            self.conversation = self.conversation[-100:]
        self.save_json(self.conversation_file, self.conversation)
    
    # Recall from memory
    def recall(self, query):
        """Search memory for something"""
        query = query.lower()
        
        # Search facts
        for key, value in self.facts.items():
            if query in key.lower() or query in str(value).lower():
                return f"I remember: {key} = {value}"
        
        # Search memories
        for key, value in self.memories.items():
            if query in key.lower() or query in str(value.get('value', '')).lower():
                return f"I remember: {key} = {value.get('value', '')}"
        
        return None
    
    # Teach new fact
    def teach(self, statement):
        """Learn new information from user"""
        # Try to parse "X is Y" or "X = Y"
        separators = [' is ', ' = ', ' called ', ' means ']
        
        for sep in separators:
            if sep in statement:
                parts = statement.split(sep, 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    self.facts[key.lower()] = value
                    self.save_json(self.facts_file, self.facts)
                    return f"Got it! I'll remember that {key} is {value} 😊"
        
        # Store as general memory
        self.remember(statement, "User taught me this")
        return "Okay, I've learned that! Thank you for teaching me 🙏"
    
    def get_recent_conversation(self, count=5):
        return self.conversation[-count:] if self.conversation else []