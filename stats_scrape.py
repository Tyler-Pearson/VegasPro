import re
import urllib2
from bs4 import BeautifulSoup, Comment
import sys


OFFENSE_URL = "https://www.pro-football-reference.com/years/2019/index.htm"
DEFENSE_URL = "https://www.pro-football-reference.com/years/2019/opp.htm"


# Helper function, football-ref html returns tables in comments
# Return tables from url in dict, {table_id:table}
def get_tables(url):
    tables = {}
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    noncomment_tables = soup.find_all('table')
    for table in noncomment_tables:
        # print table.get('id')
        tables[str(table.get('id'))] = table
    # NOTE: many tables are in comments, below code extracts them
    comments = soup.find_all(string = lambda text:isinstance(text, Comment))
    for comment in comments:
        comment = BeautifulSoup(str(comment), 'html.parser')
        table = comment.find('table')
        if (table):
            # print table.get('id')
            tables[str(table.get('id'))] = table
    return tables


# soup should be just the Team Offense table
def add_general(stats, soup):
    teams = soup.find('tbody').find_all('tr')
    for team in teams:
        name = team.find('a').text
        games_played = float(team.find('td', attrs={'data-stat':'g'}).text)
        # PPG
        points_for = float(team.find('td', attrs={'data-stat':'points'}).text)
        stats[name].append(points_for/games_played)
        # Turnovers per game
        turnovers = float(team.find('td', attrs={'data-stat':'turnovers'}).text)
        stats[name].append(turnovers/games_played)



# soup should be just the Team Conversions table
def add_conversions(stats, soup):
    teams = soup.find('tbody').find_all('tr')
    for team in teams:
        name = team.find('a').text
        games_played = float(team.find('td', attrs={'data-stat':'g'}).text)
        # Third and fourth conversion rate combined
        third_att = float(team.find('td', attrs={'data-stat':'third_down_att'}).text)
        third_suc = float(team.find('td', attrs={'data-stat':'third_down_success'}).text)
        fourth_att = float(team.find('td', attrs={'data-stat':'fourth_down_att'}).text)
        fourth_suc = float(team.find('td', attrs={'data-stat':'fourth_down_success'}).text)
        stats[name].append((third_suc + fourth_suc)/(third_att + fourth_att))
        # Red zone attempts and red zone TD rate
        rz_att = float(team.find('td', attrs={'data-stat':'red_zone_att'}).text)
        rz_suc = float(team.find('td', attrs={'data-stat':'red_zone_scores'}).text)
        stats[name].append(rz_att/games_played)
        stats[name].append(rz_suc/rz_att)


# ADD OFFENSE
def add_side(stats, url):
    tables = get_tables(url)
    add_general(stats, tables["team_stats"])
    add_conversions(stats, tables["team_conversions"])



# ADD ALL STATS
# ppg, to_pg, 3/4 conv, rz_att, rz_conv
def add_stats(stats):

   add_side(stats, OFFENSE_URL)
   add_side(stats, DEFENSE_URL)

   # no need for return, stats dict is populated directly


### Need "stats" dictionary of teams:[] to use this class
# def main():
#
#    print "Getting stats"
#    results = get_results(CUR_WEEK)
#    print str(len(results)) + " results scraped"
#    print results[0]
#
#
# if __name__=="__main__":
#    main()
