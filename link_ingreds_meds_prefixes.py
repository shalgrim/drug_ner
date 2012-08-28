'''
Date: 6/29/2012
Author: Scott Halgrim, halgrim.s@ghc.org
Functionality:
    Flattens a file that has BN/INs followed by all the drug names in which they
appear into one combo per line while also adding a third column that has the
prefix, that part of the drug name that precedes the BN/IN.
'''

from std_import import *
import re, pdb

# get module logger
logger = logging.getLogger('org.ghri.sharp.drug_ner.link_ingreds_meds_prefixes')

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

    # get name of tab-separated file that contains all of the BNs and INs in the
    # first column and the n-grams of which they are a part in later columns
    bulkyfn = cp.get('Main', 'BulkyFile')

    flatfn = options.outfn       # get name of output file

    # read in lines of bulky file and split by tabs
    bulkylines = [line.strip() for line in myos.readlines(bulkyfn)]
    cols = [line.split('\t') for line in bulkylines]
    
    flattened = []              # initialize flattened list

    for line in cols:           # for each line bulk file
        bnin = line[0]          # get BN/IN

        for longer in line[1:]:     # for each longer name of which its a part

            # find the bnin in the longer string after a space
            # (because we know it doesn't start with it)
            # and assure it is followed by whitespace or end of string
            escaped = bnin.replace('(', '\(')
            escaped = escaped.replace(')', '\)')
            escaped = escaped.replace('+', '\+')
            prefixre = r'(?<=\s)%s(?=(\s|$))'%(escaped)
            match = re.search(prefixre, longer)

            try:
                assert match.start() > 0
            except:
                print 'error'

            # get the part of the string that occurs before the BN/IN
            # do the strip because there's probs a trailing space
            prefix = longer[:match.start()].strip()

            # create a new tab sep line that is BN/IN then long name then prefix
            flattened.append(line[0] + '\t' + longer + '\t' + prefix)

    flattened.sort()                    # sort the output lines
    myos.writelines(flattened, flatfn)  # write output lines to output file
