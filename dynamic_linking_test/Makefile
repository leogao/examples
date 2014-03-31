ALL:
	gcc -fPIC -shared -o bar.so bar.c 
	gcc -fPIC -shared -o foo.so foo.c ./bar.so 
	gcc -o app t.c ./foo.so ./bar.so -ldl

clean:
	rm app foo.so bar.so
