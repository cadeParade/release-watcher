from django import template
from datetime import datetime
import pytz

register = template.Library()

@register.filter
def format_time(var="idk"):
  dt_no_tz = datetime.strptime(var, "%Y-%m-%dT%H:%M:%SZ")
  dt_utc = dt_no_tz.replace(tzinfo=pytz.timezone('UTC'))
  dt_pt = dt_utc.astimezone(pytz.timezone('US/Pacific'))
  return dt_pt.strftime("%a, %b %d -- %I:%M %p")
