
all: paper.pdf

diagrams/%.pdf: diagrams/%.dia
	dia -e TEMPFILE -t eps $<
	ps2pdf -dEPSCrop TEMPFILE $(patsubst %.dia,%.pdf,$<)

results/%.pdf: results/%.py
	python $<

results.tex: results/constants_AMD64.pdf \
	results/constants_I386.pdf \
	results/structs_I386.pdf \
	results/structs_AMD64.pdf \
	diagrams/structs.pdf
	touch results.tex

paper.pdf: paper.tex abstract.tex \
	   introduction.tex refs.bib \
	   results.tex \
	   discussion.tex conclusions.tex
	bibtex paper
	pdflatex paper.tex
	bibtex paper
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex

clean:
	rm -f *.pdf *.aux *.log *.bbl *.spl \
	    *.blg pictures/*.png \
	    pictures/*.pdf results/*.pdf
