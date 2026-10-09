import os
import sys

# ============================================

# Resource Path

# ============================================

def resource_path(relative_path):
  """Get the correct path for development and PyInstaller builds."""
  if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
  else:
    base_path = os.path.dirname(os.path.abspath(__file__))

  return os.path.join(base_path, relative_path)


# ============================================

# Food Ordering App Configuration

# ============================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "food_ordering_app")

# Application

APP_NAME = "Food Ordering App"

# GST

GST_RATE = 18

# Assets

LOGO_PATH = resource_path("assets/logo.png")
FOOD_IMAGE_FOLDER = resource_path("assets/food")
ICON_FOLDER = resource_path("assets/icons")
SQL_FILE_PATH = resource_path("sql/food_ordering_app.sql")
