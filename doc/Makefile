
all: seawolf.pdf

# Run twice (second time generates indexes and whatnot)
seawolf.pdf:
	latex -output-format=pdf -output-directory=work/ src/seawolf.tex
	latex -output-format=pdf -output-directory=work/ src/seawolf.tex
	mv work/seawolf.pdf .

work:
	mkdir -p work

clean:
	@for _f in seawolf.pdf work/*; do \
	  if [ -f $$_f ]; then \
	    echo rm $$_f; \
	    rm $$_f; \
	  fi; \
	done;

.PHONY: all clean work seawolf.pdf
