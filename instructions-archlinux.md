# Installation on arch linux

To install on arch linux, go to the packages directory and run

```bash
./cook.sh install all
```

This will install the AUR dependancies (namely opencv2), build all the packages and install them using PKGBUILDS.

## Updating the packages

If a change has been made to a repo, you may rebuild and install the package like this:

```bash
./cook.sh install libseawolf
```
