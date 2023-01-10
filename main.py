from statistics import mode
from typing import List
import eel
from noita import NoitaManager
import ctypes

print(eel)

eel.init('static_web_folder')
eel.browsers.set_path('electron', 'node_modules/electron/dist/electron')


@eel.expose
def SaveWorld(name: str, description: str) -> list:
    NoitaManager.saveWorld(name, description)
    return NoitaManager.getBackups()


@eel.expose
def LoadWorld(id: int):
    NoitaManager.loadBackup(id)


@eel.expose
def RemoveBackup(id: int) -> list:
    NoitaManager.removeBackup(id)
    return NoitaManager.getBackups()


@eel.expose
def ModifyBackup(id: int, name: str = None, description: str = None) -> list:
    NoitaManager.modifyBackupData(id, name, description)
    return NoitaManager.getBackups()


@eel.expose
def GetBackups() -> list:
    return NoitaManager.getBackups()


def hideConsole():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
hideConsole()

eel.start('index.html', mode="electron")