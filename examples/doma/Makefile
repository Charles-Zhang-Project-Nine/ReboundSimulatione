export OPENGL=0
include ../../src/Makefile.defs

all: librebound
	@echo ""
	@echo "Compiling problem file ..."
	$(CC) -I../../src/ -Wl,-rpath,./ $(OPT) $(PREDEF) problem.c -L. -lrebound $(LIB) -o Doma
	@echo ""
	@echo "Problem compiled successfully."
	
	@echo "Execute..."
	./Doma > output.txt

librebound: 
	@echo "Compiling shared library librebound.so ..."
	$(MAKE) -C ../../src/
	@-rm -f librebound.so
	@ln -s ../../src/librebound.so .

clean:
	@echo "Cleaning up shared library librebound.so ..."
	@-rm -f librebound.so
	$(MAKE) -C ../../src/ clean
	@echo "Cleaning up local directory ..."
	@-rm -vf rebound
