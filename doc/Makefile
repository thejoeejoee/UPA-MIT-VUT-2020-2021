FILE=xkolar71_xhalas10_xhertl04.pdf

all: $(FILE)

$(FILE): doc.pdf
	mv doc.pdf $(FILE)

doc.pdf: doc.tex
	pdflatex doc.tex && pdflatex doc.tex && pdflatex doc.tex
