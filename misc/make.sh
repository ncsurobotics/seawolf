
# Functions to assist in make like shell scripts

runcmd () {
    echo $@;
    $@;
}

isOutDated () {
    # target file : requirements
    if [ ! -f $1 ]; then
        return 0;
    fi
    if [ "`ls -t1 $@ | head -1`" != "$1" ]; then
        return 0;
    fi

    return 1;
}

rmNoFail () {
    for f in $@; do
        if [ -f $f ]; then
            runcmd rm $f
        fi
    done
}
