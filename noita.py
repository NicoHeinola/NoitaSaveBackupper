
import os
from turtle import back
from typing import Dict, List
import json
import shutil


class NoitaManager:
    noitaSaveLocation = r"C:\Users\\"+os.getlogin()+r"\AppData\LocalLow\Nolla_Games_Noita"
    noitaSaveName = r"save00"
    backupFolder = "backups"
    dataFilename = "data.json"

    @staticmethod
    def getSaveNamePath() -> str:
        """Returns a path to the current save folder

        Returns:
            str: path
        """
        return os.path.join(NoitaManager.noitaSaveLocation, NoitaManager.noitaSaveName)

    @staticmethod
    def getBackupLocation() -> str:
        """Returns a path to folder containing all backups

        Returns:
            str: path
        """
        return os.path.join(NoitaManager.noitaSaveLocation, NoitaManager.backupFolder)

    @staticmethod
    def getDatafilePath() -> str:
        """Returns a path to data.json

        Returns:
            str: path
        """
        return os.path.join(NoitaManager.noitaSaveLocation, NoitaManager.backupFolder, NoitaManager.dataFilename)

    @staticmethod
    def getBackups() -> List:
        dataFilepath: str = NoitaManager.getDatafilePath()
        if os.path.exists(dataFilepath):
            with open(dataFilepath) as file:
                backups = json.load(file)["backups"]
                if type(backups) == list:
                    return backups
        return []

    @staticmethod
    def __generateNewId(data: dict) -> int:
        """Generates a new valid id that doesn't exist yet for a new Noita world backup

        Args:
            data (dict): Contains all information for all current backups

        Returns:
            int: Next valid id
        """
        nextID = 0
        for d in data:
            id = d["id"]
            if id >= nextID:
                nextID = id + 1
        return nextID

    @staticmethod
    def __generateFoldername(id: int):
        """Generates a name for the folder where Noita world backup is stored in

        Args:
            id (int): Used to create unique filenames

        Returns:
            str: A new valid foldername
        """
        return "backup" + str(id)

    @staticmethod
    def saveBackupData(backupData: List) -> None:
        """Overwrites current backup info with new info

        Args:
            backupData (List): Contains all backup data. For example: [{'name': 'test', ...},{...}]
        """
        with open(NoitaManager.getDatafilePath(), 'w+') as file:
            json.dump({"backups": backupData}, file)

    @staticmethod
    def removeBackup(id: int):
        """Removes a Noita world backup both from data.json and harddrive

        Args:
            id (int): Id of backup to remove
        """
        # Finds the backup to remove and prepares a new list of backups without the one being removed
        oldBackups: list = NoitaManager.getBackups()
        newBackups: list = oldBackups.copy()
        backupToRemove: list = None
        for b in oldBackups:
            if b["id"] == id:
                backupToRemove = b
                newBackups.remove(b)
                break
        
        if backupToRemove == None:
            return
        
        # Removes backup from harddrive
        removedBackupPath: str = os.path.join(
            os.path.join(
                NoitaManager.getBackupLocation(), backupToRemove["folder"])
        )

        shutil.rmtree(removedBackupPath)

        # Lastly removes the backup from backup data file
        NoitaManager.saveBackupData(newBackups)

    @staticmethod
    def modifyBackupData(id: int, name: str = None, description: str = None):
        """Modifies saved name (aka. title) and description of a backup

        Args:
            id (int): Id of a backup to modify
            name (str, optional): New name of a backup.
            description (str, optional): New description of a backup.
        """
        backups: List = NoitaManager.getBackups()
        for b in backups:
            if b["id"] == id:
                if name is not None:
                    b["name"] = name
                if description is not None:
                    b["description"] = description
                break

        NoitaManager.saveBackupData(backups)

    @staticmethod
    def saveWorld(name: str, description: str) -> bool:
        """Saves info into a data.json and then copies current Noita world into a backup folder

        Args:
            name (str): A title for the world
            description (str): Describes what kind of a world it is

        Returns:
            bool: If any errors occurred
        """
        
        if name is None:
            name = ""
        if description is None:
            description = ""
                    
        # Creates a backup folder if one does not already exist
        backupsPath: str = NoitaManager.getBackupLocation()
        if not os.path.exists(backupsPath):
            os.mkdir(backupsPath)

        # Loads any existing backup data, so it can append to it
        oldData: list = NoitaManager.getBackups()

        # Makes a backup of current Noita world
        id: int = NoitaManager.__generateNewId(oldData)
        folder: str = NoitaManager.__generateFoldername(id)  # Backup folder

        saveNamePath: str = NoitaManager.getSaveNamePath()
        newBackupFolder: str = os.path.join(backupsPath, folder)
        shutil.copytree(saveNamePath, newBackupFolder)

        # Adds new backup to data.json
        toAppend: dict = {
            "id": id, "folder": folder, "name": name, "description": description
        }
        oldData.append(toAppend)
        NoitaManager.saveBackupData(oldData)

        return True

    @staticmethod
    def loadBackup(id: int):
        """Replaces current Noita world with a backup

        Args:
            id (int): id of the backup
        """
        backups: list = NoitaManager.getBackups()
        # Loops through backups, removes current save, copies backup into the current one's place
        for b in backups:
            if b["id"] == id:
                noitaSavePath: str = NoitaManager.getSaveNamePath()

                # Removes current save
                if(os.path.exists(noitaSavePath)):
                    shutil.rmtree(noitaSavePath)

                # Gets backup location
                backupFolderPath: str = os.path.join(
                    NoitaManager.getBackupLocation(), b["folder"])

                # Copies backup to the place of the current save
                shutil.copytree(backupFolderPath, noitaSavePath)
                break