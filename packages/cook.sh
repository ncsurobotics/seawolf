#!/bin/bash
# Inspired by redox' cook.sh
OP="$1"
PKG="$2"
TOPLEVEL="$PWD"
touch .cookvars
source .cookvars
touch .log
log() {
    echo "$@" >> "${TOPLEVEL}/.log"
}

if [ "$SW_PACKAGES_DOWNLOADED" ]
then
    source swpackages/.cooklist.sh
fi

# Since the next section may fail, we'll want try/catch
# Exept, since there are no exeptions in bash we'll need to use a trap. lol
ERRHANDLER_DO="fail"

errhandler() {
    case "$ERRHANDLER_DO" in
	"ignore")
	    true
	    ;;
	*)
	    echo "Cook failed." >&2
	    exit 1
	    ;;
    esac
}

trap "errhandler" ERR

# Blue and unblue
if test -t 1 # Tests if this is a terminal
then
    # test to make sure tput doesn't crash the script
    ERRHANDLER_DO="ignore"
    tput colors &>/dev/null
    tput_sucess_p=$(echo $?)
    ERRHANDLER_DO="fail"
    if [ "$tput_sucess_p" = "0" ]
    then
	ncolors=$(tput colors)
	if [ ! "x$ncolors" = "x" ] && [ "$ncolors" -ge "8" ] # Ensures that there are at least 8 colors
	then
	    BLU="$(tput setaf 4)$(tput bold)"
	    UBL="$(tput sgr0)"
	fi
    fi
fi

# Colored echo
cecho() {
    echo -e "${BLU}$1${UBL}"
}

# Allow subshells to give colored output
export -f cecho

# Loudly remove file
lrm() {
    file="$1"
    if [ -d "$file" ]
    then
	echo "Removing directory $file"
	rm -rf "$file"
    fi
    if [ -f "$file" ]
    then
	echo "Removing file $file"
	rm "$file"
    fi
}

# Quiet pushd & popd
qpushd() {
    pushd "$@" 2>&1 > /dev/null
}

qpopd() {
    popd "$@" 2>&1 > /dev/null
}

export -f qpushd
export -f qpopd

# The wonders of an untyped language
nullcheck_call() {
    # If rst is not null, call fst on rst
    fst="$1"
    rst="${@:2}"
    if [ "x$rst" = "x" ]
    then
	echo "Error: $1 called with no arguments"
	exit 1
    else
	"$fst" "${@:2}"
    fi
}

ask() {
    read -p "${@} [Y/n] " choice
    case "$choice" in
	y|Y)
	    echo "1"
	    ;;
	n|N)
	    echo "0"
	    ;;
	*)
	    echo "1"
	    ;;
    esac
}

usage() {
    echo "cook.sh <option> <package>" >&2
    echo "        download" >&2
    echo "        redownload" >&2
    echo "        deps" >&2
    echo "        redeps" >&2
    echo "        build" >&2
    echo "        rebuild" >&2
    echo "        clean" >&2
    echo "        install" >&2
}

if [ "x$OP" = "x" ] && [ "x$PKG" = "x" ]
then
    usage
    exit 1
fi

# Necessary before any other task
redownload() {
    if [ "$SW_PACKAGES_DOWNLOADED" = "1" ]
    then
	qpushd swpackages
	git stash
	git pull
	cecho "Seawolf package buildscripts updated"
	qpopd
    else
	git clone https://github.com/jsalzbergedu/swpackages.git
	echo "SW_PACKAGES_DOWNLOADED=1" >> .cookvars
	cecho "Seawolf package buildscripts downloaded"
    fi
}

download() {
    if [ "$SW_PACKAGES_DOWNLOADED" = "1" ]
    then
	cecho "Seawolf package buildscripts already downloaded"
    else
	redownload
    fi
    source swpackages/.cooklist.sh
}


# Archlinux
arch_deps() {
    if [ -d opencv2]
    then
	rm -r opencv2
    fi
    git clone https://aur.archlinux.org/opencv2.git
    qpushd opencv2
    makepkg -si
    qpopd
    echo "DEPS_INSTALLED=1" >> .cookvars
    cecho "Installed dependancies"
}

arch_build_onepkg() {
    pkgdir="$1"
    cecho "Building package $pkgdir"
    qpushd "$pkgdir"
    makepkg
    qpopd
    cecho "Built $pkgdir"
}

arch_build() {
    qpushd swpackages
    qpushd arch
    arch_build_onepkg "$1"
    qpopd
    qpopd
}

arch_clean_onepkg() {
    pkgdir="$1"
    cecho "Cleaning package $pkgdir"
    qpushd "$pkgdir"
    for file in *
    do
	if [ ! "$file" = "PKGBUILD" ]
	then
	    lrm "$file"
	fi
    done
    qpopd
}

arch_clean() {
    qpushd swpackages
    qpushd arch
    if [ "$1" = "all" ]
    then
	for pkg in *
	do
	    arch_clean_onepkg "$pkg"
	done
    else
	arch_clean_onepkg "$1"
    fi
    qpopd
    qpopd
}

arch_install_onepkg() {
    pkgdir="$1"
    cecho "Installing package $pkgdir"
    qpushd "$pkgdir"
    makepkg -si
    qpopd
}

arch_install() {
    qpushd swpackages
    qpushd arch
    arch_install_onepkg "$1"
    qpopd
    qpopd
}

