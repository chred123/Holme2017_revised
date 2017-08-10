#!/bin/sh
filename=$1
latex $filename
bibtex $filename
latex $filename
latex $filename
dvipdf $filename.dvi
open $filename.pdf
