#!/bin/sh

# Ensure build is up to date
make

if [ -d acoustics ]; then
    echo "The acoustics directory already exists. I need that as a temporary directory";
    exit 1;
fi

echo -n "Generating bundle...";

# Build directory structure
mkdir acoustics;
mkdir acoustics/coefs;
mkdir acoustics/libseawolf;

# Copy binaries
cp bin/acoustics-bfin ../ppiadc/ppiadc.ko acoustics;
cp -r ../libseawolf/* acoustics/libseawolf;

# Generate config files and scripts
cat <<EOF > acoustics/seawolf.conf
comm_server = 10.17.0.2
comm_password = 
EOF

cat <<EOF > acoustics/update
#!/bin/sh
cd /root && wget http://10.17.0.2:8080/acoustics.tar -O - | tar -xf - && cd /root/acoustics
EOF

cat <<EOF > acoustics/init
#!/bin/sh
cp /root/acoustics/libseawolf/lib/libseawolf.so* /usr/lib
modprobe gptimers
if cat /proc/modules | grep ppiadc > /dev/null 2>&1; then
    rmmod ppiadc
fi
insmod /root/acoustics/ppiadc.ko
mknod /dev/ppiadc c 157 0
EOF

chmod +x acoustics/update acoustics/init;

# Build FIR coefficient files
for f in ../fir_coef/*.fcf; do
    python ../fir_coef/convert.py < $f > acoustics/coefs/`basename $f .fcf`.cof;
done;

tar -cf acoustics.tar acoustics;
rm -rf acoustics;

echo "done.";

