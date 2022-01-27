#!/bin/sh

# recursively removes all .pyc files and __pycache__ directories in the current
# directory

find . | \
  grep -E "(__pycache__|\.pyc$)" | \
  xargs rm -rf

# or, for copy-pasting:
# find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
