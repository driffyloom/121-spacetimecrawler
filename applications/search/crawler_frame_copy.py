import logging
from datamodel.search.Biancat1Achiang5_datamodel import Biancat1Achiang5Link, OneBiancat1Achiang5UnProcessedLink
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4

from urlparse import urlparse, parse_qs
from uuid import uuid4
from datetime import datetime
from collections import defaultdict


logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"
outlinksDict = defaultdict(int)

URLDict = defaultdict(int)
numberOfSitesVisited = 0
outLinksDict = defaultdict(int)
subdomainDict = defaultdict(int)


'''
Subdomain Parse code found from: https://docs.python.org/2/library/urlparse.html
'''

@Producer(Biancat1Achiang5Link)
@GetterSetter(OneBiancat1Achiang5UnProcessedLink)
class CrawlerFrame(IApplication):
    app_id = "Biancat1Achiang5"

    def __init__(self, frame):
        self.app_id = "Biancat1Achiang5"
        self.frame = frame


    def initialize(self):
        self.count = 0
        links = self.frame.get_new(OneBiancat1Achiang5UnProcessedLink)
        if len(links) > 0:
            print "Resuming from the previous state."
            self.download_links(links)
        else:
            l = Biancat1Achiang5Link("http://www.ics.uci.edu/")
            print l.full_url
            self.frame.add(l)

    def update(self):
        unprocessed_links = self.frame.get_new(OneBiancat1Achiang5UnProcessedLink)
        if unprocessed_links:
            self.download_links(unprocessed_links)

    def download_links(self, unprocessed_links):
        for link in unprocessed_links:
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            links = extract_next_links(downloaded)
            for l in links:
                if is_valid(l):
                    self.frame.add(Biancat1Achiang5Link(l))

    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")
    
def extract_next_links(rawDataObj):
    outputLinks = []
    '''
    rawDataObj is an object of type UrlResponse declared at L20-30
    datamodel/search/server_datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded. 
    The frontier takes care of that.
    
    Suggested library: lxml
    '''
    try:
        outgoing = 0
        pageHTMLDoc = lxml.html.fromstring(rawDataObj.content) #nice and correct HTML document
        pageHTMLDoc.make_links_absolute(rawDataObj.url)
        for element, attribute, link, pos in pageHTMLdoc.iterlinks():
            if element == "a" and attribute == "href":
                if "?" not in url and "#"  not in url:
                    outputLinks.append(link)
                    outgoing += 1
        #associate each url (rawDataObj.url) with the number of outgoing links on that page
        if "?" not in url and "#"  not in url:
            outlinksDict[rawDataObj.url] += 1
        return outputLinks
    except:
        print("Error met with rawDataObj content: ", rawDataObj.content)

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    '''
    
    parsed = urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
        return False

    if "?" in url or "#" in url:
        return False;
    
    parsedURL = urlparse(url)
    subdomain = parsedURL.hostname.split('.')[0]
    if subdomain != "":
        subdomainDict[subdomain] += 1

    #adds url to dictionary and increments it's count
    URLDict[url]+=1

    #if we've visited the same website over 10 times stop
    if URLDict[url] >= 10:
        return False;

    global numberOfSitesVisited
    
    numberOfSitesVisited+=1
    
    if numberOfSitesVisited == 3000:

        currentDay = datetime.now()

        subdomainFile = open('subdomains_' + str(currentDay.month) + '-' \
                              + str(currentDay.day) + '-' + str(currentDay.year) + 'TIME' + str(date.hour) + '-' + str(date.minute) + '-' \
                              + str(currentDay.second) + '.txt', 'w+')

        subdomainFile.write('Subdomains and Counts:')
        for subdomain, subdomainCount in sorted(subdomainDict.items(), key = lambda x: x[1], reverse = True):
            if value == -1:
                pass
            else:
                subdomainFile.write(str(subdomain) + ' num: ' + str(subdomainCount) + '\n')

        outLinksFile = open('outLinks_' + str(currentDay.year) + '-' + str(currentDay.month) + '-' \
                                    + str(currentDay.day) + 'TIME' + str(currentDay.hour) + '-' + str(date.minute) + '-' \
                                    + str(currentDay.second) + '.txt', 'w+')
        
        outLinksFile.write('Domains and links going out:')
        for domain, numOutLinks in sorted(outLinksDict.items(), key = lambda x: x[1], reverse = True):
            createHighestLinkFile.write(str(domain) + ' Outlinks: ' + str(numOutLinks) + '\n')


        subdomainFile.close()
        outgoingLinksFile.close()

        print("Done parsing 3000 links! Check folder for results")
    
    
    try:

        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False

