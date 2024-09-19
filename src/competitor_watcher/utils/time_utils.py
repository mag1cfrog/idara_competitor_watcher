from datetime import datetime
import pytz

def get_current_timestamp(timezone_str='America/Los_Angeles'):
    timezone = pytz.timezone(timezone_str)
    return datetime.now(pytz.utc).astimezone(timezone).isoformat()
