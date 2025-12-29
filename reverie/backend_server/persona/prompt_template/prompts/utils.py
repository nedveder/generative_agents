"""
Utility functions for prompt generation.
"""
import random
import string
import json


def get_random_alphanumeric(i=6, j=6):
    """
    Returns a random alpha numeric string that has the length of somewhere
    between i and j.

    INPUT:
        i: min_range for the length
        j: max_range for the length
    OUTPUT:
        an alpha numeric str with the length of somewhere between i and j.
    """
    k = random.randint(i, j)
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return x


def extract_first_json_dict(data_str):
    """
    Extract the first JSON dictionary from a string.

    INPUT:
        data_str: String potentially containing JSON
    OUTPUT:
        Parsed JSON dict or None if not found/invalid
    """
    # Find the first occurrence of a JSON object within the string
    start_idx = data_str.find('{')
    end_idx = data_str.find('}', start_idx) + 1

    # Check if both start and end indices were found
    if start_idx == -1 or end_idx == 0:
        return None

    # Extract the first JSON dictionary
    json_str = data_str[start_idx:end_idx]

    try:
        # Attempt to parse the JSON data
        json_dict = json.loads(json_str)
        return json_dict
    except json.JSONDecodeError:
        # If parsing fails, return None
        return None
