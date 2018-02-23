mpdaemon
========
Wrapper of `python-daemon <https://pypi.python.org/pypi/python-daemon/>`_ (with modification) for easy use.

Installation
============
Source
~~~~~~
::

 git clone https://github.com/mptnt1988/mpdaemon.git
 cd mpdaemon
 pip3 install .

PyPI
~~~~
::

 pip3 install mpdaemon

Usage
=====
APIs
~~~~

.. code-block:: python

 daemon = DaemonWrapper(serviceName=None, func=None, *args, **kwargs)

If *serviceName* is None, it defaults to script's ext-stripped filename.

**func(*args, \*\*kwargs)** will be executed when running daemon.run()

.. code-block:: python

 daemon.run(func=None, *a, **ka)

Execute specified **func(*a, \*\*ka)**. If func is None, *daemon*'s func & args initialized in the constructor is executed.

Implementation
~~~~~~~~~~~~~~
See examples

Running
~~~~~~~
Assume that script file is script.py
::

 python3 script.py start
 python3 script.py status
 python3 script.py restart
 python3 script.py stop

Log file is *~/.mpdaemon/log/<service_name>.log*

PID file is *~/.mpdaemon/pid/<service_name>.pid*

(<service_name> is specified in script.py or 'script' by default)

Examples
========
Example 1
~~~~~~~~~
example1.py

.. code-block:: python

 from mpdaemon import DaemonWrapper
 import time


 def log_to_file(daemon):
     while True:
         daemon.logger.info("Testing")
         time.sleep(1)


 if __name__ == "__main__":
     daemon = DaemonWrapper()
     daemon.run(log_to_file, daemon)

Example 2
~~~~~~~~~
example2.py

.. code-block:: python

 from mpdaemon import DaemonWrapper
 import time
 import schedule


 def job():
     exec(open("/tmp/writeDate.py").read())


 def scheduling(t_mins):
     schedule.every(t_mins).minutes.do(job)
     while True:
         schedule.run_pending()
         time.sleep(1)


 if __name__ == "__main__":
     daemon = DaemonWrapper(None, scheduling, 1)
     daemon.run()

/tmp/writeDate.py

.. code-block:: python

 import datetime


 with open('/tmp/dateInfo.txt', 'a') as outFile:
     outFile.write(str(datetime.datetime.now()) + '\n')
