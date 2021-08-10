package main


import (
	"fmt"
      	"github.com/go-cmd/cmd"
	"os"
	"strings"
)

func main() {


	arg := strings.Join(os.Args[1:]," ")
	runCommand(arg)


}

func runCommand(comm string) {
	lsCmd := cmd.NewCmd(comm)
	status := <-lsCmd.Start()
	for !status.Complete {
		for _, line := range status.Stdout {
			fmt.Println(line)
	}
	}

}
