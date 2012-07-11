'''
Date: 7/10/12
Author: Scott Halgrim, halgrim.s@ghc.org
Functionality:
    Given two files, finds those lines in file 1 (a list of all medications
    that do not start with BN or IN (0034 output)) that do not appear in
    the second column of file 2 (a tab-separated file whose second column is
    drug names that contain an BN or IN (0037 output)).
'''
from std_import import *

# get module logger
logger = logging.getLogger('org.ghri.sharp.drug_ner.get_non_bnin_containing_drugs')

def main(allMedsFile, medsContainBninFile, outfn):
    '''
    Input:
        allMedsFile - each line contains a drug that does not start with BN or IN
        medsContainBninFile - second tab-sep column has meds that have BN or IN somewhere in them
        outfn - output file
    Output: None
    Functionality: Creates list of meds that do not have BN or IN in them and writes to output file
    '''

    # get set of all meds that do not start with BN or IN
    allMeds = set([line.strip() for line in myos.readlines(allMedsFile)])                       

    # get set of all of those meds that have BN or IN somewhere in them
    medsContainBnin = set([line.split('\t')[1] for line in myos.readlines(medsContainBninFile)])

    # get sorted list of meds that do not have BN or IN in them
    drugsToOutput = sorted(list(allMeds.difference(medsContainBnin)))

    # write output to output file
    myos.writelines(drugsToOutput, outfn)

    return

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
    
    # get file containing all meds not starting with bn/in
    allMysteryMedsFile = cp.get('Main', 'AllMedsFile')
    
    # get file whose second tab-separated column is meds with a BN/IN somewhere in them 
    mysteryMedsContainBninFile = cp.get('Main', 'MedsContainingBNINFile') 

    # get output filename
    outfn = options.outfn
    
    # create list of meds that don't contain BN/IN and write to outfn   
    main(allMysteryMedsFile, mysteryMedsContainBninFile, outfn)
