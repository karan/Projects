package main

import (
	"bytes"
	"fmt"
	"log"
	"net"
)

const (
	Port = "localhost:6009"
)

func ConnectServer() {
	conn, err := net.Dial("tcp", Port)
	if err != nil {
		log.Println(err)
	}
	defer conn.Close()
	fmt.Printf("Connected to %s\n", conn.RemoteAddr().String())
	var n int64
	buffer := bytes.NewBuffer(nil)
	n, err = buffer.ReadFrom(conn)
	if err != nil {
		log.Println(err)
	}
	fmt.Printf("Read %d bytes\n", n)
	fmt.Print(buffer.String())
}

func main() {
	ConnectServer()

}
