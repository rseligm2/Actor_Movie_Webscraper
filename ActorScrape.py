from bs4 import BeautifulSoup
import unicodedata
import json
import urllib3
import certifi
import unicodedata
import re
import string

class ActorScrape:

    checkedlinks = []

    def __init__(self, url):
        self._url = url

    def create_actor(self):
        #get url
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', self._url)
        soup = BeautifulSoup(response.data, features="html.parser")
        for link in self.checkedlinks:
            if link == self._url:
                print("Already been to " + self._url)
                return
        print("Getting actor info from " + self._url)
        self.checkedlinks.append(self._url)
        #extract div with filmograhy and bio div and create actor object
        biodiv = soup.find("table", {"class": "infobox biography vcard"})
        if biodiv == None:
            biodiv = soup.find("table", {"class": "infobox vcard"})
        namestr = soup.find("h1", {"id": "firstHeading"}).text
        if biodiv != None:
            agestr = biodiv.find("span", {"class": "noprint ForceAgeToShow"})
        else:
            agestr = None
        if agestr == None:
            actage = -1
        else:
            agestr = agestr.text
            agestr = unicodedata.normalize('NFKD', agestr).encode('ascii', 'ignore')
            actage = int(filter(str.isdigit, agestr))

        printable = set(string.printable)
        filter(lambda x: x in printable, namestr)

        actor = Actor(namestr, actage)
        print("created " + str(actor))
        return actor

    def get_films(self):
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', self._url)
        soup = BeautifulSoup(response.data, features="html.parser")
        print("Getting filmography from " + self._url)
        filmography = soup.find("div", {"class": "div-col columns column-width"})
        movies = []
        if filmography == None:
            return movies
        for i in filmography.find_all('i'):
            moviename = unicodedata.normalize('NFKD', i.text).encode('ascii', 'ignore')
            linktext = None
            for link in i.find_all('a'):
                linktext = link.get('href')
            if linktext == None:
                print("No link for movie")
                continue

            linktext = "https://en.wikipedia.org" + linktext
            movie = Movie(moviename, linktext)
            moviescrape = MovieScrape(movie)
            moviescrape.updatemovieinfo()
            movies.append(movie)

        return movies





