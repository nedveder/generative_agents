"""
Constants and configuration values for the generative agents simulation.

This file centralizes all magic numbers, thresholds, and configuration
values that were previously hardcoded throughout the codebase.
"""
import datetime

# ============================================================================
# TIME CONSTANTS
# ============================================================================
HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60

# Base date for time calculations (can be overridden by persona.scratch.curr_time)
# Note: This should generally be derived from the simulation's current time
DEFAULT_BASE_DATE = datetime.datetime(2022, 10, 31, 0, 0)

# ============================================================================
# SCHEDULING CONSTANTS
# ============================================================================
# Minimum number of unique activities for a diverse schedule
MIN_ACTIVITY_DIVERSITY = 5

# Maximum number of retries for schedule generation
MAX_SCHEDULE_GENERATION_RETRIES = 2

# Maximum retries for any GPT prompt before using fail-safe
MAX_GPT_RETRIES = 5

# ============================================================================
# MEMORY & COGNITION CONSTANTS
# ============================================================================
# Poignancy thresholds (1-10 scale)
MIN_POIGNANCY_THRESHOLD = 1
MAX_POIGNANCY_THRESHOLD = 10

# Number of focal points to generate during reflection
DEFAULT_FOCAL_POINTS_COUNT = 3

# ============================================================================
# CONVERSATION CONSTANTS
# ============================================================================
# Minimum time between conversations with same person (minutes)
MIN_CONVERSATION_COOLDOWN = 10

# Maximum conversation length (number of utterances)
MAX_CONVERSATION_LENGTH = 50

# ============================================================================
# SPATIAL CONSTANTS
# ============================================================================
# Path finding constants
MAX_PATH_FINDING_ITERATIONS = 1000

# ============================================================================
# LLM PARAMETERS (Defaults - can be overridden per function)
# ============================================================================
# Note: Model selection is in utils.py (ACTIVE_CHAT_MODEL, etc.)

DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 1.0
DEFAULT_FREQUENCY_PENALTY = 0.0
DEFAULT_PRESENCE_PENALTY = 0.0

# Max tokens for different types of prompts
MAX_TOKENS_SHORT_RESPONSE = 50      # For simple choices/keywords
MAX_TOKENS_MEDIUM_RESPONSE = 500    # For descriptions/summaries
MAX_TOKENS_LONG_RESPONSE = 1000     # For detailed plans/conversations
MAX_TOKENS_VERY_LONG_RESPONSE = 2000  # For complex multi-part responses

# ============================================================================
# DEBUG & LOGGING
# ============================================================================
# Whether to print debug information (should match utils.debug)
DEBUG_MODE = True

# Log file name
LOG_FILE = "generative_agents.log"
