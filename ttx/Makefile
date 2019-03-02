all:

.PHONY: all clean

TTX = ttx

%.ttx: ../download/%.otf
	$(TTX) -d . -s $<

clean:
	$(RM) *~
