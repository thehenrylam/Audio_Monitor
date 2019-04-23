#!/usr/bin/env python

import time
 
 
def main():
    print("start")
    while True:
        try:
            print('-')
            time.sleep(1)
            #while True:
                #print('-')
                #time.sleep(1)
        except KeyboardInterrupt:
            print('interrupted!')
            break

    print("end")
 
##########
 
if __name__ == "__main__":
    main()
