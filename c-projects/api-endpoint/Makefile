CC = gcc
CFLAGS= -Iinclude -I/usr/local/include/libbson-1.0 -I/usr/local/include/libmongoc-1.0 -I/usr/local/include -lmicrohttpd -ljansson -lmongoc-1.0 -lbson-1.0 
ODIR=src

_OBJ =data.o main.o server.o
OBJ =$(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.c 
	$(CC) -c -o $@ $< $(CFLAGS)

service: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
clean: 
	rm $(ODIR)/*.o

 
