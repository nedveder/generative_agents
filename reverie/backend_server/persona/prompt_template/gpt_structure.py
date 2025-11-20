"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling OpenAI APIs.
"""
import json
import random
import logging
from openai import OpenAI, RateLimitError, APIError, APITimeoutError
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import time

from utils import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('generative_agents.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=openai_api_key)

# API usage tracking
class APIUsageTracker:
    def __init__(self):
        self.total_requests = 0
        self.total_tokens = 0
        self.failed_requests = 0

    def log_request(self, success=True, tokens=0):
        self.total_requests += 1
        if success:
            self.total_tokens += tokens
        else:
            self.failed_requests += 1

        if self.total_requests % 10 == 0:
            logger.info(f"API Stats - Total: {self.total_requests}, Tokens: {self.total_tokens}, Failed: {self.failed_requests}")

usage_tracker = APIUsageTracker()

def temp_sleep(seconds=0.1):
  time.sleep(seconds)

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError))
)
def ChatGPT_single_request(prompt):
  temp_sleep()

  try:
    completion = client.chat.completions.create(
      model=ACTIVE_CHAT_MODEL,
      messages=[{"role": "user", "content": prompt}]
    )
    tokens = completion.usage.total_tokens if hasattr(completion, 'usage') else 0
    usage_tracker.log_request(success=True, tokens=tokens)
    return completion.choices[0].message.content
  except (RateLimitError, APITimeoutError, APIError) as e:
    logger.error(f"API error in ChatGPT_single_request: {str(e)}")
    usage_tracker.log_request(success=False)
    raise  # Let retry decorator handle it
  except Exception as e:
    logger.error(f"Unexpected error in ChatGPT_single_request: {str(e)}")
    usage_tracker.log_request(success=False)
    raise


# ============================================================================
# #####################[SECTION 1: CHATGPT-3 STRUCTURE] ######################
# ============================================================================

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError))
)
def GPT4_request(prompt):
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response.
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of
                   the parameter and the values indicating the parameter
                   values.
  RETURNS:
    a str of GPT-4's response.
  """
  temp_sleep()

  try:
    completion = client.chat.completions.create(
      model=ACTIVE_CHAT_MODEL,
      messages=[{"role": "user", "content": prompt}]
    )
    tokens = completion.usage.total_tokens if hasattr(completion, 'usage') else 0
    usage_tracker.log_request(success=True, tokens=tokens)
    return completion.choices[0].message.content

  except (RateLimitError, APITimeoutError, APIError) as e:
    logger.error(f"API error in GPT4_request: {str(e)}")
    usage_tracker.log_request(success=False)
    raise  # Let retry decorator handle it
  except Exception as e:
    logger.error(f"Unexpected error in GPT4_request: {str(e)}")
    usage_tracker.log_request(success=False)
    return "ChatGPT ERROR"


