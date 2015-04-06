## Seawolf Software Install

Notes on installing Seawolf stuff.

URC's software was written with Fedora, Debian, Mint, and Ubuntu in mind. All the software _should_ work on Mac as well.

We assume some basic command line knowledge in order to complete this.

### System Packages

Install these system packages with your package manager. The package names given are Debian, Ubuntu, or Mint packages. If you have Fedora, use the packages in parenthesis.

* python-dev (python-devel)
* python-opengl
* python-wxtools (wxPython)
* build-essential
* git
* swig
* libopencv-dev, libcv-dev, libhighgui-dev (opencv-devel)
* python-numpy-dev
* python-opencv (opencv-python)
* libjpeg-dev (libjpeg-turbo-devel)
* ncurses-dev (ncurses-devel) (Try libncurses5-dev and libncursesw5-dev on Ubuntu if ncurses-dev doesn't work)

You can install OpenCV from source if you want. If you do, skip installing the opencv- packages. There is a tutorial for installing OpenCV from source on the wiki: Installing OpenCV


### Software Repositories

Seawolf's software is split into a number of repositories, all hosted online on github: https://github.com/ncsurobotics

You will use the git version control system to get these repositories. To clone a repository, use the git clone command:

    $ git clone <url>

Do this for each of the following URLs

* git@github.com:ncsurobotics/libseawolf.git
* git@github.com:ncsurobotics/swpycv.git
* git@github.com:ncsurobotics/svr.git
* git@github.com:ncsurobotics/seawolf.git

### Installation


##### libseawolf

Go into the libseawolf directory and run:

    $ make
    $ sudo make install
    $ make pylib
    $ sudo make pylib-install
    $ sudo ldconfig

To test:

    $ python
    >>> import seawolf

##### swpycv

Go into the swpycv directory and run:

    $ make
    $ sudo make install
    $ sudo ldconfig

##### svr

Go into the svr directory and run:

    $ make
    $ sudo make install
    $ sudo ldconfig

To test:

    $ python
    >>> import svr

##### Seawolf

Go into the seawolf directory and run:

    $ make

### Troubleshooting

For Fedora (or other systems where stropts.h is missing), create a blank file stropts.h in /usr/include

If something like “libsvr.so.0” is missing, try creating the file “seawolf.conf” containing ”/usr/local/lib” in /etc/ld.so.conf.d
