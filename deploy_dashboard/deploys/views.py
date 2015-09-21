from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
import datetime
import requests
import json
from .models import Release
import pytz

def home(req):

  if(str(req.user) == "AnonymousUser"):
    return render(req, 'deploys/login.html')
  if not user_is_member_of_altschool(req.user):
    return HttpResponse("You are not a member of Altschool. Go away.")

  next_release = determine_next_release()
  return redirect('/releases/%s' % next_release.version)

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
      return "Yes"
  return "No"


def is_production_deployed(req, release):
  prs = latest_merges_for_branches(req, 'soak', 'production', 100)
  for pr in prs:
    dt_no_tz = datetime.datetime.strptime(pr['merged_at'], "%Y-%m-%dT%H:%M:%SZ")
    dt_utc = dt_no_tz.replace(tzinfo=pytz.timezone('UTC'))
    dt_pt = dt_utc.astimezone(pytz.timezone('US/Pacific'))
    if dt_pt > release.code_freeze_date and dt_pt < release.production_release_date + datetime.timedelta(days=2):
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

def releases(req):
  releases = Release.objects.order_by('-production_release_date').all()
  return render(req, 'deploys/releases.html', {'releases': releases})

def release(req, release_version):
  if(str(req.user) == "AnonymousUser"):
    return render(req, 'deploys/login.html')


  release_version = release_version.rstrip('/')
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

def user_is_member_of_altschool(user):
    url = 'https://api.github.com/user/memberships/orgs?access_token=%s' % user.social_auth.filter(provider='github')[0].access_token
    r = requests.get(url)
    if(r.ok):
      orgs = r.json()
      org_names = [org['organization']['login'] for org in orgs]
      if 'AltSchool' in org_names:
        return True
    return False

