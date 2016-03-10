#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import json
import argparse
import urllib2
import sys

orgs = []
users = []
branch = []
filename = []

raw_github = "https://raw.githubusercontent.com"
github = "http://github.com"

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, \
                                 description='Search juju-solutions repos for layers and interfaces',
                                 epilog='org, user and branch are all appended arguments, e.g.: \n' \
                                 'gitgetinfo.py -s basic -b master -b featurebranch1 -b featurebranch2' \
                                 ' -u bobsmith -u mikepeters -o org1 -o org2')
parser.add_argument("-s, --search", action="store", help="layer or interface name (or substring)", dest="search")
parser.add_argument("-b, --branch", action="append", help="specify additional branch names (default is master)", dest="branch")
parser.add_argument("-o, --org", action="append", help="specify additional github org names to scan", dest="org")
parser.add_argument("-u, --user", action="append", help="specify additional github user repos to scan", dest="user")
parser.add_argument("-f, --filename", action="append", help="filename to scan in repo for search string", dest="filename")
args = parser.parse_args()

if args.filename:
    for name in args.filename:
        filename.append(name)

if args.org:
    for name in args.org:
        orgs.append(name)

if args.user:
    for name in args.user:
        users.append(name)

if args.branch:
    for name in args.branch:
        branch.append(name)
else:
    branch.append("master")

if not args.search:
    parser.print_help()
    sys.exit(0)
else:
    search = args.search

def scan_org(org, branch, file):
    print "\nScanning {} for {}[{}] in {}...\n".format(org, search, branch, file)
    full_url = 'https://github.com/' + org
    try:
        open_org = urllib2.urlopen(full_url)
    except urllib2.HTTPError as e:
        print "\nBad organisation name, {}\n".format(e)
        sys.exit(1)
    soup = BeautifulSoup(open_org)
    for link in soup.findAll('a'):
        if 'itemprop' in str(link) and 'layer' in str(link):
            scan_url = raw_github + str(link.get('href')) + '/' + branch + '/' + file
            git_url = github + str(link.get('href')) + '/blob/' + branch + '/' + file
            try:
                onions = urllib2.urlopen(scan_url)
                onion_soup = BeautifulSoup(onions)
                d = onion_soup.findAll(text=True)
                for line in d:
                    for line2 in line.strip().split('\n'):
                        if 'include' in line2:
                            if search in line2:
                                print search + " Found in: " + git_url
                                print line2 + "\n"
            except:
                pass

def scan_user(user, branch, filename):
    print "\nScanning {} for {}[{}] in {}...\n".format(user, search, branch, filename)
    full_url = 'https://api.github.com/users/' + user + '/repos?page=1&per_page=100'
    try:
        open_user = urllib2.urlopen(full_url)
    except urllib2.HTTPError as e:
        print "\nBad username, {}\n".format(e)
        sys.exit(1)
    user_data = json.load(open_user)
    for repo in user_data:
        scan_url = raw_github + '/' + repo['full_name'] + '/' + branch + '/' + filename
        git_url = github + '/' + repo['full_name'] + '/blob/' + branch + '/' + filename
        try:
            onions = urllib2.urlopen(scan_url)
            onion_soup = BeautifulSoup(onions)
            d = onion_soup.findAll(text=True)
            for line in d:
                for line2 in line.strip().split('\n'):
                    if search in str(line2):
                        print search + " Found in: " + git_url
                        print line2 + "\n"
        except:
            pass

if orgs:
    for org in orgs:
        for br in branch:
            for fn in filename:
                scan_org(org, br, fn)

if users:
    for user in users:
        for br in branch:
            for fn in filename:
                scan_user(user, br, fn)
