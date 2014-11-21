from getData import *
import argparse

parser = argparse.ArgumentParser(description = "Infinite loop to check feeds and take action")
parser.add_argument('interval', metavar = 'N', type = int, help = "Seconds between interation", nargs = "?", default = 300)
args = parser.parse_args()

while(True):
    addFromFeed()
    time.sleep(args.interval)
