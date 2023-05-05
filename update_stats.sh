#!/bin/bash

stat()
{
    echo "run $1"
    eval $1 > /tmp/$2.$$ && mv -f /tmp/$2.$$ $2
}

stat "popf.py -check        | tail -20 | head -19" popf-check.i
stat "popf.py -efficiency 7 | tail -21 | head -20" popf-efficiency.i
