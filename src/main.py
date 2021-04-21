import sys
import os
import argparse
from my_funcs import cap_data


if __name__ == '__main__':
    # Argparse    
    ap = argparse.ArgumentParser(description="Run Elasticsearch on NYC Open Data Api")
    
    # set main arguments
    ap.add_argument('-p',"--page_size",  type=int, metavar='', required=True, help="This is the total nuumber of records requested per API call",)
    ap.add_argument('-n',"--num_pages",  type=int, metavar='', help=" This is the total number of calls to the API", default=None)
    
    # create container and set mutually exclusive group
    group = ap.add_mutually_exclusive_group()
    group.add_argument('-q',"--quiet", action='store_true', help=" This prints out quiet info provided that both page_size and num_pages were provided" )
    group.add_argument('-v',"--verbose", action='store_true', help=" This prints out verbose info")
    
    args = ap.parse_args()
    
    
    if args.quiet:
        print("The page size:", args.page_size)
        print("The number of pages :", args.num_pages)
        print("The total number of documents are:", args.page_size*args.num_pages)
        
    elif args.verbose:
        cap_data(args.page_size, args.num_pages)
        
    else:
        cap_data(args.page_size, args.num_pages)
        
