Introduction
============


.. image:: https://readthedocs.org/projects/micropython-uplot/badge/?version=latest
    :target: https://micropython-uplot.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/micropython-Ok-purple.svg
    :target: https://micropython.org
    :alt: micropython

.. image:: https://img.shields.io/pypi/v/micropython-uplot.svg
    :alt: latest version on PyPI
    :target: https://pypi.python.org/pypi/micropython-uplot

.. image:: https://static.pepy.tech/personalized-badge/micropython-uplot?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Pypi%20Downloads
    :alt: Total PyPI downloads
    :target: https://pepy.tech/project/micropython-uplot

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

MicroPython Graphics Library. This library uses the IL9486 driver from Peter Hinch taken from
https://github.com/peterhinch/micropython-nano-gui. with a Waveshare 3.5 display
This library uses FrameBuffer. It could work for other displays, however, is not my intention to
apadated or provide this functionality. This is an exercise to learn MicroPython Graphics adapting
the following library from CircuitPython
https://github.com/jposada202020/CircuitPython_uplot

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
