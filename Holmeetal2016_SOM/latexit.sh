#!/bin/sh
filename=$1
pdflatex $filename
bibtex $filename
pdflatex $filename
pdflatex $filename
#dvipdf $filename.dvi
open $filename.pdf
