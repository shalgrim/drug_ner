'''
Date: 8/22/12
Author: Scott Halgrim, halgrim.s@ghc.org
Functionality:
    Tokenizes the BNIN file and the mystery drugs file I was given by adding
    space around commas and brackets ([ and ]) and parens and braces.
'''
import std_import as si

# get module logger
logger = si.logging.getLogger('org.ghri.sharp.drug_ner.tokenize')

def tokenizeBnInFile(infn, outfn, seps=[',', '[', ']', '(', ')', '{', '}']):
    '''
    Input:
        infn - pipe-delimited file that contains BNs and INs in its last column and synonyms (?)
               in its first column
        outfn - file to write tokenized output
        seps - strings to put spaces around
    Output: None
    Functionality: Tokenizes a file by adding space around each sep
    '''

    inlines = si.myos.readlines(infn)

    cols = [line.strip().split('|') for line in inlines]

    for row in cols:
        firstCol = ' '.join(row[0].split('\t'))
        for s in seps:
            firstCol = firstCol.replace(s, ' %s '%(s)).strip()
            row[-1] = ' '.join(row[-1].replace(s, ' %s '%(s)).strip().split())
        row[0] = '\t'.join(firstCol.split())

    outlines = ['|'.join(row) for row in cols]
    si.myos.writelines(outlines, outfn)

    return

def tokenizeMysteryMedsFile(infn, outfn, seps=[',', '[', ']', '(', ')', '{', '}']):
    '''
    Input:
        infn - file that has a med that does not start with BN or IN on each line
        outfn - file to write tokenized output
        seps - strings to put spaces around
    Output: None
    Functionality: Tokenizes a file by adding space around each sep
    '''

    inlines = [line.strip() for line in si.myos.readlines(infn)]
    outlines = []

    for line in inlines:
        outline = line
        for s in seps:
            outline = outline.replace(s, ' %s '%(s))

        outlines.append(' '.join(outline.strip().split()))

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
    
    bninFile = cp.get('Main', 'BnInFile')
    mystMedsFile = cp.get('Main', 'MysteryMedsFile')
    bninOutfile = cp.get('Main', 'BnInOutfile')
    mystMedsOutfile = cp.get('Main', 'MysteryMedsOutfile')
    
    # Tokenize the bnin file and write to output file
    tokenizeBnInFile(bninFile, bninOutfile)

    # Tokenize the bnin file and write to output file
    tokenizeMysteryMedsFile(mystMedsFile, mystMedsOutfile)

