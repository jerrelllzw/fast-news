import time
from utils import fetch_and_notify

def main():
    while True:
        fetch_and_notify()
        time.sleep(60)

if __name__ == "__main__":
    main()
