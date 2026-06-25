import os
import sys
import signal
import logging
import json
import io
import time
import httpx
from google import genai
from PIL import Image
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ─── Logging ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── Gemini client ────────────────────────────────────────────────────────────

gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Disable thinking mode — not needed for JSON extraction, makes responses faster
_FAST_CONFIG = genai.types.GenerateContentConfig(
    thinking_config=genai.types.ThinkingConfig(thinking_budget=0)
)

MODEL = "gemini-2.5-flash"

# ─── Singleton guard ──────────────────────────────────────────────────────────

PID_FILE = "/tmp/quiz_bot.pid"


def enforce_singleton() -> None:
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                old_pid = int(f.read().strip())

