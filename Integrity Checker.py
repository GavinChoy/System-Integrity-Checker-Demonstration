#    Proof of concept demonstration of holistically ensuring data integrity on a system
#    Copyright (C) 2018 Gavin Choy
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

print("--------------------------------------------------------------------------------------------------")
print('')
print("    Proof of concept demonstration of holistically ensuring data integrity on a system")
print("    Copyright (C) 2018 Gavin Choy")
print("    This program comes with ABSOLUTELY NO WARRANTY; for details please see the LICENSE file.")
print("    This is free software, and you are welcome to redistribute it")
print("    under certain conditions; please see the LICENSE file for details.")
print('')
print("--------------------------------------------------------------------------------------------------")
print('')

print("Please read the README file for a description of what this program was designed to do.")
print('')
print("--------------------------------------------------------------------------------------------------")
print('')

import os
import hashlib
import time
import threading
import shutil

# subroutine to check the integrity of the system files
def system(systemdirectory):
    
    # keep this looping forever
    while True:

        # if the directory with the system files exists
        if os.path.exists(systemdirectory)==True:

            # contents of description file containing directory structure and checksums
            desc=[]

            # whether the description file exists
            descexist=False

            # the filename and path is the directory of the system plus the '-description.txt'
            descfiledir=systemdirectory+'-description.txt'

            # try opening the description file
            try:
                file=open(descfiledir,mode='rt')

                # try loading the contents into memory
                for line in file:
                    desc.append(line)
                file.close()

                # indicate that the description file exists
                descexist=True

            # if the description file does not exist, raise an error
            except:

                # acquire lock to print multiple lines
                # multithreaded so need to ensure all lines are printed together
                with lock:
                    print('ERROR: system: description file cannot be opened or is non-existant.')
                    print('________________________________________________')
                    print()

            # if the description file exists, start checking directory structure and checksums of all files
            if descexist:

		        # separate the contents of the description file into parts
		        # these parts are formatted so that it is clear what is the checksum of the description file
		        # or the directory structure
		        # or the files and their checksum
                parts=[]

                line=0
                length=len(desc)

		        # loop over all lines in the contents of the description file
                while line<length:

                    # temporary store for each part
                    temp=[]

                    # loop over all lines
                    while line<length:
                        line=line+1

                        # break current loop to finish a part if an empty line is detected
                        if desc[line-1]=='\n':
                            break

                        # remove newline character from all lines
                        temp.append(desc[line-1].strip('\n'))

                    # add part to list of parts
                    parts.append(temp)

                # this is the checksum of the description file
                descintegrity=parts[0]

                # list of lines from description file to be input to hashing algorithm
                integritycheck=[]
                
                # add all lines from parts (the description file)
                for i in range(1,len(parts)):
                    for line in parts[i]:
                        integritycheck.append(line)
                    integritycheck.append('')
                
                # stores the hashes, list so that more than one hashing algorithm can be used
                integrityhashes=[]

                # use SHA1 hashing algorithm
                sha1=hashlib.sha1()

                # input all lines into hashing algorithm
                for i in integritycheck:
                    sha1.update(i.encode('utf-8'))

                # return the checksum in hexadecimals
                integrityhashes.append(sha1.hexdigest())

                # if the checksum of the description file matches the calculated checksum
                # the description file is not corrupt
                if integrityhashes==descintegrity:

                    # list of directories and filepaths
                    dirstructure=[]

                    # list of files failed to be opened
                    failopen=[]

                    # add all directories and filepaths to dirstructure
                    for root, dirs, files in os.walk(str(os.getcwd())+'\\system'):
                            level=root.replace(str(os.getcwd())+'\\system','')
                            if level=='':
                                level='\\'
                            dirstructure.append(level)
                            for file in files:
                                filepath=os.path.join(level,file)
                                dirstructure.append(filepath)

                    # sort the list of directories and filepaths
                    # the final check is dependent on order
                    # so ensure order
                    dirstructure.sort()

                    # list of files
                    files=[]

                    # list of filepaths
                    filepaths=[]

                    # separate into files and filepaths
                    for l in dirstructure:
                        filepath=str(os.getcwd())+'\\system\\'+l
                        if os.path.isfile(filepath):
                            files.append(l)
                            filepaths.append(filepath)

                    # again, sort because the final check is order dependent
                    files.sort()
                    filepaths.sort()

                    # counter to go through all files
                    number=0

                    # list of files and their hashes
                    filehashes=[]

                    # for all files
                    while number<len(files):
                        
                        # try opening the file
                        try:

                            # temporary store
                            results=[]

                            # hash function
                            sha1=hashlib.sha1()

                            # open file in read binary mode
                            f=open(filepaths[number],'rb')

                            # read in blocks of 4096 bytes
                            # update hash function
                            while True:
                                buf=f.read(4096)
                                if not buf:
                                    break
                                sha1.update(buf)

                            # close file
                            f.close()

                            # add filepath and its checksum to result
                            results.append(files[number])
                            results.append(sha1.hexdigest())

                            # add result to list of files and hashes
                            filehashes.append(results)

                        # add filepaths of files that could not be opened
                        except:
                            failopen.append(files[number])

                        # next file
                        number=number+1

                    # final list for computing hash
                    final=[]

                    # add directory structure to final list
                    for l in dirstructure:
                        final.append(l)

                    final.append('')

                    # add all files and their checksums to final list
                    for l in filehashes:
                        for k in l:
                            final.append(k)
                        final.append('')

                    # final hash output, list so that multipe hash algorithms can be used
                    finalhash=[]

                    # algorithm
                    sha1=hashlib.sha1()

                    # add all final items into hashing algorithm
                    for l in final:
                        sha1.update(l.encode('utf-8'))

                    # hash output as hex
                    finalhash.append(sha1.hexdigest())

                    # if checksum of description file and calculated checksum are equal
                    # system files are not corrupt
                    if final==integritycheck:
                        with lock:
                            print('system: filesystem verified.')
                            print('________________________________________________')
                            print()

                    # otherwise the system is corrupt and an error is raised
                    else:
                        with lock:
                            print('ERROR: system: filesystem is corrupt.')
                            print('________________________________________________')
                            print()

                # if the calculated checksum of the description file does not match the checksum recorded
                # description file is corrupt and raise an error
                else:
                    with lock:
                        print('ERROR: system: description file is corrupt.')
                        print('________________________________________________')
                        print()
        
        # if the directory with the system files does not exist
        else:
            with lock:
                print('ERROR: system: directory does not exist.')
                print('________________________________________________')
                print()

        # only runs periodically
        time.sleep(10)

