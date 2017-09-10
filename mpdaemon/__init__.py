from .mpdaemon import DaemonWrapper
import sys
import subprocess
import os


def main():
    """Entry point for the application script"""
    if len(sys.argv) == 2 and sys.argv[1] == 'init':
        pidDir = "/tmp/mpdaemon/run/"
        if os.path.isdir(pidDir):
            print("MPDaemon already initiated.")
        else:
            returnCode = subprocess.call(["mkdir", "-p", pidDir])
            if returnCode == 0:
                print("MPDaemon has been initiated.")
            else:
                print("Failed to initiate MPDaemon.")
            sys.exit(returnCode)
    else:
        print("HELP: Run \"mpdaemon init\"")
        sys.exit(1)
