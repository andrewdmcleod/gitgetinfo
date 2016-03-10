# gitgetinfo

Tool for finding STRING in FILENAME in github ORG or USERNAME repos.

## Dependencies

BeautifulSoup

	pip install beautifulsoup

## limits 
The org query just does an http get - so the following limits do not apply.
 
For user repo queries:
	* api.github.com allows 1 request per minute for non-authenticated users
	* only returns first 100 repos

## Usage

usage: gitgetinfo.py [-h] [-s, --search SEARCH] [-b, --branch BRANCH]
                     [-o, --org ORG] [-u, --user USER]
                     [-f, --filename FILENAME]

Search juju-solutions repos for layers and interfaces

optional arguments:
  -h, --help            show this help message and exit
  -s, --search SEARCH   layer or interface name (or substring)
  -b, --branch BRANCH   specify additional branch names (default is master)
  -o, --org ORG         specify additional github org names to scan
  -u, --user USER       specify additional github user repos to scan
  -f, --filename FILENAME
                        filename to scan in repo for search string

org, user and branch are all appended arguments, e.g.: 

gitgetinfo.py -s basic -b master -b featurebranch1 -b featurebranch2 -u bobsmith -u mikepeters -o org1 -o org2

or a simpler example:

gitgetinfo.py -s hadoop-client -b ha -b master -o org1 -u johndoe 
