CC = gcc
CFLAGS= -Iinclude -I/usr/local/include/ -Iinclude/ -L/usr/local/lib -lhiredis -ljansson
ODIR=src

_OBJ =main.o aux.o 
OBJ =$(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.c 
	$(CC) -c -o $@ $< $(CFLAGS)

redis-cli: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)
clean: 
	rm $(ODIR)/*.o
install: 
	cp redis-cli /usr/local/bin
