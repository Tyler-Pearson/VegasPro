from results_scrape import *
from stats_scrape import *
import sys


CUR_WEEK = 15
RESULTS_FILENAME = "results.csv"



def add_teams(results, stats):
   for result in results:
      stats[result[0]] = {}
      stats[result[2]] = {}


def write_results(results, filename):
    with open(filename, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["home_team", "home_score", "away_team", "away_score"])
        for result in results:
            filewriter.writerow(result)


def main():

   stats = {}

   cur_week = CUR_WEEK if (len(sys.argv) < 2) else int(sys.argv[1])
   print "getting results..."
   results = get_results(cur_week)

   print "writing results to " + RESULTS_FILENAME
   write_results(results, RESULTS_FILENAME)

   # create stats dict, add dict(team)={} for each team
   print "init stats dictionary, adding base teams..."
   add_teams(results[:16], stats)
   print str(len(stats)) + " teams added"

   add_stats(stats)


if __name__=="__main__":
   main()
