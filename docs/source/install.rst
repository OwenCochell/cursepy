============
Installation
============

Introduction
============

This section of the documentation shows how to install cursepy.
We will cover the steps you will need to take to get cursepy up and running.

Python
======

cursepy requires python to be installed before it can be used. We will
walk through the steps of achieving this for each major platform.
It is recommended to use python version 3.7 or above!
Using a lower version can and will lead to performance issues, 
as the typing module is very slow in previous versions!
cursepy is NOT backwards compatible with python 2!

To check what version of python you have installed,
you can run the following command in your terminal to find out:

.. code-block:: bash

    $ python --version

This will print the python version. If you run this command 
on python 3.9, the output will look something like this:

.. code-block:: bash

    Python 3.9.5

If the above command does not return python 7.x or above,
then you may have to manually specify the python version like so:

.. code-block:: bash

    $ python3 --version 

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

You can install cursepy using pip like so:

.. code-block:: bash

    $ pip install cursepy

To learn more about PIP and installing third party modules in general, check out the
`Tutorial on installing packages <https://packaging.python.org/tutorials/installing-packages/>`_.

Source Code
===========

You can acquire the source code from github like so:

.. code-block:: bash

    git clone https://github.com/Owen-Cochell/cursepy

This will download the repository to your computer via git.
You can then reference the package from your application,
or install it using pip:

.. code-block:: bash

    $ cd cursepy  # Navigate to the installed directory
    $ pip install .

You can also get the tarball from github, which you can download like so:

.. code-block:: bash

    $ curl -ol https://github.com/Owen-Cochell/cursepy/tarball/master

Updating
========

If you installed using pip, you can preform an update like so:

.. code-block:: bash

    $ pip install cursepy --upgrade

This will update cursepy if necessary.
