from Movie import Movie
from Actor import Actor
from bs4 import BeautifulSoup
import unicodedata
import json
import urllib3
import certifi
import unicodedata
import re
import string
import sys
import logging

logging.basicConfig(filename='crawler.log',level=logging.DEBUG, format='%(asctime)s %(message)s', filemode='w')
class MovieScrape:

    checkedlinks = []

    def __init__(self, Movie):
        self._Movie = Movie

    #get gross and film year
    def updatemovieinfo(self):
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        try:
            response = http.request('GET', self._Movie._url)
        except:
            logging.error("Couldn't connect to url")
            return
        soup = BeautifulSoup(response.data, features="html.parser")

        for link in self.checkedlinks:
            if link == self._Movie._url:
                logging.info("Already been to " + self._Movie._url)
                return
        self.checkedlinks.append(self._Movie._url)
        logging.info("Getting movie info from " + self._Movie._url)
        infodiv = soup.find("table", {"class": "infobox vevent"})
        if infodiv == None:
            infodiv = soup.find("table", {"class:" "infobox vcard"})
            if infodiv == None:
                logging.warning("Couldn't find infobox at " + self._Movie._url)
                return
        date = infodiv.find("span", {"class": "bday dtstart published updated"})
        if date == None:
            try:
                date = infodiv("tr")[-6]
                if date == None:
                    logging.error("Could not find date")
                    datetext = "0000"
                else:
                    if date.find('td') == None:
                        logging.error("Could not find date")
                        datetext = "0000"
                    else:
                        datetext = date.find('td').text
            except IndexError:
                logging.error("Could not find date")
                datetext = "0000"
        else:
            datetext = date.text

        datetext = re.findall(r"[-+]?\d*\.\d+|\d+", datetext)
        datenum = 0
        for i in datetext:
            if int(i) > 1900:
                datenum = i
        datetext = int(datenum)

        grossrow = infodiv("tr")[-1]
        gross = grossrow.find('td').text
        gross = gross[:-3]
        gross = re.findall(r"[-+]?\d*\.\d+|\d+", gross)

        try:
            self._Movie.setgross(gross[0])
        except IndexError:
            logging.warning("Box Office Gross not found")
            self._Movie.setgross(0)

        self._Movie.setyear(datetext)
        logging.info("Updated " + self._Movie._name)

    def gettopactors(self):

        listelements = self.getstarringlist()
        if listelements == None:
            return
        actors = []
        for element in listelements:
            linktext = None
            for link in element.find_all('a'):
                linktext = link.get('href')
            if linktext == None:
                logging.warning("No link for actor")
                continue
            linktext = "https://en.wikipedia.org" + linktext
            actorscrape = ActorScrape(linktext)
            actor = actorscrape.create_actor()
            if actor == None:
                continue
            actor._url = linktext
            actors.append(actor)

        return actors

    def getstarringlist(self):
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        try:
            response = http.request('GET', self._Movie._url)
        except:
            logging.error("Couldn't connect to url")
            return
        soup = BeautifulSoup(response.data, features="html.parser")
        logging.info("Getting starring from " + self._Movie._url)
        infodiv = soup.find("table", {"class": "infobox vevent"})
        if infodiv == None:
            infodiv = soup.find("table", {"class:" "infobox vcard"})
            if infodiv == None:
                logging.warning("Couldn't find infobox at " + self._Movie._url)
                return
        tablerows = infodiv.find_all('tr')
        index = 0
        for row in tablerows:
            tableheader = row.find('th')
            if (tableheader != None):
                tableheader = unicodedata.normalize('NFKD', tableheader.text).encode('ascii', 'ignore')
                if tableheader == "Starring":
                    break
            index += 1
        if index == len(tablerows):
            logging.warning("Coulnd't find starring in infobox")
            return
        logging.info("found starring row: " + str(index))
        starring = tablerows[index]
        listelements = starring.find_all('li')

        return listelements

    # def getcast(self):
    #     http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    #     try:
    #         response = http.request('GET', self._Movie._url)
    #     except:
    #         logging.error("Couldn't connect to url")
    #         return
    #     soup = BeautifulSoup(response.data, features="html.parser")
    #     logging.info("Getting cast of " + self._Movie._name)
    #     cast = soup.find("h2", string = "Cast")
    #     if cast == None:
    #         print("Cast not found on page")
    #         return
    #     actors = []
    #     for sibling in cast.next_siblings:
    #         check = sibling.find('ul')
    #         if check == None:
    #             continue
    #         else:
    #             listelements = check.find_all('href')
    #             for element in listelements:
    #                 linktext = None
    #                 link = element.find('a')
    #                 linktext = link.get('href')
    #                 if linktext == None:
    #                     print("No link for actor")
    #                     continue
    #                 linktext = "https://en.wikipedia.org" + linktext
    #                 actorscrape = ActorScrape(linktext)
    #                 actor = actorscrape.create_actor()
    #                 if actor == None:
    #                     continue
    #                 actor._url = linktext
    #                 actors.append(actor)
    #             break
    #     return actors




class ActorScrape:

    checkedlinks = []

    def __init__(self, url):
        self._url = url

    def create_actor(self):
        #get url
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        try:
            response = http.request('GET', self._url)
        except:
            logging.error("Couldn't connect to url")
            logging.error(sys.exc_info()[0])
            return
        soup = BeautifulSoup(response.data, features="html.parser")

        for link in self.checkedlinks:
            if link == self._url:
                logging.info("Already been to " + self._url)
                return
        logging.info("Getting actor info from " + self._url)
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
        namestr = filter(lambda x: x in printable, namestr)

        actor = Actor(namestr, actage)
        logging.info("created " + str(actor))
        return actor

    def get_films(self):
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        try:
            response = http.request('GET', self._url)
        except:
            logging.error("Couldn't connect to url")
            return
        soup = BeautifulSoup(response.data, features="html.parser")

        logging.info("Getting filmography from " + self._url)
        filmography = soup.find("div", {"class": "div-col columns column-width"})
        movies = []
        if filmography == None:
            filmography = self.getfilmstable()
            if filmography == None:
                logging.warning("Couldn't find filmography")
                return movies
        for i in filmography.find_all('i'):
            moviename = unicodedata.normalize('NFKD', i.text).encode('ascii', 'ignore')
            linktext = None
            for link in i.find_all('a'):
                linktext = link.get('href')
            if linktext == None:
                logging.warning("No link for movie")
                continue

            linktext = "https://en.wikipedia.org" + linktext
            movie = Movie(moviename, linktext)
            moviescrape = MovieScrape(movie)
            moviescrape.updatemovieinfo()
            movies.append(movie)

        return movies

    def getfilmstable(self):
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        try:
            response = http.request('GET', self._url)
        except:
            logging.error("Couldn't connect to url")
            return
        soup = BeautifulSoup(response.data, features="html.parser")
        filmspan = soup.find("span", id="Filmography")
        filmheader = filmspan.parent
        for sibling in filmheader.next_siblings:
            if sibling.name == "table":
                logging.info("Found filmography table")
                return sibling
        return




