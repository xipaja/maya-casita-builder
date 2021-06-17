from maya import cmds
import os
import json
import pprint

# The directory where Maya is in user's computer 
USER_APP_DIR = cmds.internalVar(userAppDir = True)

# Concatenate user app directory with casitaBuilder
DIRECTORY = os.path.join(USER_APP_DIR, 'casitaBuilder')

def createDirectory(directory = DIRECTORY):
    """
    Creates the given directory if it doesn't already exist
    
    Args:
        directory (str): The directory to create
    """

    if not os.path.exists(directory):
        os.mkdir(directory)

class CasitaLibrary(dict):

    def save(self, fileName, directory = DIRECTORY, screenshot = True, **infoDict):
        createDirectory(directory)

        # The path to save user's file to as ma file
        filePath = os.path.join(directory, '%s.ma' % fileName)

        infoFile = os.path.join(directory, '%s.json' % fileName)

        # Add new keys, name and path, to dict for saving file 
        infoDict['name'] = fileName
        infoDict['path'] = filePath

        cmds.file(rename = filePath)

        # If user makes a selection, export just that; if not, save the whole file
        if cmds.ls(selection = True):
            cmds.file(force = True, type = 'mayaAscii', exportSelected = True)
        else:
            cmds.file(save = True, type = 'mayaAscii', force = True)


        # TODO: Screenshot stuff

        # Dump dictionary information into a JSON
        with open(infoFile, 'w') as jsonFile:
            json.dump(infoDict, jsonFile, indent = 4)

        # Update self with the dictionary every time user saves
        self[fileName] = infoDict


    def find(self, directory = DIRECTORY):
        """
        Finds casita parts on disk

        Args:
            directory (str): the directory to search in
        """

        # Clear out to avoid duplicates
        self.clear()

        # No saved casita parts
        if not os.path.exists(directory):
            return

        filesInDirectory = os.listdir(directory)

        # Append found files to array if it is a Maya file
        mayaFiles = [foundFile for foundFile in filesInDirectory if foundFile.endswith('.ma')]

        for mayaFile in mayaFiles:
            # Split text from file path to return name and extension separately
            fileName, fileExt = os.path.split(mayaFile)

            fullPath = os.path.join(directory, mayaFile)

            # Save our info from our dictionary above 
            infoFile = '%s.json' % fileName

            # If there is an infoFile json, load json data from the filestream we just opened 
            # Store it into info var
            if infoFile in filesInDirectory:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as f:
                    info = json.load(f)

            else:
                info = {}

            # TODO: More screenshot stuff

        
        # Populate dictionary in case the info isn't there after emptying
        info['name'] = fileName
        info['path'] = fullPath

        # Assign key fileName to info dictionary values
        self[fileName] = info

        pprint.pprint(self)