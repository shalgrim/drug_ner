'''
File: get_bn_in_counts.py
Author: Scott Halgrim, shalgrim@gmail.com
Date: 6/26/12
Functionality: Extracts the BNs and INs from a file format prepared for me by
               Sunghwan and ouputs to a file where you get the count of each one
               as a BN and as an IN sorted by total count in descending order.
'''

from std_import import *
from collections import defaultdict

# get module logger
logger = logging.getLogger('org.ghri.sharp.drug_ner.get_bn_in_counts')

# create default factory for an element, initializes a dict that counts
# IN and BN occurences
def defaultInBnCounterDict(): return {'IN':0, 'BN':0}

if __name__ == '__main__':                  # if run as main, not if imported
    
    # usage string to give if user asks for help or gets command line wrong
    usageStr = '%(prog)s configfile [options]'
    parser = opts.ConfigFileParser(usage=usageStr)  # create cmd line parser
    options = parser.parse_args()                   # parse command line

    # start logging at root according to command line
    mylogger.config(logfn=options.logfile, logmode=options.logmode, \
                                                    loglevel=options.loglevel)

    logger.setLevel(options.loglevel)   # set module logging level to input

    # TODO: subclass this so i can set defaults and let the get function
    #       have some error checking, etc.
    cp = ConfigParser.SafeConfigParser()    # create config file parser
    cp.read(options.configfn)               # read in config file

    infn = cp.get('Main', 'infile')         # get input file
    outfn = options.outfn                   # get output file

    # read in lines and strip off whitespace (\n)
    lines = [line.strip() for line in myos.readlines(infn)]

    # split |-separated lines
    columns = [line.split('|') for line in lines]

    # Put into list of just IN or BN and then the IN or BN itself
    inbns = [(c[-2], c[-1]) for c in columns]

    # create counter dict
    counts = defaultdict(defaultInBnCounterDict)

    for ib in inbns:                        # for each IN/BN
        counts[ib[1].lower()][ib[0]] += 1   # increment count of its type

    # sort the items of counter dict by total count descending
    sortedcounts = sorted(list(counts.items()), \
                          key=lambda(k,v): sum(v.values()), reverse=True)

    outlines = []                   # initialize lines of output file
    
    for sc in sortedcounts:         # for each BN/IN we counted

        # create its output line
        outlines.append('\t'.join([sc[0], 'BN', str(sc[1]['BN']),
                                          'IN', str(sc[1]['IN'])]))

    myos.writelines(outlines, outfn)    # write output lines to file
