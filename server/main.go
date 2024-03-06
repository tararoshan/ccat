// SERVER MAIN.GO
package main

import (
	"net"
)

func main() {
	// Listen is used to create a server
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		// handle error
	}
	for {
		conn, err := ln.Accept()
		if err != nil {
			// handle error
		}
		go handleConnection(conn)
	}
}

func handleConnection(net.Conn conn) {

}