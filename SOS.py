#!/usr/bin/env python3
""" Saving Our Soups.

Backs up Soup.io tumblelogs.
Copyright (C) 2020 J12i

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

from sys import argv
from os import getcwd
from sys import exit
from subprocess import run
from time import time
from os.path import join,exists

if len(argv)<2:
    print('''Usage: SOS <soup name> <since> <working directory>
  At least give the soup name as argument.
  If you want to give wd but not since, enter 0.''')
    exit(2^5)
    
soup = argv[1]
page = argv[2] if len(argv)>2 and argv[2]!= '0' else None
wd = argv[3] if len(argv)>3 else getcwd()

wgetCommand = ['wget', '-t0', '-w0.5', '-e', 'robots=off', '-a', soup + '_log', '-nv', '--no-adjust-extension', '-x', '--save-cookies', 'cookies', '--keep-session-cookies', '--retry-on-http-error=503,500']
haveCookies = exists(join(wd, 'cookies'))
if haveCookies: wgetCommand.extend(['--load-cookies', 'cookies'])
    
downloadDir = join(wd, soup + '.soup.io')
curLenOfNo = 9

def downloadPage():
    global haveCookies
    starttime = time()
    thisWgetCommand = wgetCommand.copy()
    if page:
        thisWgetCommand += ['https://' + soup + '.soup.io/since/' + page]
        try:
            run(thisWgetCommand, cwd = wd, check = True)
        except:
            print(' '.join(thisWgetCommand) + ' failed.')
            exit(2)
        if not haveCookies and exists(join(wd, 'cookies')):
            wgetCommand.extend(['--load-cookies', 'cookies'])
            haveCookies = True
    else:
        if not haveCookies:
            firstWgetCommand = wgetCommand.copy()
            firstWgetCommand.append('https://' + soup + '.soup.io/')
            run(firstWgetCommand, cwd = wd)
            wgetCommand.extend(['--load-cookies', 'cookies'])
            haveCookies = True
            thisWgetCommand = wgetCommand.copy()
        thisWgetCommand += ['-H', '--domains', soup + '.soup.io,www.soup.io,asset.soup.io,static.soup.io', '-p', 'https://' + soup + '.soup.io/']
        run(thisWgetCommand, cwd = wd)
    print('got ' + (page if page != None else 'start') + ' in ' + str(round(time() - starttime)) + ' s')

def extractNextPage():
    global curLenOfNo, page
    try:
        pageFileName = '/since/' + page if page != None else '/index.html'
        pageFile = open(downloadDir + pageFileName)
    except IOError:
        print('pageFile not found: ' + downloadDir + pageFileName)
        exit(1)
    with pageFile:
        nextPage = None
        for line in pageFile:
            if line.startswith("      SOUP.Endless.next_url = '/since/"):
                nextPage = line[38:38+curLenOfNo]
                while nextPage[curLenOfNo-1] not in ['0','1','2','3','4','5','6','7','8','9']:
                    curLenOfNo -= 1
                nextPage = nextPage[:curLenOfNo]
                break
        if nextPage != None:
            page = nextPage
        else:
            print('Last download corrupt or end of soup reached.\n\t' + page)
            exit(4)


while True:
    downloadPage()
    extractNextPage()
