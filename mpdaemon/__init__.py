from .mpdaemon import DaemonWrapper
import sys
import subprocess
import os
import getpass


def main():
    """Entry point for the application script"""
    if len(sys.argv) == 2 and sys.argv[1] == 'init':
        init_pid_dir()
        init_log_dir()
        print("MPDaemon successfully initiated.")
    else:
        print("HELP: Run \"mpdaemon init\"")
        sys.exit(1)


def init_pid_dir():
    pidDir = "/tmp/mpdaemon/run/"
    makeDirCmd = _make_dir_cmd(pidDir)
    changeOwnerCmd = _change_dir_owner_cmd(pidDir)
    _init_dir(makeDirCmd, changeOwnerCmd)


def init_log_dir():
    logDir = "/var/log/mpdaemon/"
    sudo = "/usr/bin/sudo"
    makeDirCmd = _make_dir_cmd(logDir)
    makeDirCmd.insert(0, sudo)
    changeOwnerCmd = _change_dir_owner_cmd(logDir)
    changeOwnerCmd.insert(0, sudo)
    _init_dir(makeDirCmd, changeOwnerCmd)


def _init_dir(makeDirCmd, changeOwnerCmd):
    subprocess.call(makeDirCmd)
    returnCode = subprocess.call(changeOwnerCmd)
    if returnCode:
        print("Failed to initiate MPDaemon.")
        sys.exit(1)


def _make_dir_cmd(directory):
    return ["mkdir", "-p", directory]


def _change_dir_owner_cmd(directory):
    return ["chown", "-R", getpass.getuser() + ":", directory]
