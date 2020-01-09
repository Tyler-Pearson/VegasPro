# RETURN FORMAT: (team 0, score 0, team 1, score 1)

import csv
import datetime
import re
import os
import urllib2
from bs4 import BeautifulSoup
import sys


BASE_URL = "https://www.basketball-reference.com"
# ALPHA Date vals are from first games month - October 1
ALPHA_MONTH = 10
ALPHA_DAY = 1
# OMEGA Date vales are from end of NBA closing month - June 30
OMEGA_MONTH = 6
OMEGA_DAY = 30


# game_bundle == (boxscore_url, away_abbreviation, home_abbreviation)




# throws exception if stats_soup.find returns None
def append_team_stats(stats_soup, arr):

    # field goals - get 2 pt and 3 pt fg made + fg attempts
    fg = int(stats_soup.find('td', attrs={'data-stat':'fg'}).text)
    fga = int(stats_soup.find('td', attrs={'data-stat':'fga'}).text)
    fg3 = int(stats_soup.find('td', attrs={'data-stat':'fg3'}).text)
    fg3a = int(stats_soup.find('td', attrs={'data-stat':'fg3a'}).text)
    fg2 = fg - fg3
    fg2a = fga - fg3a
    arr.append(fg2)
    arr.append(fg2a)
    arr.append(fg3)
    arr.append(fg3a)

    # ft made and attempted
    ft = int(stats_soup.find('td', attrs={'data-stat':'ft'}).text)
    fta = int(stats_soup.find('td', attrs={'data-stat':'fta'}).text)
    arr.append(ft)
    arr.append(fta)

    # offensive and defensive rebounds
    orb = int(stats_soup.find('td', attrs={'data-stat':'orb'}).text)
    drb = int(stats_soup.find('td', attrs={'data-stat':'drb'}).text)
    arr.append(orb)
    arr.append(drb)

    # assists, steals, blocks, turnovers, fouls
    ast = int(stats_soup.find('td', attrs={'data-stat':'ast'}).text)
    stl = int(stats_soup.find('td', attrs={'data-stat':'stl'}).text)
    blk = int(stats_soup.find('td', attrs={'data-stat':'blk'}).text)
    tov = int(stats_soup.find('td', attrs={'data-stat':'tov'}).text)
    pf = int(stats_soup.find('td', attrs={'data-stat':'pf'}).text)
    arr.append(ast)
    arr.append(stl)
    arr.append(blk)
    arr.append(tov)
    arr.append(pf)

    # points
    pts = int(stats_soup.find('td', attrs={'data-stat':'pts'}).text)
    arr.append(pts)


# throws exception if append_team_stats throws exception
def get_stats(date, url, away_abbr, home_abbr, boxscores):

    stats = []

    page = None
    while (page == None):
        try:
            page = urllib2.urlopen(url, timeout=2)
        except:
            page = None
    soup = BeautifulSoup(page, 'html.parser')

    # general game info - date and time
    game_time = soup.find('div', attrs={'class':'scorebox_meta'}).find_all('div')[0].text.split(",")[0]
    stats.append(str(date.date()))
    stats.append(str(game_time))

    # home team name + stats
    home_stats = soup.find('table', attrs={'id':'box-'+home_abbr+'-game-basic'})
    home_team = " ".join(home_stats.find('caption').text.split()[:-2])
    stats.append(str(home_team))
    append_team_stats(home_stats.find('tfoot'), stats)

    # away team name + stats
    away_stats = soup.find('table', attrs={'id':'box-'+away_abbr+'-game-basic'})
    away_team = " ".join(away_stats.find('caption').text.split()[:-2])
    stats.append(str(away_team))
    append_team_stats(away_stats.find('tfoot'), stats)

    return stats


def get_abbr(href):
    # href == "/teams/ABR/YEAR.html"
    href_segs = href.split("/")
    # href_segs == ["", "teams", "ABR", "YEAR.html"]
    return href_segs[2]


# game_bundle == (boxscore_url, away_abbreviation, home_abbreviation)
def get_boxscore_urls_and_abbrs(url):

    game_bundles = []

    page = None
    while (page == None):
        try:
            page = urllib2.urlopen(url, timeout=2)
        except:
            page = None
    soup = BeautifulSoup(page, 'html.parser')
    try:
        game_summaries = soup.find('div', attrs={'class':'game_summaries'})
        games_tables = game_summaries.find_all('table', attrs={'class':'teams'})
    except:
        return []
    for game_links in games_tables:
        links = [str(link['href']) for link in game_links.find_all('a') if link['href']]
        if len(links) != 3:
            continue
        away_abbr = get_abbr(links[0])
        home_abbr = get_abbr(links[2])
        game_bundles.append((BASE_URL + links[1], away_abbr, home_abbr))

    return game_bundles


def get_boxscores(season):

    boxscores = []

    date = datetime.datetime(season-1, ALPHA_MONTH, ALPHA_DAY)
    date_end = datetime.datetime(season, OMEGA_MONTH, OMEGA_DAY)
    while date < date_end:
        # get url for cur date
        cur_date_url = BASE_URL \
            + "/boxscores/?month=" + str(date.month) \
            + "&day=" + str(date.day) \
            + "&year=" + str(date.year)
        # if (date.day == 1 or date.day == 15):
        #     print date.date()
        # get games from cur date
        cur_game_bundles = get_boxscore_urls_and_abbrs(cur_date_url)
        # print cur_game_bundles
        for game_bundle in cur_game_bundles:
            # get_stats(url, away_abbr, home_abbr, boxscores from this fn)
            try:
                game_stats = get_stats(date, game_bundle[0], game_bundle[1], game_bundle[2], boxscores)
                boxscores.append(game_stats)
            except:
                # if get_stats throws exception, just ignore the game
                pass
        # print len(boxscores)
        date += datetime.timedelta(days=1)
    # print (date + datetime.timedelta(days=1))

    return boxscores


    # print datetime.datetime.now()


def write_boxscores(season, boxscores):

    filename = "./data/" + str(season) + '.csv'
    print "writing to " + filename
    with open(filename, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["date", "start_time",\
                "home_team", "h_fg2", "h_fg2a", "h_fg3", "h_fg3a", "h_ft", "h_fta", "h_orb", "h_drb", "h_ast", "h_stl", "h_blk", "h_tov", "h_pf", "h_pts",\
                "away_team", "a_fg2", "a_fg2a", "a_fg3", "a_fg3a", "a_ft", "a_fta", "a_orb", "a_drb", "a_ast", "a_stl", "a_blk", "a_tov", "a_pf", "a_pts"])
        for boxscore in boxscores:
            filewriter.writerow(boxscore)


def scrape_boxscores(init_season, end_season):
    season = init_season
    while (season <= end_season):
        try:
            print "scraping " + str(season)
            boxscores = get_boxscores(season)
            print str(len(boxscores)) + " games scraped"
            write_boxscores(season, boxscores)
            print '\a\a\a'
            season += 1
        except:
            return season
    print '\a\a\a\a\a'
    return season


def main():

    try:
        os.mkdir('./data')
    except OSError:
        pass

    season = 1984
    # season = 2008
    end_season = 2020
    while (season <= end_season):
        season = scrape_boxscores(season, end_season)


if __name__=="__main__":
   main()