# subroutine to check the integrity of the files put in the store
def store(storedirectory):

    # keep this looping forever
    while True:

        # if the directory with the stored files exists
        if os.path.exists(storedirectory)==True:

            # list of all directories in store
            directories=[]
            
            # walk through and add all directories
            # only add top level directory paths
            for root,dirs,files in os.walk(storedirectory):
                directories.extend(dirs)
                break
            
            # for each directory
            for i in directories:

                # if the directory exists
                if os.path.exists(str(os.getcwd())+'\\store\\'+i+'-description.txt')==True:

                    # contents of description file containing directory structure and checksums
                    desc=[]

                    # whether the description file exists
                    descexist=False

                    # the filename and path is the directory plus '-description.txt'
                    descfiledir=storedirectory+'\\'+i+'-description.txt'

                    # try opening the description file
                    try:
                        file=open(descfiledir,mode='rt')

                        # try loading the contents into memory
                        for line in file:
                            desc.append(line)
                        file.close()

                        # indicate that the description file exists
                        descexist=True

                    # if the description file does not exist, raise an error
                    except:
                        with lock:
                            print('ERROR: store: description file of '+i+'  cannot be opened or is non-existant.')
                            print('________________________________________________')
                            print()

                    # if the description file exists, start checking directory structure and checksums of all files
                    if descexist:

                        # separate the contents of the description file into parts
		        # these parts are formatted so that it is clear what is the checksum of the description file
                        # or the directory structure
	                # or the files and their checksum
                        parts=[]

                        line=0
                        length=len(desc)

                        # loop over all lines in the contents of the description file
                        while line<length:

                            # temporary store for each part
                            temp=[]

                            # loop over all lines
                            while line<length:
                                line=line+1

                                # break current loop to finish a part if an empty line is detected
                                if desc[line-1]=='\n':
                                    break

                                # remove newline character from all lines
                                temp.append(desc[line-1].strip('\n'))

                            # add part to list of parts
                            parts.append(temp)

                        # this is the checksum of the description file
                        descintegrity=parts[0]

                        # list of lines from description file to be input to hashing algorithm
                        integritycheck=[]
                        
                        # add all lines from parts (the description file)
                        for l in range(1,len(parts)):
                            for line in parts[l]:
                                integritycheck.append(line)
                            integritycheck.append('')
                        
                        # stores the hashes, list so that more than one hashing algorithm can be used
                        integrityhashes=[]

                        # use SHA1 hashing algorithm
                        sha1=hashlib.sha1()

                        # input all lines into hashing algorithm
                        for l in integritycheck:
                            sha1.update(l.encode('utf-8'))

                        # return the checksum in hexadecimals
                        integrityhashes.append(sha1.hexdigest())

                        # if the checksum of the description file matches the calculated checksum
                        # the description file is not corrupt
                        if integrityhashes==descintegrity:

                            # list of directories and filepaths
                            dirstructure=[]

                            # list of files failed to be opened
                            failopen=[]

                            # add all directories and filepaths to dirstructure
                            for root, dirs, files in os.walk(str(os.getcwd())+'\\store\\'+i):
                                    level=root.replace(str(os.getcwd())+'\\store\\'+i,'')
                                    if level=='':
                                        level='\\'
                                    dirstructure.append(level)
                                    for file in files:
                                        filepath=os.path.join(level,file)
                                        dirstructure.append(filepath)

                            # sort the list of directories and filepaths
                            # the final check is dependent on order
                            # so ensure order
                            dirstructure.sort()

                            # list of files
                            files=[]

                            # list of filepaths
                            filepaths=[]

                            # separate into files and filepaths
                            for l in dirstructure:
                                filepath=str(os.getcwd())+'\\store\\'+i+l
                                if os.path.isfile(filepath):
                                    files.append(l)
                                    filepaths.append(filepath)

                            # again, sort because the final check is order dependent
                            files.sort()
                            filepaths.sort()

                            # counter to go through all files
                            number=0

                            # list of files and their hashes
                            filehashes=[]

                            # for all files
                            while number<len(files):
                                
                                # try opening the file
                                try:

                                    # temporary store
                                    results=[]
                                    
                                    # hash function
                                    sha1=hashlib.sha1()

                                    # open file in read binary mode
                                    f=open(filepaths[number],'rb')

                                    # read in blocks of 4096 bytes
                                    # update hash function
                                    while True:
                                        buf=f.read(4096)
                                        if not buf:
                                            break
                                        sha1.update(buf)

                                    # close file
                                    f.close()

                                    # add filepath and its checksum to result
                                    results.append(files[number])
                                    results.append(sha1.hexdigest())

                                    # add result to list of files and hashes
                                    filehashes.append(results)

                                # add filepaths of files that could not be opened
                                except:
                                    failopen.append(files[number])

                                # next file
                                number=number+1

                            # final list for computing hash
                            final=[]

                            # add directory structure to final list
                            for l in dirstructure:
                                final.append(l)

                            final.append('')

                            # add all files and their checksums to final list
                            for l in filehashes:
                                for k in l:
                                    final.append(k)
                                final.append('')

                            # final hash output, list so that multipe hash algorithms can be used
                            finalhash=[]

                            # algorithm
                            sha1=hashlib.sha1()

                            # add all final items into hashing algorithm
                            for l in final:
                                sha1.update(l.encode('utf-8'))

                            # hash output as hex
                            finalhash.append(sha1.hexdigest())

                            # if checksum of description file and calculated checksum are equal
                            # files are not corrupt
                            if final==integritycheck:
                                with lock:
                                    print('store: filesystem of '+i+' verified.')
                                    print('________________________________________________')
                                    print()
                            
                            # otherwise the files are corrupt and an error is raised
                            else:
                                with lock:
                                    print('ERROR: store: filesystem of '+i+' is corrupt.')
                                    print('________________________________________________')
                                    print()
                        
                        # if the calculated checksum of the description file does not match the checksum recorded
                        # description file is corrupt and raise an error
                        else:
                            with lock:
                                print('ERROR: store: description file of '+i+' is corrupt.')
                                print('________________________________________________')
                                print()
                
        # if the directory with the system files does not exist
        else:
            with lock:
                print('ERROR: store: store directory does not exist.')
                print('________________________________________________')
                print()

        # only runs periodically
        time.sleep(10)