# Ubuntu
ubu_deps() {
    # build dependencies -- libseawolf
    sudo apt-get install git cmake swig ninja-build python-dev python-all fakeroot build-essential
    # build dependencies -- the rest
    sudo apt-get install python-dev python-opengl python-wxtools libopencv-dev libopencv-dev python-numpy-dev python-opencv libjpeg-dev ncurses-dev
    echo "DEPS_INSTALLED=1" >> .cookvars 
    cecho "Installed dependancies"
}

ubu_install_onepkg () {
    pkgdir="$1"
    cecho "Installing package $packagedir"
    qpushd "$pkgdir"
    ./install.sh
    qpopd
}

ubu_install() {
    qpushd swpackages
    qpushd ubu
    ubu_install_onepkg "$pkg"
    qpopd
    qpopd
}

ubu_build_onepkg() {
    pkgdir="$1"
    cecho "Building package $pkgdir"
    qpushd "$pkgdir"
    ./fetchbuild.sh
    qpopd
}

ubu_build() {
    qpushd swpackages
    qpushd ubu
    ubu_build_onepkg "$pkg"
    qpopd
    qpopd
}

# If first matches any of the rest, return true
anyeq() {
    fst="$1"
    p=1
    for item in "${@:2}"
    do
	if [ "$fst" = "$item" ]
	then
	    p=0
	fi
    done
    return $p
}

export -f anyeq

ubu_clean_onepkg() {
    pkgdir="$1"
    cecho "Cleaning package $pkgdir"
    qpushd "$pkgdir"
    for file in *
    do
	if ! anyeq "$file" "fetchbuild.sh" "DEBIAN" "install.sh"
	then
	    lrm "$file"
	fi
	if [ -d DEBIAN ]
	then
	    qpushd DEBIAN
	    for file in *
	    do
		if ! anyeq "$file" "control"
		then
		    lrm "$file"
		fi
	    done
	    qpopd
	fi
    done
    qpopd
}

ubu_clean() {
    qpushd swpackages
    qpushd ubu
    if [ "$1" = "all" ]
    then
	for pkg in *
	do
	    ubu_clean_onepkg "$pkg"
	done
    else
	ubu_clean_onepkg "$1"
    fi
    qpopd
    qpopd
}

# Placeholders for the real functions
DEPS_FN=""
BUILD_FN=""
CLEAN_FN=""
INSTALL_FN=""

redeps() {
    $DEPS_FN "$@"
}

deps() {
    if [ $DEPS_INSTALLED ]
    then
	cecho "Dependancies already installed"
    else
	redeps "$@"
    fi
}

build() {
    download
    $BUILD_FN "$@"
}

clean_unsafe() {
    download
    $CLEAN_FN "$@"
}

clean() {
    nullcheck_call clean_unsafe "$@"
}


rebuild() {
    clean "$@"
    build "$@"
}

install() {
    deps "$@"
    clean "$@"
    build "$@"
    $INSTALL_FN "$@"
}

# Set the correct functions depending on os
source /etc/os-release 
OS="$ID"
case "$OS" in
    arch)
	DEPS_FN="arch_deps"
	BUILD_FN="arch_build"
	CLEAN_FN="arch_clean"
	INSTALL_FN="arch_install"
	;;
    ubuntu)
	DEPS_FN="ubu_deps"
	BUILD_FN="ubu_build"
	CLEAN_FN="ubu_clean"
	INSTALL_FN="ubu_install"
	;;
    *)
	cecho "OS or distro either unsupported or without packages"
	;;
esac

all_to_last() {
    if [ "$1" = "all" ]
    then
	echo "${COOKLIST[-1]}"
    else
	echo "$1"
    fi
}

in_cooklist() {
    in_list_p=0
    for pkg in "${COOKLIST[@]}"
    do
	if [ "$1" = "$pkg" ]
	then
	    in_list_p=1
	fi
    done

    if [ "$1" = "all" ]
    then
	in_list_p=1
    fi

    if [ "$in_list_p" = "0" ]
    then
	echo "Package $1 does not exist."
	exit 1
    else
	echo "$1"
    fi
}

make_cookable() {
    echo $(in_cooklist $(all_to_last "$1"))
}

cooklist_transform() {
    op="$1"
    requested_package="$2"
    for pkg in "${COOKLIST[@]}"
    do
	if [ "$requested_package" = "$pkg" ]
	then
	    "$op" "$requested_package"
	    break
	else
	    user_allows_install=$(ask "To ${op} ${requested_package}, cook must first install ${pkg}. Is that ok?")
	    if [ "$user_allows_install" = "1" ]
	    then
		install "$pkg"
	    else
		cecho "Without installing ${pkg}, cook cannot ${op} ${requested_package}. Exiting."
		exit 1
	    fi
	fi
    done
}

cook() {
    qpushd "$TOPLEVEL"
    OP="$1"
    PKG="$2"
    case "$OP" in
	download)
	    download
	    ;;
	redownload)
	    redownload
	    ;;
	deps)
	    deps
	    ;;
	redeps)
	    redeps
	    ;;
	build)
	    cooklist_transform "$OP" "$(make_cookable $PKG)"
	    ;;
	rebuild)
	    cooklist_transform "$OP" "$(make_cookable $PKG)"
	    ;;
	clean)
	    clean "$(in_cooklist $PKG)"
	    ;;
	install)
	    cooklist_transform "$OP" "$(make_cookable $PKG)"
	    ;;
	--help)
	    usage
	    ;;
	-h)
	    usage
	    ;;
	*)
	    cecho "${OP}: Command not recognized" >&2
	    usage
	    ;;
    esac
    qpopd
}

cook "$@"
