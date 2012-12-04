'''
Date: 10/19/12
Author: Scott Halgrim, halgrim.s@ghc.org
Functionality:
    Tokenizes the synonym->RxNormName map file created at Sunghwan's request so it
    can be used to reduce tokenized mystery meds later on.
    This script should work to tokenize the list of BNINs and their counts I did in chain 0033
    so as of 10/23/12 I'm repurposing it for that as well
'''
import std_import as si

# get module logger
logger = si.logging.getLogger('org.ghri.sharp.drug_ner.tokenize_rxnav_syns')

def tokenizeFile(infn, outfn, seps=[',', '[', ']', '(', ')', '{', '}'], unique=True, tosort=True):
    '''
    Input:
        infn - tab-separated file where first column is synonym, second column is RxNormName of BN or IN
        outfn - file to write tokenized output
        seps - strings to put spaces around
        unique - if True then ensure output lines are unique
        tosort - if True then sort output lines
    Output: None
    Functionality: Tokenizes a file by adding space around each sep
    '''

    inlines = si.myos.readlines(infn)

    cols = [line.strip().split('\t') for line in inlines]

    for row in cols:
        firstCol = ' '.join(row[0].split('\t'))
        for s in seps:
            row[0] = ' '.join(row[0].replace(s, ' %s '%(s)).strip().split())
            row[1] = ' '.join(row[1].replace(s, ' %s '%(s)).strip().split())

    outlines = ['\t'.join(row) for row in cols]

    if unique:
        outlines = list(set(outlines))

    if tosort:
        outlines.sort()

    si.myos.writelines(outlines, outfn)

    return


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
    
    infn = cp.get('Main', 'infile')
    uniq = cp.getboolean('Main', 'unique')
    tosort = cp.getboolean('Main', 'sort')

    # Tokenize the file and write to output file
    tokenizeFile(infn, options.outfn, unique=uniq, tosort=tosort)

