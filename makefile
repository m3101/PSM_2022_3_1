DSPHOST:
	if [ -d build ]; then rm -rf build; fi
	if [ ! -d bin ]; then mkdir bin; fi
	mkdir build
	gcc -c -g -o build/FilterUtils.o src/C/FilterUtils.c
	gcc -c -o build/Main.o src/C/Main.c
	gcc -o bin/dsphost build/*.o -lpulse-simple -lpulse -lm
	rm -rf build