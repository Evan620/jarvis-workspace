#!/bin/bash
# Vercel deployment wrapper with SSL bypass
export NODE_TLS_REJECT_UNAUTHORIZED=0
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt

# If first argument is a directory, cd into it and shift arguments
if [ -d "$1" ]; then
    cd "$1" || exit 1
    shift
fi

# Run vercel with all remaining arguments
vercel "$@"
