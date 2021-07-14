package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type Post struct {
	UserId int    `json:"userId"`
	Id     int    `json:"id"`
	Title  string `json:"title"`
	Body   string `json:"body"`
}

func main() {

	endpoint := "https://jsonplaceholder.typicode.com/posts"
	test_api(endpoint)

	posts := test_api(endpoint)
	for _, post := range posts {
		fmt.Println(post)
		break
	}

}

func test_api(endpoint string) []Post {

	var posts []Post

	resp, err := http.Get(endpoint)
	defer resp.Body.Close()
	if err != nil {
		panic(err)
	} else {

		fmt.Printf("%T\n", resp)

		data, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			panic(err)
		} else {
			fmt.Println("Works with ioutil")
		}
		e := json.Unmarshal(data, &posts)
		if e != nil {
			fmt.Println(e)
			fmt.Println(posts)
		} else {
			fmt.Println("really made it work")
		}

	}

	return posts

}
