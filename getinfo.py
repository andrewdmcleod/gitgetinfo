#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import argparse
import urllib2
import sys

orgs = []
branch = []
parser = argparse.ArgumentParser(description='Search juju-solutions repos for layers and interfaces')
parser.add_argument("-s, --search", action="store", help="layer or interface name (or substring)", dest="search")
parser.add_argument("-b, --branch", action="append", help="specify additional branch names (default is master)", dest="branch")
parser.add_argument("-o, --org", action="append", help="specify additional github org/namespaces (full url) to scan\
                                                        e.g. -o http://www.github.com/your_user_name/", dest="org")
args = parser.parse_args()
search = args.search
if args.org:
    for name in args.org:
        orgs.append(name)

if args.branch:
    for name in args.branch:
        branch.append(name)
else:
    branch.append("master")

if not search:
    parser.print_help()
    sys.exit(0)

raw_github = "https://raw.githubusercontent.com"
github = "http://github.com"
orgs.append("http://github.com/juju-solutions")

def scan_org(org, branch):
    print "\nScanning {} for {} in layer.yaml...\n".format(org, search)
    open_org = urllib2.urlopen(org)
    soup = BeautifulSoup(open_org)
    for link in soup.findAll('a'):
        if 'itemprop' in str(link) and 'layer' in str(link):
            scan_url = raw_github + str(link.get('href')) + '/' + branch + '/layer.yaml'
            git_url = github + str(link.get('href')) + '/blob/' + branch + '/layer.yaml'
            onions = urllib2.urlopen(scan_url)
            onion_soup = BeautifulSoup(onions)
            d = onion_soup.findAll(text=True)
            for line in d:
                for line2 in line.strip().split('\n'):
                    if 'include' in line2:
                        if search in line2:
                            print search + " Found in: " + git_url
                            print line2 + "\n"

for org in orgs:
    for br in branch:
        scan_org(org, br)