# subroutine to check the integrity of incoming files
def incoming(incomingdirectory):

    # keep this looping forever
    while True:

        # if the directory with the incoming files exists
        if os.path.exists(incomingdirectory)==True:

            # list of all directories in incoming
            directories=[]
            
            # walk through and add all directories
            # only add top level directory paths
            for root,dirs,files in os.walk(incomingdirectory):
                directories.extend(dirs)
                break

            # for each directory
            for i in directories:

                # if the directory exists
                if os.path.exists(str(os.getcwd())+'\\incoming\\'+i+'-description.txt')==True:

                    # contents of description file containing directory structure and checksums
                    desc=[]

                    # whether the description file exists
                    descexist=False

                    # the filename and path is the directory plus '-description.txt'
                    descfiledir=incomingdirectory+'\\'+i+'-description.txt'

                    # try opening the description file
                    try:
                        file=open(descfiledir,mode='rt')

                        # try loading the contents into memory
                        for line in file:
                            desc.append(line)
                        file.close()

                        # indicate that the description file exists
                        descexist=True

                    # if the description file does not exist, raise an error
                    except:
                        with lock:
                            print('ERROR: incoming: description file cannot be opened or is non-existant.')
                            print('________________________________________________')
                            print()

                    # if the description file exists, start checking directory structure and checksums of all files
                    if descexist:

                        # separate the contents of the description file into parts
                        # these parts are formatted so that it is clear what is the checksum of the description file
                        # or the directory structure
                        # or the files and their checksum
                        parts=[]

                        line=0
                        length=len(desc)

                        # loop over all lines in the contents of the description file
                        while line<length:

                            # temporary store for each part
                            temp=[]

                            # loop over all lines
                            while line<length:
                                line=line+1

                                # break current loop to finish a part if an empty line is detected
                                if desc[line-1]=='\n':
                                    break

                                # remove newline character from all lines
                                temp.append(desc[line-1].strip('\n'))

                            # add part to list of parts
                            parts.append(temp)

                        # this is the checksum of the description file
                        descintegrity=parts[0]

                        # list of lines from description file to be input to hashing algorithm
                        integritycheck=[]

                        # add all lines from parts (the description file)
                        for l in range(1,len(parts)):
                            for line in parts[l]:
                                integritycheck.append(line)
                            integritycheck.append('')

                        # stores the hashes, list so that more than one hashing algorithm can be used
                        integrityhashes=[]

                        # use SHA1 hashing algorithm
                        sha1=hashlib.sha1()

                        # input all lines into hashing algorithm
                        for l in integritycheck:
                            sha1.update(l.encode('utf-8'))

                        # return the checksum in hexadecimals
                        integrityhashes.append(sha1.hexdigest())

                        # if the checksum of the description file matches the calculated checksum
                        # the description file is not corrupt
                        if integrityhashes==descintegrity:

                            # list of directories and filepaths
                            dirstructure=[]

                            # list of files failed to be opened
                            failopen=[]

                            # add all directories and filepaths to dirstructure
                            for root, dirs, files in os.walk(str(os.getcwd())+'\\incoming\\'+i):
                                    level=root.replace(str(os.getcwd())+'\\incoming\\'+i,'')
                                    if level=='':
                                        level='\\'
                                    dirstructure.append(level)
                                    for file in files:
                                        filepath=os.path.join(level,file)
                                        dirstructure.append(filepath)

                            # sort the list of directories and filepaths
                            # the final check is dependent on order
                            # so ensure order
                            dirstructure.sort()

                            # list of files
                            files=[]

                            # list of filepaths
                            filepaths=[]

                            # separate into files and filepaths
                            for l in dirstructure:
                                filepath=str(os.getcwd())+'\\incoming\\'+i+l
                                if os.path.isfile(filepath):
                                    files.append(l)
                                    filepaths.append(filepath)

                            # again, sort because the final check is order dependent
                            files.sort()
                            filepaths.sort()

                            # counter to go through all files
                            number=0

                            # list of files and their hashes
                            filehashes=[]

                            # for all files
                            while number<len(files):

                                # try opening the file
                                try:

                                    # temporary store
                                    results=[]

                                    # hash function
                                    sha1=hashlib.sha1()

                                    # open file in read binary mode
                                    f=open(filepaths[number],'rb')

                                    # read in blocks of 4096 bytes
                                    # update hash function
                                    while True:
                                        buf=f.read(4096)
                                        if not buf:
                                            break
                                        sha1.update(buf)

                                    # close file
                                    f.close()

                                    # add filepath and its checksum to result
                                    results.append(files[number])
                                    results.append(sha1.hexdigest())

                                    # add result to list of files and hashes
                                    filehashes.append(results)

                                # add filepaths of files that could not be opened
                                except:
                                    failopen.append(files[number])

                                # next file
                                number=number+1

                            # final list for computing hash
                            final=[]

                            # add directory structure to final list
                            for l in dirstructure:
                                final.append(l)

                            final.append('')

                            # add all files and their checksums to final list
                            for l in filehashes:
                                for k in l:
                                    final.append(k)
                                final.append('')

                            # final hash output, list so that multipe hash algorithms can be used
                            finalhash=[]

                            # algorithm
                            sha1=hashlib.sha1()

                            # add all final items into hashing algorithm
                            for l in final:
                                sha1.update(l.encode('utf-8'))

                            # hash output as hex
                            finalhash.append(sha1.hexdigest())

                            # if checksum of description file and calculated checksum are equal
                            # files are not corrupt
                            if final==integritycheck:
                                with lock:
                                    print('incoming: filesystem verified.')
                                    print('________________________________________________')
                                    print()

                                # if the incoming file and its description file exist
                                # if the file and description file do not already exist in the store
                                if os.path.exists(str(os.getcwd())+'\\incoming\\'+i)==True and os.path.exists(str(os.getcwd())+'\\incoming\\'+i+'-description.txt')==True and os.path.exists(str(os.getcwd())+'\\store\\'+i)==False and os.path.exists(str(os.getcwd())+'\\store\\'+i+'-description.txt')==False:

                                    # move the file and its description file to store
                                    shutil.move(str(os.getcwd())+'\\incoming\\'+i,str(os.getcwd())+'\\store')
                                    shutil.move(str(os.getcwd())+'\\incoming\\'+i+'-description.txt',str(os.getcwd())+'\\store')
                                    with lock:
                                        print('incoming: item moved from incoming to store.')
                                        print('________________________________________________')
                                        print()

                                # if there is already a file or a description file with the same name in store
                                # then cannot move file and descrption file
                                elif os.path.exists(str(os.getcwd())+'\\store\\'+i)==True and os.path.exists(str(os.getcwd())+'\\store\\'+i+'-description.txt')==True:
                                    with lock:
                                        print('ERROR: incoming: item cannot be moved from incoming to store because there are items with the same name.')
                                        print('________________________________________________')
                                        print()

                                # if the above two cases do not occur
                                else:
                                    with lock:
                                        print('ERROR: incoming: item cannot be moved from incoming to store.')
                                        print('________________________________________________')
                                        print()

                            # raise an error because file is corrupt
                            else:
                                with lock:
                                    print('ERROR: incoming: filesystem is corrupt.')
                                    print('________________________________________________')
                                    print()

                        # f the calculated checksum of the description file does not match the checksum recorded
                        # description file is corrupt and raise an error
                        else:
                            with lock:
                                print('ERROR: incoming: description file is corrupt.')
                                print('________________________________________________')
                                print()

        # if the directory with the incoming files does not exist
        else:
            with lock:
                print('ERROR: incoming: directory does not exist.')
                print('________________________________________________')
                print()

        # only runs periodically
        time.sleep(10)

