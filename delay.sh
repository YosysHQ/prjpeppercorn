#!/bin/bash

set -e
ARCHIVE="cc-toolchain-linux.tar.gz"

rm -rf delay
mkdir -p delay

wget -O "$ARCHIVE" "https://colognechip.com/downloads/cc-toolchain-linux.tar.gz"

tar --extract \
    --file="$ARCHIVE" \
    --wildcards \
    --strip-components=3 \
    --directory=delay \
    'cc-toolchain-linux/bin/p_r/*.dly'
