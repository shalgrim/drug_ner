'''
Date: 8/28/12
Author: Scott Halgrim, halgrim.s@ghc.org
Functionality:
    Takes the tokenized version of the BN/IN/syn file from Sunghwan
    and creates an output file with a single column with all of the
    BNs, INs, and syns singled asciibetically
Notes:
    Difference between this and combine_bnin_syn_files.py is basically the input files.
    I also normalized to lowercase here.  Which I must have done at a different step
    before.
'''

import std_import as si

# get module logger
logger = si.logging.getLogger('org.ghri.sharp.drug_ner.combine_bnin_syn_files_2')

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

    infn = cp.get('Main', 'infile')       # get name of file with BNs, INs, and syns
    outfn = options.outfn       # get name of output file

    inlines = si.myos.readlines(infn)
    bnins = set([' '.join(line.split('|')[0].lower().split('\t')) for line in inlines])
    syns = set([line.split('|')[-1].lower().strip() for line in inlines])

    outset = syns.union(bnins)
    outlines = sorted(list(outset))

    si.myos.writelines(outlines, outfn)
