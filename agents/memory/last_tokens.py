from datetime import datetime
from llm import count_tokens
from utils import Logger

class LastTokens:
    def __init__(self, max_tokens=2000):            
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
    
    def get_last_tokens(self, max_tokens=2000):
        total_memory_tokens = sum([mem["token_count"] for mem in self.memory])
        if total_memory_tokens < max_tokens:
            return [{"role": memory["role"], "content": memory["content"]} for memory in self.memory]

        last_tokens = []
        for memory in reversed(self.memory):
            last_tokens.append({
                "role": memory["role"],
                "content": memory["content"]
            })
            total_memory_tokens -= memory["token_count"]
            if total_memory_tokens < max_tokens:
                break

        return last_tokens
