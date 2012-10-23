'''
Scott Halgrim
10/22/12
Adding this as an entry point for all of the main script files
in this project so that I don't have to rewrite all the __main__ code
every time.
The idea is that you say what algo you want to call on the command line.
'''

import std_import as si
from collections import defaultdict

def resolveMysteryMeds(mmfn, synfn, outfn=None):
    '''
    Takes a list of tokenized mystery meds and a synonyms file and links each
    mystery med with longest starting synonym and INBN of that synonym
    '''

    # read in mystery meds
    meds = [line.strip() for line in si.myos.readlines(mmfn)]

    # read in synonyms and associated BN/INs
    synlines = [line.strip() for line in si.myos.readlines(synfn)]

    # split into synonyms and associated BN/INs
    syncols = [syn.split('\t') for syn in synlines]

    # initialize dict for storing synonym->list of BN/IN
    synToName = defaultdict(list)

    # build that dict
    for syn, bnin in syncols:
        synToName[syn].append(bnin)

    outlines = []               # initialize output lines

    for med in meds:            # for each mystery med
        toks = med.split()      # split on whitespace

        # go from full mystery med to first token reducing
        # by one token at a time
        for i in range(len(toks), 0, -1):
            ngram = ' '.join(toks[:i])

            if ngram in synToName:              # if that ngram is a synonym
                links = synToName[ngram]        # then get its BN/INs
                outline = med + '\t' + ngram    # initialize output line

                # for each BN/IN, add it to output line
                for link in links:
                    outline += '\t' + link

                # add line to list of output lines
                outlines.append(outline)
                break

    # sort output lines and write to output file
    si.myos.writelines(sorted(outlines), outfn)

    return

# get module logger
logger = si.logging.getLogger('org.ghri.sharp.drug_ner.main')

if __name__ == '__main__':                  # if run as main, not if imported
    
    # usage string to give if user asks for help or gets command line wrong
    usageStr = '%(prog)s method configfile [options]'
    parser = si.opts.ConfigFileParser(usage=usageStr)  # create cmd line parser
    
    # add method argument for which method to run
    parser.add_argument('method', help='name of method to run')

    options = parser.parse_args()                   # parse command line

    # start logging at root according to command line
    si.mylogger.config(logfn=options.logfile, logmode=options.logmode, \
                                                    loglevel=options.loglevel)

    logger.setLevel(options.loglevel)   # set module logging level to input

    # TODO: subclass this so i can set defaults and let the get function
    #       have some error checking, etc.
    cp = si.ConfigParser.SafeConfigParser()    # create config file parser
    cp.read(options.configfn)               # read in config file

    if options.method == 'resolveMysteryMeds':
        medfn = cp.get('Main', 'MedsFile')      # get name of file to be filtered
        synsfn = cp.get('Main', 'SynsFile')     # get name of synonyms file
        outfn = options.outfn                   # get name of output file
        resolveMysteryMeds(medfn, synsfn, outfn)
    else:
        logger.warning('Unknown method %s'%(options.method))
