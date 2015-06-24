#
# Having "." in PYTHONPATH is really important, so that the compile doesn't pick up
#  a previously-installed simple_ra_utils
#
# Not a wonderful solution, but will have to do for now
#
PYTHONPATH:=.:$(PYTHONPATH)
SYSPREFIX=/usr/local
export PYTHONPATH


all: simple_ra_receiver.py

simple_ra_receiver.py: simple_ra_receiver.grc
	@echo Using $(PYTHONPATH) for compile...
	grcc -d . simple_ra_receiver.grc
#svn info |grep evision |sed -e 's/.*: //' >tmprev.tmp
	sed -e 's/@@REV@@/9999/' <simple_ra_receiver.py >tmprec.py
	cp tmprec.py simple_ra_receiver.py
	rm -f tmprev.tmp tmprec.py
	
install: simple_ra_receiver.py
	@echo INSTALLING in $(HOME)/bin if this is not what you want, consider sudo make sysinstall instead
	-mkdir -p $(HOME)/bin
	cp -p simple_ra $(HOME)/bin
	cp -p simple_ra_receiver.py $(HOME)/bin
	cp -p simple_ra_utils.py $(HOME)/bin
	cp -p process_simple_tpdat $(HOME)/bin
	cp -p process_simple_specdat $(HOME)/bin
	cp -p spec_animator $(HOME)/bin

sysinstall: simple_ra_receiver.py pythonpath
	install -D -o root -g root simple_ra $(SYSPREFIX)/bin/simple_ra
	install -D -o root -g root simple_ra_receiver.py $(SYSPREFIX)/bin/simple_ra_receiver.py
	install -D -o root -g root simple_ra_utils.py $(SYSPREFIX)/`./pythonpath`/simple_ra_utils.py
	install -D -o root -g root process_simple_tpdat $(SYSPREFIX)/bin/process_simple_tpdat
	install -D -o root -g root process_simple_specdat $(SYSPREFIX)/bin/process_simple_specdat
	install -D -o root -g root spec_animator $(SYSPREFIX)/bin/spec_animator
	
tarfile:
	tar czvf simple_ra.tar.gz simple_ra \
		Makefile simple_ra_receiver.grc \
		 simple_ra_utils.py \
		process_simple_tpdat process_simple_specdat spec_animator
		
clean:
	rm -f *.o *.pyc simple_ra_receiver.py differential_receiver.py simple_ra.tar.gz
