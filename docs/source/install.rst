

============
Installation
============

Introduction
============

This section of the documentation shows how to install capy.
We will cover the steps you will need to take to get capy up and running.

Python
======

capy requires python to be installed before it can be used. We will
walk through the steps of achieving this for each major platform.
It is recommended to use python version 3.8 or above.
capy is NOT backwards compatible with python 2!

To check what version of python you have installed,
you can run the following command in your terminal to find out:

.. code-block:: terminal

    $ python --version

This will print the python version. If you run this command 
on python 3.9, the output will look something like this:

.. code-block:: bash

    Python 3.9.5

Linux
-----

You can install python using your system's package manager.
Below, we will install python 3.8 and pip using apt, the Debian package manager:

.. code-block:: bash

    $ apt install python3.8 python3-pip

It is important to specify the python 3 version of pip, or else it will not work correctly!

Windows
-------

Windows users can download the `python installer <https://www.python.org/downloads/>`_.
The installation is pretty straightforward, although we recommend adding python to your PATH environment
variable, as it makes using python much easier.

Mac
---

You can find installation instructions `here <https://docs.python-guide.org/starting/install3/osx/>`_.

Installation via pip
====================

You can install capy using pip like so:

.. code-block:: bash

    $ pip install capy

To learn more about PIP and installing third party modules in general, check out the
`Tutorial on installing packages <https://packaging.python.org/tutorials/installing-packages/>`_.

Source Code
===========

You can acquire the source code from github like so:

.. code-block:: bash

    git clone https://github.com/Owen-Cochell/capy

This will download the repository to your computer via git.
You can then reference the package from your application,
or install it using pip

.. code-block:: bash

    $ cd capy  # Navigate to the installed directory
    $ pip install .

You can also get the tarball from github, which you can download like so:

.. code-block:: bash

    $ curl -ol https://github.com/Owen-Cochell/capy/tarball/master

Updating
========

If you installed using pip, you can preform an update like so:

.. code-block:: bash

    $ pip install capy --upgrade

This will update capy if necessary.
