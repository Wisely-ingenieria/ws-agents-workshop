import openai
import os
import tiktoken
from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import load_dotenv
from utils import Logger

# Logger
logger = Logger()

# Load secrets and config from .env file
load_dotenv()

# OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL")

# Model endpoint names
gpt35_model = os.getenv("OPENAI_GPT35_MODEL")
gpt35_16k_model = os.getenv("OPENAI_GPT35_16K_MODEL")
gpt4_model = os.getenv("OPENAI_GPT4_MODEL")

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def generate_text(prompt, model=gpt35_model, messages=[], max_tokens=-1, temperature=1.0, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=None):
    _messages = []
    for msg in messages:
        _messages.append({"role": msg.get("role",""), "content": msg.get("content","")})
    _messages.append({"role": "user", "content": prompt})
    
    _log_message = "\n\n============================ PROMPT ============================\n"
    for message in _messages:
        _log_message += f"{message['role']}: {message['content']}\n"
    logger.info(_log_message)
    
    if max_tokens == -1:
        max_tokens = None
        
    response = openai.ChatCompletion.create(
        model=model,
        messages=_messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    _log_message = "\n\n============================ RESPONSE ============================\n"
    _log_message += f"{response}\n"
    logger.info(_log_message)
    
    return response["choices"][0]["message"]["content"]

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def generate_text_with_function_call(prompt, model=gpt35_model, messages=[], functions=[], max_tokens=-1, temperature=1.0, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=None, function_call='auto'):
    _messages = []
    _messages.extend(messages)
    _messages.append({"role": "user", "content": prompt})

    _log_message = "\n\n============================ FUNCTION CALL ============================\n"
    _log_message += "Functions:\n"
    for function in functions:
        _log_message += f"{function}\n"
    
    _log_message += "Messages:\n"
    for message in _messages:
        _log_message += f"{message['role']}: {message['content']}\n"
        
    logger.info(_log_message)
    
    if max_tokens == -1:
        max_tokens = None

    response = openai.ChatCompletion.create(
        model=model,
        messages=_messages,
        functions=functions,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
        function_call=function_call
    )
    _log_message = "\n\n============================ RESPONSE ============================\n"
    _log_message += f"{response}\n"
    logger.info(_log_message)
    
    if "function_call" in response["choices"][0]["message"]:
        return response["choices"][0]["message"]["function_call"]
    else:
        return None
    

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def generate_embeddings(text):
    response = openai.Embedding.create(input=text, engine=embedding_model)
    embeddings = response["data"][0]['embedding']
    return embeddings

def count_tokens(input_txt=""):
    if not input_txt:
        return 0
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(enc.encode(input_txt, disallowed_special=()))