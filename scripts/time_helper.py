from datetime import datetime, timedelta
import pytz

TIME_FORMAT = "%Y-%m-%d %R"
NANOSECONDS = 1_000_000_000

def time_params():
    now = datetime.utcnow()
    return {
        'start': (now - timedelta(days=1)).strftime(TIME_FORMAT),
        'end': now.strftime(TIME_FORMAT),
    }

def format_ts(timestamp):
    return int(datetime.fromisoformat(timestamp).timestamp()) * NANOSECONDS
