SRC_DIR := src
HEAD_DIR := include
default:
	gcc -o daemon $(SRC_DIR)/main.c $(SRC_DIR)/core.c $(SRC_DIR)/utils.c -I $(HEAD_DIR) -lmicrohttpd -ljansson
