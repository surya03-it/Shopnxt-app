#!/bin/bash
curl -sf http://localhost:5000/health && echo "OK" || exit 1
