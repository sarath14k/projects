#!/bin/bash
end=$((SECONDS+5))
while [ $SECONDS -lt $end ]; do
    ps axo comm | grep -E "^nmcli$"
    sleep 0.1
done
