# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 15:29:20 2017

@author: groberta
"""

import bs4
import requests
import csv

# Function to return molecular weights given a drug name
def get_mwt(name, debug=True):
    '''Uses drug name pull wikipedia page.
    
    Identifies mol weight element as containing "/mol"
    in a <td> element of the html.
    
    Returns the string, after taking off labels    
    '''
    req_string = 'https://en.wikipedia.org/wiki/'+name
    if debug==True:
        print(req_string)
    res = requests.get(req_string)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    type(soup)

    sel = soup.select('td')
    return [str(x)[4:-5] for x in sel if "/mol" in str(x)]


def main(namefile, outfile="mwts.csv"):

# Read in the names
    with open (namefile, 'r') as names_csv:
        names = [y[0] for y in csv.reader(names_csv)]
    
# Build the list of molecular weights (or FAILs)
    mwts = []
    for drug in names:
        try:
            mwts.append(get_mwt(drug))
        except:
            mwts.append("FAILED")
 
    # Write out results   
    with open(outfile, 'w', newline="") as outfile:
        drugw = csv.writer(outfile)
        for i,drug in enumerate(names):
            try:
                drugw.writerow([drug,mwts[i][0]])
            except:
                continue

if __name__ == "__main__":
    import sys
    main("names.csv")
