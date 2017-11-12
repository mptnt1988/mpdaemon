from .daemon import runner
import __main__
import os
import logging
from lockfile import LockFailed
import sys


class DaemonWrapper:
    class App():
        def __init__(self, serviceName, pidFile):
            self.stdin_path = "/dev/null"
            self.stdout_path = "/dev/tty"
            self.stderr_path = "/dev/tty"
            self.pidfile_path = pidFile
            self.pidfile_timeout = 5
            self.running_func = lambda: None
            self.running_func_args = ((), {})

        def run(self):
            (args, kwargs) = self.running_func_args
            self.running_func(*args, **kwargs)

    def __init__(self):
        serviceName = os.path.basename(__main__.__file__).strip(".py")
        self._pidFile = "/tmp/mpdaemon/run/" + serviceName + ".pid"
        self._logFile = "/var/log/mpdaemon/" + serviceName + ".log"

        # Logging
        self._loggerName = "MPDaemon_" + serviceName
        self._logger = logging.getLogger(self._loggerName)
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        try:
            handler = logging.FileHandler(self._logFile)
        except (IOError):
            self._mpdaemon_init_error()
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.info("Command: " + " ".join(sys.argv[1:]))

        # App
        self._app = DaemonWrapper.App(serviceName, self._pidFile)
        if len(sys.argv) == 2 and sys.argv[1] == 'status':
            try:
                with open(self._pidFile, 'r') as f:
                    pid = int(f.read().strip())
            except (IOError, TypeError):
                pid = 0
            if pid:
                print("Process is running...")
            else:
                print("Process not running!")
            sys.exit(0)
        else:
            self._daemon_runner = runner.DaemonRunner(self._app)
            self._daemon_runner.daemon_context.files_preserve = [handler.stream]

    @property
    def logger(self):
        return self._logger

    def run_func(self, func, *args, **kwargs):
        self._app.running_func = func
        self._app.running_func_args = (args, kwargs)
        try:
            self._daemon_runner.do_action()
        except (LockFailed):
            self._mpdaemon_init_error()

    def _mpdaemon_init_error(self):
        print("HELP: Try \"mpdaemon init\" first")
        sys.exit(1)
