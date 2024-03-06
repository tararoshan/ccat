// CLIENT MAIN.GO
package main

import (
	"bufio"
	"fmt"
	"net"
)

func main() {
	// Dial is used to connect to a server
	conn, err := net.Dial("tcp", "golang.org:80")
	if err != nil {
		// handle error
	}
	fmt.Fprintf(conn, "GET / HTTP/1.0\r\n\r\n")
	status, err := bufio.NewReader(conn).ReadString('\n')
}
