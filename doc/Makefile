
SRCS= $(vpath %.tex srC)

all: seawolf.pdf

seawolf.pdf: work/seawolf.pdf
	cp work/seawolf.pdf seawolf.pdf

work/seawolf.pdf: work $(SRCS)
	latex -output-format=pdf -output-directory=work/ src/seawolf.tex

work:
	mkdir work

clean:
	@for _f in seawolf.pdf work/*; do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean
