from django.shortcuts import render
from django.utils import timezone
import datetime
import requests
import json
from .models import Release
import pytz

# Create your views here.
def home(req):

  if(str(req.user) == "AnonymousUser"):
    return render(req, 'deploys/login.html')

  next_release = determine_next_release()
  master_in_acceptance_for_release = is_master_in_acceptance_for_release(req, next_release)
  soak_in_production_for_release = is_production_deployed(req, next_release)


  master_to_acceptance = latest_merges_for_branches(req, 'master', 'acceptance')
  acceptance_to_soak = latest_merges_for_branches(req, 'acceptance', 'soak')
  soak_to_production = latest_merges_for_branches(req, 'soak', 'production')
  acceptance_to_master = latest_merges_for_branches(req, 'acceptance', 'master')
  context = {
    'master_to_acceptance': master_to_acceptance,
    'acceptance_to_soak': acceptance_to_soak,
    'soak_to_production': soak_to_production,
    'acceptance_to_master': acceptance_to_master,
    'release': next_release,
    'master_in_acceptance_for_release': master_in_acceptance_for_release,
    'soak_in_production_for_release': soak_in_production_for_release
  }
  return render(req, 'deploys/dashboard.html', context)


def determine_next_release():
  future_releases = Release.objects.filter(code_freeze_date__gt=timezone.now())
  if future_releases:
    return future_releases[0]
  else:
    return Release.objects.all().order_by('-code_freeze_date')[0]


def is_master_in_acceptance_for_release(req, release):
  prs = latest_merges_for_branches(req, 'master', 'acceptance', 100)
  for pr in prs:
    dt_no_tz = datetime.datetime.strptime(pr['merged_at'], "%Y-%m-%dT%H:%M:%SZ")
    dt_utc = dt_no_tz.replace(tzinfo=pytz.timezone('UTC'))
    dt_pt = dt_utc.astimezone(pytz.timezone('US/Pacific'))
    if dt_pt > release.code_freeze_date and dt_pt < release.production_release_date:
      print 'in if'
      return "Yes"
  return "No"


def is_production_deployed(req, release):
  prs = latest_merges_for_branches(req, 'soak', 'production', 100)
  for pr in prs:
    dt_no_tz = datetime.datetime.strptime(pr['merged_at'], "%Y-%m-%dT%H:%M:%SZ")
    dt_utc = dt_no_tz.replace(tzinfo=pytz.timezone('UTC'))
    dt_pt = dt_utc.astimezone(pytz.timezone('US/Pacific'))
    if dt_pt > release.code_freeze_date and dt_pt < release.production_release_date + datetime.timedelta(days=2):
      print 'in if'
      return "Yes"
  return "No"


def latest_merges_for_branches(req, head_branch_name, base_branch_name, num_results=5):
  payload = {
    'access_token': req.user.social_auth.filter(provider='github')[0].access_token,
    'per_page': num_results,
    'head': 'AltSchool:%s' % head_branch_name,
    'base': base_branch_name,
    'state': 'closed',
  }
  r = requests.get('https://api.github.com/repos/altschool/vishnu-frontend/pulls', params=payload)
  if(r.ok):
    prs = r.json()
    return prs
  else:
    print 'NOT OK'

def release(req, release_version):
  if(str(req.user) == "AnonymousUser"):
    return render(req, 'deploys/login.html')

  # next_release = determine_next_release()
  release = Release.objects.get(version=release_version)
  master_in_acceptance_for_release = is_master_in_acceptance_for_release(req, release)
  soak_in_production_for_release = is_production_deployed(req, release)


  master_to_acceptance = latest_merges_for_branches(req, 'master', 'acceptance')
  acceptance_to_soak = latest_merges_for_branches(req, 'acceptance', 'soak')
  soak_to_production = latest_merges_for_branches(req, 'soak', 'production')
  acceptance_to_master = latest_merges_for_branches(req, 'acceptance', 'master')
  context = {
    'master_to_acceptance': master_to_acceptance,
    'acceptance_to_soak': acceptance_to_soak,
    'soak_to_production': soak_to_production,
    'acceptance_to_master': acceptance_to_master,
    'release': release,
    'master_in_acceptance_for_release': master_in_acceptance_for_release,
    'soak_in_production_for_release': soak_in_production_for_release
  }
  return render(req, 'deploys/dashboard.html', context)