@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError))
)
def ChatGPT_request(prompt):
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response.
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of
                   the parameter and the values indicating the parameter
                   values.
  RETURNS:
    a str of GPT-4's response.
  """
  # temp_sleep()
  try:
    completion = client.chat.completions.create(
      model=ACTIVE_CHAT_MODEL,
      messages=[{"role": "user", "content": prompt}]
    )
    tokens = completion.usage.total_tokens if hasattr(completion, 'usage') else 0
    usage_tracker.log_request(success=True, tokens=tokens)
    return completion.choices[0].message.content

  except (RateLimitError, APITimeoutError, APIError) as e:
    logger.error(f"API error in ChatGPT_request: {str(e)}")
    usage_tracker.log_request(success=False)
    raise  # Let retry decorator handle it
  except Exception as e:
    logger.error(f"Unexpected error in ChatGPT_request: {str(e)}")
    usage_tracker.log_request(success=False)
    return "ChatGPT ERROR"


def GPT4_safe_generate_response(prompt, 
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat): 

    try: 
      curr_gpt_response = GPT4_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass

  return False


def ChatGPT_safe_generate_response(prompt, 
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  # prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt = '"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat): 

    try: 
      curr_gpt_response = ChatGPT_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]

      # print ("---ashdfaf")
      # print (curr_gpt_response)
      # print ("000asdfhia")
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass

  return False


def ChatGPT_safe_generate_response_OLD(prompt, 
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat): 
    try: 
      curr_gpt_response = ChatGPT_request(prompt).strip()
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      if verbose: 
        print (f"---- repeat count: {i}")
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass
  print ("FAIL SAFE TRIGGERED") 
  return fail_safe_response


# ============================================================================
# ###################[SECTION 2: ORIGINAL GPT-3 STRUCTURE] ###################
# ============================================================================

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError))
)
def GPT_request(prompt, gpt_parameter):
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response.
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of
                   the parameter and the values indicating the parameter
                   values.
  RETURNS:
    a str of GPT-3.5's response.
  """
  temp_sleep()
  try:
    response = client.completions.create(
                model=gpt_parameter["engine"],
                prompt=prompt,
                temperature=gpt_parameter["temperature"],
                max_tokens=gpt_parameter["max_tokens"],
                top_p=gpt_parameter["top_p"],
                frequency_penalty=gpt_parameter["frequency_penalty"],
                presence_penalty=gpt_parameter["presence_penalty"],
                stream=gpt_parameter["stream"],
                stop=gpt_parameter["stop"],)
    tokens = response.usage.total_tokens if hasattr(response, 'usage') else 0
    usage_tracker.log_request(success=True, tokens=tokens)
    return response.choices[0].text
  except (RateLimitError, APITimeoutError, APIError) as e:
    logger.error(f"API error in GPT_request: {str(e)}")
    usage_tracker.log_request(success=False)
    raise  # Let retry decorator handle it
  except Exception as e:
    logger.error(f"Unexpected error in GPT_request: {str(e)}")
    usage_tracker.log_request(success=False)
    return "TOKEN LIMIT EXCEEDED"


def generate_prompt(curr_input, prompt_lib_file): 
  """
  Takes in the current input (e.g. comment that you want to classifiy) and 
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this 
  function replaces this substr with the actual curr_input to produce the 
  final promopt that will be sent to the GPT3 server. 
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file. 
  RETURNS: 
    a str prompt that will be sent to OpenAI's GPT server.  
  """
  if type(curr_input) == type("string"): 
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):   
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt: 
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()


def safe_generate_response(prompt, 
                           gpt_parameter,
                           repeat=5,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False): 
  if verbose: 
    print (prompt)

  for i in range(repeat): 
    curr_gpt_response = GPT_request(prompt, gpt_parameter)
    if func_validate(curr_gpt_response, prompt=prompt): 
      return func_clean_up(curr_gpt_response, prompt=prompt)
    if verbose: 
      print ("---- repeat count: ", i, curr_gpt_response)
      print (curr_gpt_response)
      print ("~~~~")
  return fail_safe_response


@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError))
)
def get_embedding(text, model=None):
  if model is None:
    model = ACTIVE_EMBEDDING_MODEL

  text = text.replace("\n", " ")
  if not text:
    text = "this is blank"

  try:
    response = client.embeddings.create(input=[text], model=model)
    tokens = response.usage.total_tokens if hasattr(response, 'usage') else 0
    usage_tracker.log_request(success=True, tokens=tokens)
    return response.data[0].embedding
  except (RateLimitError, APITimeoutError, APIError) as e:
    logger.error(f"API error in get_embedding: {str(e)}")
    usage_tracker.log_request(success=False)
    raise
  except Exception as e:
    logger.error(f"Unexpected error in get_embedding: {str(e)}")
    usage_tracker.log_request(success=False)
    raise


if __name__ == '__main__':
  gpt_parameter = {"engine": "gpt-3.5-turbo-instruct", "max_tokens": 50, 
                   "temperature": 0, "top_p": 1, "stream": False,
                   "frequency_penalty": 0, "presence_penalty": 0, 
                   "stop": ['"']}
  curr_input = ["driving to a friend's house"]
  prompt_lib_file = "prompt_template/test_prompt_July5.txt"
  prompt = generate_prompt(curr_input, prompt_lib_file)

  def __func_validate(gpt_response): 
    if len(gpt_response.strip()) <= 1:
      return False
    if len(gpt_response.strip().split(" ")) > 1: 
      return False
    return True
  def __func_clean_up(gpt_response):
    cleaned_response = gpt_response.strip()
    return cleaned_response

  output = safe_generate_response(prompt, 
                                 gpt_parameter,
                                 5,
                                 "rest",
                                 __func_validate,
                                 __func_clean_up,
                                 True)

  print (output)




















