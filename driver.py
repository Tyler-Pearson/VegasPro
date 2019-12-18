from results_scrape import *
from stats_scrape import *
import sys


CUR_WEEK = 15
RESULTS_FILENAME = "results.csv"
STATS_FILENAME = "stats.csv"



def add_teams(results, stats):
   for result in results:
      stats[result[0]] = [result[0]]
      stats[result[2]] = [result[2]]


def write_results(results, filename):
    with open(filename, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["home_team", "home_score", "away_team", "away_score"])
        for result in results:
            filewriter.writerow(result)

# ppg, to_pg, 3/4 conv, rz_att, rz_conv

# defs:
#  pg=per game
#  to=turnovers
#  ld=late down
#  cr=conversion rate
#  rz=red zone (last 20 yards)
#  apg=attempts per game
#  d=defensive
#  ta=takeaways
def write_stats(stats, filename):
    with open(filename, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["team_name", "ppg", "to_pg", "ld_cr", "rz_apg", "rz_cr",\
                "dppg", "ta_pg", "dld_cr", "drz_apg", "drz_cr"])
        for team in stats:
            filewriter.writerow(stats[team])


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
   print str(len(stats)) + " teams added!"

   print "getting stats..."
   add_stats(stats)

   print "writing stats to " + STATS_FILENAME
   write_stats(stats, STATS_FILENAME)

   # print "---"
   # for stat in stats:
   #     print stat
   #     print stats[stat]
   #     print "---"


if __name__=="__main__":
   main()
