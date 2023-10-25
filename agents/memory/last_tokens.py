from llm import count_tokens
from utils import Logger
from .last_memories import LastMemories

class LastTokens(LastMemories):
    def __init__(self):            
        super().__init__()
        self.log = Logger()

    def add_to_memory(self, role, content):
        super().add_to_memory(role, content)
        memory_item = self.memory[-1]
        memory_item["token_count"] = count_tokens(content)
        self.log_memory_update(memory_item)

    def log_memory_update(self, memory_item):
        total_memory_tokens = sum([mem.get("token_count", 0) for mem in self.memory])
        self.log.info(
            f"Adding memory item {len(self.memory)} with {memory_item['token_count']} tokens. "
            f"Total memory tokens: {total_memory_tokens}"
        )
    
    def get_last_tokens(self, max_tokens=2000):
        total_memory_tokens = sum([mem.get("token_count", 0) for mem in self.memory])
        if total_memory_tokens < max_tokens:
            return [
                {
                    "role": memory["role"], 
                    "content": memory["content"],
                    "timestamp" : memory["timestamp"]
                } for memory in self.memory][::-1]

        _messages = []
        _tokens = 0
        for memory in reversed(self.memory):
            _tokens += memory.get("token_count", 0)
            if _tokens >= max_tokens:
                break
            
            _messages.append({
                "role": memory["role"],
                "content": memory["content"],
                "timestamp" : memory["timestamp"]
            })
            
        return _messages[::-1]