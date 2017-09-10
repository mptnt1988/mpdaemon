mpdaemon
========
Wrapper of `python-daemon <https://pypi.python.org/pypi/python-daemon/>`_ for easy use.

Installation
============
Source
~~~~~~
::

 git clone https://github.com/mptnt1988/mpdaemon.git
 cd mpdaemon
 pip install .

PyPI
~~~~
::

 pip install mpdaemon

Usage
=====
Initialization
~~~~~~~~~~~~~~
::

 mpdaemon init

Implementation
~~~~~~~~~~~~~~
See examples

Running
~~~~~~~
Assume that script file is script.py
::

 python script.py start
 python script.py status
 python script.py restart
 python script.py stop

Log file is */var/log/mpdaemon/script.log*

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
     daemon.run_func(log_to_file, daemon)

Example 2
~~~~~~~~~
example2.py

.. code-block:: python

 from mpdaemon import DaemonWrapper
 import time
 import schedule


 def job():
     execfile('writeDate.py')


 def scheduling(daemon, t_mins):
     while True:
         schedule.every(t_mins).minutes.do(job)
         while True:
             schedule.run_pending()
             time.sleep(1)


 if __name__ == "__main__":
     daemon = DaemonWrapper()
     daemon.run_func(scheduling, daemon, 1)

writeDate.py

.. code-block:: python

 import datetime


 with open('/tmp/dateInfo.txt', 'a') as outFile:
     outFile.write(str(datetime.datetime.now()) + '\n')
