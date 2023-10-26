from datetime import datetime

class LastMemories:
    def __init__(self):            
        self.memory = []

    def add_to_memory(self, role, content):
        memory_item = {
            "timestamp": datetime.now(),
            "role": role,
            "content": content
        }
        self.memory.append(memory_item)
    
    def clean_memory(self):
        self.memory = []
        
    def get_last_memories(self, n=5):
        if n > len(self.memory):
            n = len(self.memory)

        last_memories = []
        for i in range(1, n+1):
            memory = self.memory[-i]
            last_memories.append({
                "role": memory["role"],
                "content": memory["content"],
                "timestamp" : memory["timestamp"]
            })

        return last_memories[::-1]