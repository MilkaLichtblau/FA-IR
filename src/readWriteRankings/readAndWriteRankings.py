'''
Created on Mar 29, 2017

utility module to load and store ranking data

@author: meike.zehlike
'''
import os
import csv
import pickle


def loadPicklesFromDirectory(path):
    """
    loads all ranking pickles from a directory
    """
    allRankings = dict()

    for root, _, files in os.walk(path):
        for filename in files:
            if "gitignore" in filename:
                # FIXME: quick fix for SAT directory
                continue
            pickle = loadPickleFromDisk(root + filename)
            allRankings[filename.lower()] = pickle
    return allRankings


def loadPicklesFromSubDirs(path):
    """
    loads all pickles from all subdirectories of the given path and returns a two layered dictionary
    containing the directories as first layer key and the filename as second

    @param path: path to the root directory to be searched for pickles

    Return:
    -------
    a two layered dictionary data structure that contains all ranking pickles from subdirs, looking like this:

    subdir1 :    | filename1 : ranking1
                 | filename2 : ranking2

    subdir2 :    | filename1 : ranking1
                 | filename2 : ranking2
    """
    allRankings = dict()

    for root, dirs, files in os.walk(path):
        for directory in dirs:
            subdirPickles = dict()
            for root, dirs, files in os.walk(path + directory):
                for filename in files:
                    pickle = loadPickleFromDisk(root + '/' + filename)
                    subdirPickles[filename.lower()] = pickle
            allRankings[directory] = subdirPickles
    return allRankings


def writePickleToDisk(data, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def loadPickleFromDisk(filename):
    with open(filename, 'rb') as handle:
        data = pickle.load(handle)
    return data


def convertAllPicklesToCSV(sourceRootDir, destRootDir):
    for root, _, filenames in os.walk(sourceRootDir):
        for filename in filenames:
            if filename.endswith('.pickle'):
                # load candidate objects
                rankedCandidates = loadPickleFromDisk(root + '/' + filename)
                # write into csv file
                destDir = destRootDir + root.replace(sourceRootDir, "") + '/FA-IR/'
                if not os.path.exists(destDir):
                    os.makedirs(destDir)
                destPath = destDir + filename.replace(".pickle", ".csv")
                print(destPath)
                with open(destPath, 'wt') as file:
                    writer = csv.writer(file)
                    writer.writerow(("query_id", "position", "score", "protAttr"))
                    for candidate in rankedCandidates:
                        row = (int(candidate.stuffToSave.get("query_id")),
                               int(candidate.stuffToSave.get("position")),
                               candidate.originalQualification,
                               int(candidate.isProtected))
                        writer.writerow(row)
