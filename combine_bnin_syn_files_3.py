'''
Date: 10/22/12
Author: Scott Halgrim, halgrim.s@ghc.org
Functionality:
    Takes the tokenized version of the BN/IN file from Sunghwan and the
    synonym file created from the RxNav processes
    and creates an output file with a single column with all of the
    BNs, INs, and syns singled asciibetically
Notes:
    Difference between this and combine_bnin_syn_files(_2)?.py is basically the input files.
    This is actually much closer to the original than to _2
'''

import std_import as si

# get module logger
logger = si.logging.getLogger('org.ghri.sharp.drug_ner.combine_bnin_syn_files_3')

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

    bninfn = cp.get('Main', 'BnInFile')      # get name of file to be filtered
    synsfn = cp.get('Main', 'SynsFile')     # get name of synonyms file

    outfn = options.outfn       # get name of output file

    synlines = si.myos.readlines(synsfn)
    syns = set([line.split('\t')[0] for line in synlines])

    bninlines = si.myos.readlines(bninfn)
    bnins = set([line.split('\t')[0] for line in bninlines])

    outset = syns.union(bnins)
    outlines = sorted(list(outset))

    si.myos.writelines(outlines, outfn)
