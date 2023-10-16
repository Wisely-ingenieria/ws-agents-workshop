from datetime import datetime
from llm import count_tokens
from utils import Logger

class LastMemories:
    def __init__(self):            
        self.memory = []
        self.log = Logger()        

    def add_to_memory(self, role, content):
        memory_item = {
            "timestamp": datetime.now(),
            "token_count": count_tokens(content),
            "role": role,
            "content": content
        }
        self.memory.append(memory_item)
        self.log_memory_update(memory_item)

    def log_memory_update(self, memory_item):
        total_memory_tokens = sum([mem["token_count"] for mem in self.memory])
        self.log.info(
            f"Adding memory item {len(self.memory)} with {memory_item['token_count']} tokens. "
            f"Total memory tokens: {total_memory_tokens}"
        )
        
    def get_last_memories(self, n=5):
        if n > len(self.memory):
            n = len(self.memory)

        last_memories = []
        for i in range(1, n+1):
            memory = self.memory[-i]
            last_memories.append({
                "role": memory["role"],
                "content": memory["content"]
            })

        return last_memories