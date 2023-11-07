from datetime import datetime, timedelta
import pytz

TIME_FORMAT = "%Y-%m-%d %R"
NANOSECONDS = 1_000_000_000

def time_params(coverage):
    now = datetime.utcnow()
    if coverage == 5:
        return {
            'start': now.replace(hour=0, minute=0).strftime(TIME_FORMAT),
            'end': now.strftime(TIME_FORMAT),
        }
    else:        
        return {
            'start': (now - timedelta(days=coverage)).strftime(TIME_FORMAT),
            'end': now.strftime(TIME_FORMAT),
        }


def format_ts(timestamp):
    return int(datetime.fromisoformat(timestamp).timestamp()) * NANOSECONDS
