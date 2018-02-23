from .daemon import runner
import __main__
import os
import logging
from lockfile import LockFailed
import sys
from pathlib import Path


class DaemonWrapper:
    class App():
        def __init__(self, pidFile, func, *a, **ka):
            # for runner.DaemonRunner
            self.stdin_path = '/dev/null'
            self.stdout_path = '/dev/tty'
            self.stderr_path = '/dev/tty'
            self.pidfile_path = pidFile
            self.pidfile_timeout = 0.1
            # extra configs
            self.func = func
            self.args = a, ka

        def run(self):
            a, ka = self.args
            self.func(*a, **ka)

    def __init__(self, serviceName=None, func=None, *args, **kwargs):
        # serviceName defaults to script's ext-stripped filename
        if not serviceName:
            serviceName = os.path.basename(__main__.__file__).strip('.py')
        elif type(serviceName) is not str:
            self._handle_error()

        # func returns None by default
        if not func:
            func = lambda *a, **ka: None
        elif not callable(func):
            self._handle_error()

        # prepare dirs for pid file and log file
        home = str(Path.home())
        appDir = os.path.join(home, '.mpdaemon')
        pidDir = os.path.join(appDir, 'pid')
        logDir = os.path.join(appDir, 'log')
        Path(pidDir).mkdir(parents=True, exist_ok=True)
        Path(logDir).mkdir(parents=True, exist_ok=True)
        self._pidFile = os.path.join(pidDir, serviceName + '.pid')
        self._logFile = os.path.join(logDir, serviceName + '.log')

        # LOGGING
        self._loggerName = 'MPDaemon_' + serviceName
        self._logger = logging.getLogger(self._loggerName)
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        try:
            handler = logging.FileHandler(self._logFile)
        except (IOError):
            self._handle_error()
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.info('Command: ' + ' '.join(sys.argv[1:]))

        # DAEMON APP
        self._app = DaemonWrapper.App(self._pidFile, func, *args, **kwargs)
        if len(sys.argv) == 2 and sys.argv[1] == 'status':
            try:
                with open(self._pidFile, 'r') as f:
                    pid = int(f.read().strip())
            except (IOError, TypeError):
                pid = 0
            if pid:
                print('Process is running...')
            else:
                print('Process not running!')
            sys.exit(0)
        else:
            self._daemon_runner = runner.DaemonRunner(self._app)
            self._daemon_runner.daemon_context.files_preserve = [handler.stream]

    @property
    def logger(self):
        return self._logger

    def run(self, func=None, *a, **ka):
        """
        func=None means using default func
        """
        if func:
            if callable(func):
                self._app.func = func
                self._app.args = a, ka
            else:
                self._handle_error()

        try:
            self._daemon_runner.do_action()
        except (LockFailed):
            self._handle_error()

    def _handle_error(self):
        print('Some error')
        sys.exit(1)
