import requests
from add_user import add_user
from rcb import run_rcb
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose action")
    parser.add_argument('funkcja', choices=['add_user', 'run_rcb'], help="action name")
    
    args = parser.parse_args()

    if args.funkcja == 'add_user':
        add_user()
    elif args.funkcja == 'run_rcb':
        run_rcb()
    else:
        print('please select action')