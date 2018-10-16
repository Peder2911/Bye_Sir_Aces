
import os
import sys

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

import csv
import re

from lib.Cli import Cli

# argument stuff ###################
usage = 'usage: bsa.py [datafile templatefile][destination -e extension]'

# get files #######################

files = []
for a in sys.argv[1:]:
    if os.path.isfile(a):
        files.append(a)
        sys.argv.remove(a)

    if len(files) == 2:
        break
else:
    print(usage)
    sys.exit(1)

datafile,templatefile = files

# get path (optional) ##############

for a in sys.argv[1:]:
    if os.path.isdir(a):
        dest = os.path.abspath(a)
        break
else:
    dest = './'

# custom file extension ############

if '-e' in sys.argv:
    try:
        extension = sys.argv[sys.argv.index('-e')+1]
    except IndexError:
        print(usage)
        sys.exit(1)
else:
    extension = '.txt'

# Main flow ########################

if __name__ == '__main__':

    myCli = Cli(demarcate = True,nlpad = True)
    # Read the template ############

    with open(templatefile) as File:
        template = File.read()
        fields = re.findall('(?<=\{)[^\}]*(?=})',template)
        fields = list(set(fields))

    # Work with data ###############

    with open(datafile) as File:
        reader = csv.reader(File)
        header = next(reader)

        # Assign fields to columns # 
        mapping = {}
        for f in fields:
            m = myCli.menu(options = header,prompt = 'Select column for %s'%(f))
            m = header.index(m)
            mapping.update({f:m})

        
        # Column to name files #####
        namingcol = myCli.menu(options = header,prompt = 'Select naming column')
        namingcol = header.index(namingcol)

        # Iterate over data, #######
        # making files #############
        for row in reader:
            filename = row[namingcol]
            filename = filename + extension
            
            num = 0
            while os.path.isfile(os.path.join(dest,filename)):
                num += 1
                filename = str(num) + '_' + filename

            filename = os.path.join(dest,filename)

            rowmap = {}
            for f,i in mapping.items():
                rowmap.update({f:row[i]})

            formatted = template.format(**rowmap)

            with open(filename,'w') as out:
                out.write(formatted)

