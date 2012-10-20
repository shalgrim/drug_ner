'''
8/14/12
Scott Halgrim, halgrim.s@ghc.org
Takes Sunghwan's requested file (see chain 0066) and reduces it so that each synonym-RxNormName
combo is in the output once and only once
'''
import std_import as si

# get module logger
logger = si.logging.getLogger('org.ghri.sharp.drug_ner.reduce_syn_map')

def reduceSynonyms(inlines):
    '''

    '''
    cols = [line.split('|') for line in inlines]        # split lines into columns

    # put lines into a list of (syn, RxName) tuples
    # then make that unique by making a set
    # then convert to a sorted list
    sortedCombos = sorted(list(set([(col[0], col[-2]) for col in cols])))
    return sortedCombos         # return output

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

    infn = cp.get('Main', 'infile')      # get name of file to be filtered

    inlines = [line.strip() for line in si.myos.readlines(infn)]           # read in input file
    uniqueCombos = reduceSynonyms(inlines)                  # reduce to output combos
    outlines = ['\t'.join(uq) for uq in uniqueCombos]
    si.myos.writelines(outlines, options.outfn) # write output to file


