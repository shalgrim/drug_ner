'''
Date: 8/14/12
Author: Scott Halgrim, halgrim.s@ghc.org
Functionality:
    Takes a file of meds that don't start with BN or IN and filters out those
    that start with a synonym of a BN or IN.
'''

import std_import as si

CREATE_SYN_SET = {
                  "fromSunghwanFile":lambda x: set([' '.join(line.split('|')[0].split('\t')) for line in x]),
                  "fromRxNavResults":lambda x: set([line.split('\t')[0] for line in x])
                  }

# get module logger
logger = si.logging.getLogger('org.ghri.sharp.drug_ner.filter_out_syn_initial_meds')

if __name__ == '__main__':                  # if run as main, not if imported
    
    # usage string to give if user asks for help or gets command line wrong
    usageStr = '%(prog)s configfile [options]'
    parser = si.opts.ConfigFileParser(usage=usageStr)  # create cmd line parser
    options = parser.parse_args()                   # parse command line

    # start logging at root according to command line
    si.mylogger.config(logfn=options.logfile, logmode=options.logmode, \
                                                    loglevel=options.loglevel)

    logger.setLevel(options.loglevel)   # set module logging level to input

    # TODO: subclass this so i can set defaults and let the get function
    #       have some error checking, etc.
    cp = si.ConfigParser.SafeConfigParser()    # create config file parser
    cp.read(options.configfn)               # read in config file

    medfn = cp.get('Main', 'MedsFile')      # get name of file to be filtered
    synsfn = cp.get('Main', 'SynsFile')     # get name of synonyms file

    # get name of method used to create unique set of synonyms from lines in synonyms file
    synMethod = cp.get('Main', 'SynMethod') 

    outfn = options.outfn       # get name of output file

    synlines = si.myos.readlines(synsfn)
    syns = CREATE_SYN_SET[synMethod](synlines)

    # the old way before I had two methods
    #syns = set([' '.join(line.split('|')[0].split('\t')) for line in synlines])

    medlines = [line.strip() for line in si.myos.readlines(medfn)]

    outlines = []

    for ml in medlines:
        for i in range(len(ml), 0, -1):
            subber = ' '.join(ml.split()[:i])
            if subber in syns:
                break
        else:
            outlines.append(ml)

    si.myos.writelines(outlines, outfn)
    

    si.myos.writelines(outlines, outfn)
