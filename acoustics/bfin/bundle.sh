#!/bin/sh

if [ -d acoustics ]; then
    echo "The acoustics directory already exists. I need that as a temporary directory";
else
    echo -n "Generating bundle...";

    mkdir acoustics;
    mkdir acoustics/coefs;

    cp bin/acoustics-bfin ../ppiadc/ppiadc.ko ../../libseawolf/libseawolf-bfin.so acoustics/;

    cat <<EOF > acoustics/seawolf.conf
Comm_server = 10.17.0.2
Comm_password = 
EOF

    cat <<EOF > acoustics/update
#!/bin/sh
cd /root && wget http://10.17.0.2:8080/acoustics.tar -O - | tar -xf - && cd /root/acoustics
EOF

    cat <<EOF > acoustics/init
#!/bin/sh
cp /root/acoustics/libseawolf-bfin.so /lib
modprobe gptimers
if cat /proc/modules | grep ppiadc > /dev/null 2>&1; then
  rmmod ppiadc
fi
insmod /root/acoustics/ppiadc.ko
mknod /dev/ppiadc c 157 0
EOF

    chmod +x acoustics/update acoustics/init;
    
    for f in ../fir_coef/*.fcf; do
	python ../fir_coef/convert.py < $f > acoustics/coefs/`basename $f .fcf`.cof;
    done;

    tar -cf acoustics.tar acoustics;
    rm -rf acoustics;

    echo "done.";
fi;
