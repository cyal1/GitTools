#!/usr/bin/env python3

'''
Finder is part of https://github.com/internetwache/GitTools

Developed and maintained by @gehaxelt from @internetwache

Use at your own risk. Usage might be illegal in certain circumstances.
Only for educational purposes!
'''

import argparse
from functools import partial
from multiprocessing import Pool
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import sys
import requests
import ssl
import encodings.idna
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def findgitrepo(output_file, domains):
    domain = ".".join(encodings.idna.ToASCII(label).decode("ascii") for label in domains.strip().split("."))

    # try:
    #     # Try to download http://target.tld/.git/HEAD
    #     with urlopen(''.join(['http://', domain, '/.git/HEAD']), context=ssl._create_unverified_context(), timeout=5) as response:
    #         answer = response.read(200).decode('utf-8', 'ignore')

    # except HTTPError:
    #     return
    # except URLError:
    #     return
    # except OSError:
    #     return
    # except ConnectionResetError:
    #     return
    # except ValueError:
    #     return
    # except (KeyboardInterrupt, SystemExit):
    #     raise
    try:
        resp = requests.get(domain+"/.git/HEAD",verify=False,timeout=5,headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"})
    except:
        return
    # Check if refs/heads is in the file
    # print(domain,resp.text)
    if 'refs/heads' not in resp.text:
        return

    # Write match to output_file
    # print(domain)
    with open(output_file, 'a') as file_handle:
        file_handle.write(''.join([domain, '\n']))

    print(''.join(['[*] Found: ', domain]))


def read_file(filename):
    with open(filename) as file:
        return file.readlines()

def main():
    print("""
###########
# Finder is part of https://github.com/internetwache/GitTools
#
# Developed and maintained by @gehaxelt from @internetwache
#
# Use at your own risk. Usage might be illegal in certain circumstances.
# Only for educational purposes!
###########
""")

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', default='input.txt', help='input file')
    parser.add_argument('-o', '--outputfile', default='output.txt', help='output file')
    parser.add_argument('-t', '--threads', default=200, help='threads')
    args = parser.parse_args()

    domain_file = args.inputfile
    output_file = args.outputfile
    try:
        max_processes = int(args.threads)
    except ValueError as err:
        sys.exit(err)

    try:
        domains = read_file(domain_file)
    except FileNotFoundError as err:
        sys.exit(err)

    fun = partial(findgitrepo, output_file)
    print("Scanning...")
    with Pool(processes=max_processes) as pool:
        pool.map(fun, domains)
    print("Finished")

if __name__ == '__main__':
    main()
