import os
import re

class Config:
    # টেলিগ্রাম API
    API_ID = int(os.environ.get("API_ID", 26111232))
    API_HASH = os.environ.get("API_HASH", "4fc12c70563778156553581f7ed3c9c6")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7506695492:AAEjyL6RbyKuPoSIzpAwUiM_G6-4xt4BAk4")
    
    # ডেটাবেস
    DATABASE_URI = os.environ.get("DATABASE_URI", "mongodb+srv://prentertainment1st:YHCIrZteqxOUNoJH@cluster0.bjabyuc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "Cluster0")
    
    # চ্যানেল ও অ্যাডমিন
    CHANNELS = [int(ch) for ch in os.environ.get("CHANNELS", "-5716904910").split()]
    ADMINS = [int(admin) for admin in os.environ.get("ADMINS", "5716904910").split()]
    
    # অন্যান্য সেটিংস
    CACHE_TIME = int(os.environ.get("CACHE_TIME", 300))
    USE_CAPTION_FILTER = bool(os.environ.get("USE_CAPTION_FILTER", True))

# রেগুলার এক্সপ্রেশন
id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default
      