# subroutine to calculate the checksums of all files
# record the directory structure and checksums of all files in a description file
def outgoing(outgoingdirectory):

    # keep this looping forever
    while True:

        # if the directory with the outgoing files exists
        if os.path.exists(outgoingdirectory)==True:

            # list of all directories in outgoing
            directories=[]

            # walk through and add all directories
            # only add top level directory paths
            for root,dirs,files in os.walk(outgoingdirectory):
                directories.extend(dirs)
                break

            # for each directory
            for i in directories:

                # if there is no description file already present
                # then create a description file
                if os.path.exists(str(os.getcwd())+'\\outgoing\\'+i+'-description.txt')==False:

                    # list of directories and filepaths
                    dirstructure=[]

                    # list of files failed to be opened
                    failopen=[]

                    # add all directories and filepaths to dirstructure
                    for root, dirs, files in os.walk(str(os.getcwd())+'\\outgoing\\'+i):
                            level=root.replace(str(os.getcwd())+'\\outgoing\\'+i,'')
                            if level=='':
                                level='\\'
                            dirstructure.append(level)
                            for file in files:
                                filepath=os.path.join(level,file)
                                dirstructure.append(filepath)

                    # sort the list of directories and filepaths
                    dirstructure.sort()

                    # list of files
                    files=[]

                    # list of filepaths
                    filepaths=[]

                    # separate into files and filepaths
                    for l in dirstructure:
                        filepath=str(os.getcwd())+'\\outgoing\\'+i+l
                        if os.path.isfile(filepath):
                            files.append(l)
                            filepaths.append(filepath)

                    # sort files and filepaths
                    files.sort()
                    filepaths.sort()

                    # counter to go through all files
                    number=0

                    # list of files and their hashes
                    filehashes=[]

                    # for all files
                    while number<len(files):

                        # try opening the file
                        try:

                            # temporary store
                            results=[]

                            # hash function
                            sha1=hashlib.sha1()

                            # open file in read binary mode
                            f=open(filepaths[number],'rb')
                            while True:
                                buf=f.read(4096)
                                if not buf:
                                    break
                                sha1.update(buf)

                            # close file
                            f.close()

                            # add filepath and its checksum to result
                            results.append(files[number])
                            results.append(sha1.hexdigest())

                            # add result to list of files and hashes
                            filehashes.append(results)

                        # add filepaths of files that could not be opened
                        except:
                            failopen.append(files[number])

                        # next file
                        number=number+1

                    # final list for computing hash
                    final=[]

                    # add directory structure to final list
                    for l in dirstructure:
                        final.append(l)

                    final.append('')

                    # add all files and their checksums to final list
                    for l in filehashes:
                        for k in l:
                            final.append(k)
                        final.append('')

                    # final hash output, list so that multipe hash algorithms can be used
                    finalhash=[]

                    # algorithm
                    sha1=hashlib.sha1()

                    # add all final items into hashing algorithm
                    for l in final:
                        sha1.update(l.encode('utf-8'))

                    # hash output as hex
                    finalhash.append(sha1.hexdigest())

                    # create description file
                    with open(str(os.getcwd())+'\\outgoing\\'+i+'-description.txt','wt') as create:

                        # record all checksums of description file contents
                        for l in finalhash:
                            create.write(l)
                            create.write('\n')

                        # separate the checksums for the description file contents and the description itself
                        create.write('\n')

                        # record the description (directory structure and file checksums)
                        for l in final:
                            create.write(l)
                            create.write('\n')

                    # close the description file
                    create.close()

                # if the outgoing file and its description file exist
                # if the file and description file do not already exist in the sent directory
                if os.path.exists(str(os.getcwd())+'\\outgoing\\'+i)==True and os.path.exists(str(os.getcwd())+'\\outgoing\\'+i+'-description.txt')==True and os.path.exists(str(os.getcwd())+'\\sent\\'+i)==False and os.path.exists(str(os.getcwd())+'\\sent\\'+i+'-description.txt')==False:

                    # move the file and its description file to sent
                    shutil.move(str(os.getcwd())+'\\outgoing\\'+i,str(os.getcwd())+'\\sent')
                    shutil.move(str(os.getcwd())+'\\outgoing\\'+i+'-description.txt',str(os.getcwd())+'\\sent')
                    with lock:
                        print('outgoing: item moved from outgoing to sent.')
                        print('________________________________________________')
                        print()

                # if there is already a file or a description file with the same name in sent
                # then cannot move file and descrption file
                elif os.path.exists(str(os.getcwd())+'\\sent\\'+i)==True and os.path.exists(str(os.getcwd())+'\\sent\\'+i+'-description.txt')==True:
                    with lock:
                        print('ERROR: outgoing: item cannot be moved from outgoing to sent because there are items with the same name.')
                        print('________________________________________________')
                        print()

                # if the above two cases do not occur
                else:
                    with lock:
                        print('ERROR: outgoing: item cannot be moved from outgoing to sent.')
                        print('________________________________________________')
                        print()

        # if the directory with the outgoing files does not exist
        else:
            with lock:
                print('ERROR: outgoing: directory does not exist.')
                print('________________________________________________')
                print()

        # only runs periodically
        time.sleep(10)


# main

# define a lock so that the lock can be acquired when printing multiple lines
# prevents different prints from interleaving each other
lock=threading.RLock()

# start thread for checking the integrity of the system files
systemthread=threading.Thread(target=system, args=(str(os.getcwd())+'\\system',))

# start thread for checking the integrity of the stored files
storethread=threading.Thread(target=store, args=(str(os.getcwd())+'\\store',))

# start thread for checking the integrity of the incoming files and to move to store if not corrupt
incomingthread=threading.Thread(target=incoming, args=(str(os.getcwd())+'\\incoming',))

# start thread for creating description files for outgoing files
# then move files and description file to sent
outgoingthread=threading.Thread(target=outgoing, args=(str(os.getcwd())+'\\outgoing',))

#start threads
systemthread.start()
storethread.start()
incomingthread.start()
outgoingthread.start()

# wait for all threads to end before ending main 
systemthread.join()
storethread.join()
incomingthread.join()
outgoingthread.join()
