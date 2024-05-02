'''
Windows Driver Update Utility
Author: Node001

NOTE:   CLI tool for updating all drivers within the C:/Windows/System32 directory.
        Crawls the System32 directory to the end and uses PNPUTIL.exe to install/update relevant drivers.
        Failed driver installation/updates paths and failed purpose are recorded within a txt file and displayed at the end.
        Also invokes the System File Checker Utility after driver install/update is complete to help ensure system files are in order. 

        To ensure all necassary drivers are updated, please be sure to run this with administrative privileges
'''

import os
from subprocess import run as cmd, Popen as bg_process
from multiprocessing import Pool as pThread
import time

#GLOBALS
RED: str = '\33[31m'
GREEN: str = '\33[32m'
YELLOW: str = '\33[33m'
RESET: str = '\33[0m'
OUTFILE: str = './failed_driver_updates.txt'
TARGET_PATH: str = 'C:/Windows/System32/'
PROCESSES: int = 1
MAX_TASK: int = 1

#blank file for failure output to be stored.
def create_outfile() -> None:
    print(f'Creating/ clearing contents of {OUTFILE}')
    with open(OUTFILE, mode='w') as fhandle:
        fhandle.write('FAILED DRIVERS\n\n')

#get reason for driver install/update failure
def get_err(stdout) -> str:
    for err in stdout.split(chr(0x0a)):
        if('Failed' in err):
            return err
    return 'Error finding reason for failure'

#install/update driver, log errors to file
def update(inf_file) -> None:
    inf: str = inf_file.split('/')[-1].removesuffix('.inf')
    print(f'Checking {inf} for updates...')
    try: 
        result = cmd(f'C:/Windows/System32/PNPUTIL.exe /add-driver {inf_file} /install', capture_output=True, text=True)
        if('Failed' in result.stdout):
            raise
    except: 
        err: str = get_err(result.stdout)
        with open(OUTFILE, mode='a') as fhandle:
            fhandle.write(f'DRIVER CONFIG FILE: {inf_file}{chr(0x0a)}{err}{chr(0x0a)*2}')
        print(f'{RED}[-] {inf} Update Failed{chr(0x0a)}{RESET}')
        value: int = 0
    else: 
        print(f'{GREEN}[+] {inf} Update Successful{chr(0x0a)}{RESET}')
        value: int =1
    finally: return value


def main() -> None:
    driver_inf_filepaths: list = list()
    driver_count: int = 0
    
    print(f'{chr(0x0a)}{YELLOW}To ensure that all drivers are updated properly, please be sure to run this with administrative privileges.{RESET}')
    create_outfile()
    time.sleep(3)

    #crawl directories in search for dirver config files
    print(f'{chr(0x0a)}Scanning {TARGET_PATH} for driver config.inf files.{chr(0x0a)}Please be patient...')
    for dirpath, _, filename in os.walk(TARGET_PATH): 
        for file in filename:
            inf_filepath: str = os.path.join(dirpath, file).replace('/', '\\')
            if(file.endswith(r'.inf') and (not((inf_filepath) in driver_inf_filepaths))):
                driver_inf_filepaths.append(inf_filepath)
                driver_count += 1

    print(f'{chr(0x0a)}Found {driver_count} drivers. Preparing to install/update drivers...')
    time.sleep(3)

    #thread updates driver list
    thread: object = pThread(processes=PROCESSES, maxtasksperchild=MAX_TASK)
    values: list = thread.map(update, driver_inf_filepaths)
    thread.close()
    thread.join()

    success: int = sum(values)
    fail: int = driver_count - success

    print('DRIVER UPDATE STATUS')
    print('='*34)
    print(f'||  Total Drivers:{chr(0x09)}{driver_count}{chr(0x09)}||')
    print(f'||  Successful Updates:{chr(0x09)}{success}{chr(0x09)}||')
    print(f'||  Failed Updates:{chr(0x09)}{fail}{chr(0x09)}||')
    print('='*34)

    #display error log if errors exist
    if(fail > 0): 
        print(f'{chr(0x0a)}{YELLOW}Please review the Failed Driver installations/updates while the program scans system files for integrity violations.{chr(0x0a)}Opening {OUTFILE}...{RESET}')
        time.sleep(5)
        bg_process(f'notepad {OUTFILE}')
    else: print('\n Process complete with zero installation/update errors. Running System File Checker to scan system files for integrity violations...')
    
    time.sleep(3)
    #run system file checker
    cmd('sfc -scannow')

    #exit program
    input(f'{chr(0x0a)}{YELLOW}Press [{GREEN}ENTER{YELLOW}] to quit{RESET}')

if(__name__=="__main__"):
    main()  
