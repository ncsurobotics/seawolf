
all: seawolf.pdf

# Run twice (second time generates indexes and whatnot)
seawolf.pdf:
	mkdir -p work
	latex -output-format=pdf -output-directory=work/ src/seawolf.tex
	latex -output-format=pdf -output-directory=work/ src/seawolf.tex
	mv work/seawolf.pdf .

clean:
	@for _f in seawolf.pdf work/*; do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean seawolf.pdf
