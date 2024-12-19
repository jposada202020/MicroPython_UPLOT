⛔️ DEPRECATED
===============

This repository is no longer supported, please consider using alternatives.

.. image:: http://unmaintained.tech/badge.svg
  :target: http://unmaintained.tech
  :alt: No Maintenance Intended

MicroPython Graphics Library. This library uses the IL9486 driver from Peter Hinch taken from
https://github.com/peterhinch/micropython-nano-gui. with a Waveshare 3.5 display
This library uses FrameBuffer. It could work for other displays, however, is not my intention to
adapt or provide this functionality. This is an exercise to learn MicroPython Graphics adapting
the following library from CircuitPython
https://github.com/jposada202020/CircuitPython_uplot

Take a look in the `examples <https://micropython-uplot.readthedocs.io/en/latest/examples.html>`_ section in RTD to see the gallery


.. image:: https://github.com/jposada202020/MicroPython_UPLOT/blob/main/docs/readme1.png


Installing with mip
====================
To install using mpremote

.. code-block:: shell

    mpremote mip install github:jposada202020/MicroPython_UPLOT

To install directly using a WIFI capable board

.. code-block:: shell

    mip.install("github:jposada202020/MicroPython_UPLOT")


Installing Library Examples
============================

If you want to install library examples:

.. code-block:: shell

    mpremote mip install github:jposada202020/MicroPython_UPLOT/examples.json

To install directly using a WIFI capable board

.. code-block:: shell

    mip.install("github:jposada202020/MicroPython_UPLOT/examples.json")


Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/micropython-uplot/>`_.
To install for current user:

.. code-block:: shell

    pip3 install micropython-uplot

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install micropython-uplot

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install micropython-uplot


Usage Example
=============

Take a look at the examples directory

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://micropython-uplot.readthedocs.io/en/latest/>`_.
