from datetime import datetime
from llm import generate_embeddings, count_tokens
from utils import Logger, vector_similarity

class RelevantMemories:
    def __init__(self):            
        self.memory = []
        self.log = Logger()        

    def add_to_memory(self, role, content):
        memory_item = {
            "timestamp": datetime.now(),
            "token_count": count_tokens(content),
            "role": role,
            "content": content,
            "embedding": generate_embeddings(content)
        }
        self.memory.append(memory_item)
        self.log_memory_update(memory_item)

    def log_memory_update(self, memory_item):
        total_memory_tokens = sum([mem["token_count"] for mem in self.memory])
        self.log.info(
            f"Adding memory item {len(self.memory)} with {memory_item['token_count']} tokens. "
            f"Total memory tokens: {total_memory_tokens}"
        )
                
    def get_relevant_memories(self, query, max_tokens = 2000, sim_k = 0.8, rec_k = 0.25):
        total_memory_tokens = sum([memory_item["token_count"] for memory_item in self.memory])
        if total_memory_tokens < max_tokens:
            return [{"role": memory["role"], "content": memory["content"]} for memory in self.memory]

        self.log.info(f"Executing get_relevant_memories with the following parameters: max_tokens: {max_tokens}, sim_k: {sim_k}, rec_k: {rec_k}, Query: {query}")

        relevant_memories = []
        query_embedding = generate_embeddings(query)

        for memory_index, memory in enumerate(self.memory):
            similarity = vector_similarity(query_embedding, memory["embedding"])
            recency = memory_index / len(self.memory)
            score = (sim_k * similarity) + (rec_k * recency)

            self.log.info(f"Calculating score for memory {memory_index}: Similarity: {similarity} - Recency: {recency} => Score: {score}")

            relevant_memories.append({
                "content": memory["content"],
                "score": score,
                "token_count": memory["token_count"],
                "timestamp" : memory["timestamp"],
                "role" : memory["role"]
            })

        relevant_memories.sort(key=lambda x: x["score"], reverse=True)
        total_token_count = sum(memory["token_count"] for memory in relevant_memories)
        self.log.info("[REMOVED MEMORIES]")
        while total_token_count > max_tokens:
            removed_memory = relevant_memories.pop()
            total_token_count -= removed_memory["token_count"]
            self.log.info(f"Removed memory with {removed_memory['token_count']} tokens.")

        relevant_memories.sort(key=lambda x: x["timestamp"], reverse=False)
        self.log.info("[RELEVANT MEMORIES]")

        relevant_messages = []

        for memory in relevant_memories:
            relevant_messages.append({
                "role" : memory["role"],
                "content": memory["content"]
            })

        return relevant_messages