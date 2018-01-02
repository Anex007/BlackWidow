
import urllib
import argparse
from web_crawler import Spider

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', help='Verbose Output', action="store_true")
    group.add_argument('-q', '--quiet', help='Be Quiet, My mom\'s looking', action="store_true")
    parser.add_argument('url', help='The website to crawl')
    parser.add_argument('-t', '--threads', help='The number of threads the crawler will run on', default=3, type=int)

    args = parser.parse_args()

    if not (args.url.startswith('http://') or args.url.startswith('https://')):
        print('[-] Url should be in [http|https]:// format')
        return

    verbose = 2
    
    if args.quiet:
        verbose = 1
    elif args.verbose:
        verbose = 3

    threads = []

    for i in range(args.threads):
        spider = Spider(args.url ,str(i), verbose)
        spider.start()
        threads.append(spider)

    for i in threads:
        i.join()


if __name__ == "__main__":
    main()
