'''
Date: 8/15/12
Author: Scott Halgrim, halgrim.s@ghc.org
Functionality:
    Takes the two original files from Sunghwan, the BNIN file and the mystery
    meds file, and creates a tab-sep output file that lists those mystery meds
    that start with a synonym (the first column of the BNIN file) along with
    the synonym with which they start
'''
import std_import as si

# get module logger
logger = si.logging.getLogger('org.ghri.sharp.drug_ner.get_start_with_syn')

def main(mysteryfn, bninfn, outfn):
    '''
    Takes a file of mystery meds, looks for those that start with something in
    the first column of bninfn and writes those meds, along with the syn they
    start with, to outfn
    '''
    syns = set([' '.join(line.split('|')[0].split())
                for line in si.myos.readlines(bninfn)])
    mysterymeds = set([line.strip() for line in si.myos.readlines(mysteryfn)])

    startWithSyn = {}
    for med in mysterymeds:
        toks = med.split()
        for i in range(len(toks), 0, -1):
            subber = ' '.join(toks[:i])
            if subber in syns:
                startWithSyn[med] = subber
                break

    outlines = ['\t'.join(item) for item in startWithSyn.items()]
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
    
    # get file containing all meds not starting with bn/in
    allMysteryMedsFile = cp.get('Main', 'MedsFile')
    
    # get file whose second tab-separated column is meds with a BN/IN somewhere in them 
    mysteryMedsContainBninFile = cp.get('Main', 'BNINFile') 

    # get output filename
    outfn = options.outfn
    
    # create list of meds that start with a synonym write to outfn   
    main(allMysteryMedsFile, mysteryMedsContainBninFile, outfn)
