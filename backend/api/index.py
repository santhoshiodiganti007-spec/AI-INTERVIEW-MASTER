import sys
import os

# Ensure backend root is in sys.path for Vercel Serverless Functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

handler = app

