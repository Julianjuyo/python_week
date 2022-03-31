import os
import main as file

'''
-------------------------------------
Team name: Driven By Data
Team Id: 10

Yash Kumar Jain
Mohamad Serhan
Julian esteban Oliveros forero
Qinghua Ye
-------------------------------------
'''

def readFile(filePath):

    with open(filePath, 'r') as f:
        listl = []
        for line in f:
            strip_lines = line.strip()
            listli = strip_lines.split()
            listl.append(listli)
    del listl[0]
    return listl

def findGlobalScore(filepath,sortingFile):

def runScript(af,ad,aaa):


    return af

if __name__ == '__main__':

    # os.system("main.py")

    GlobalRoboticSatisfaction=0

    writePathStart ="output/"
    directory = 'data/'

    dictWithSubgroups = {
        "1_binary_landscapes.txt": 9000,
        "11_randomizing_paintings.txt": 11000,
        "110_oily_portraits.txt": "1964",
        "0_example.txt": 10,
        "10_computable_moments.txt": 2000
    }

    # iterate over files in
    # that directory
    for filename in os.scandir(directory):
        if filename.is_file():

            compare = filename.path

            print(filename.path)

            if compare in dictWithSubgroups:

                GlobalRoboticSatisfaction = GlobalRoboticSatisfaction + file.runScript(filename.path,writePathStart+filename.path,dictWithSubgroups[compare])


    print("--------------------------------------")
    print("GLOBAL ROBOT SATISFACTION IS:" +GlobalRoboticSatisfaction)
    print("--------------------------------------")