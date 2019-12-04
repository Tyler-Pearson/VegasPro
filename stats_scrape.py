import re
import urllib2
from bs4 import BeautifulSoup
import sys



def get_week(url):

   page = urllib2.urlopen(url)
   soup = BeautifulSoup(page, 'html.parser')
   game_summaries = soup.find('div', attrs={'class':'game_summaries'})
   games = game_summaries.find_all('div', attrs={'class':'game_summary'})

   results = []
   for game in games:
      result = game.find('table', attrs={'class':'teams'})
      teams = result.find_all('tr')
      results.append((
         str(teams[1].find('a').text),
         int(teams[1].find('td', attrs={'class':'right'}).text),
         str(teams[2].find('a').text),
         int(teams[2].find('td', attrs={'class':'right'}).text)))

   return results


# ADD OFFENSE
# ADD DEFENSE
def add_stats(stats):

   results = []

   for i in range(cur_week):
      url = BASE_URL +  "week_" + str(i+1) + ".htm"
      # print url
      results.extend(get_week(url))

   return results


def main():

   print "Getting results"
   results = get_results(CUR_WEEK)
   print str(len(results)) + " results scraped"
   print results[0]


if __name__=="__main__":
   main()