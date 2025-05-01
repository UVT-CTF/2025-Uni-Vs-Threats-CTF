package main

import (
	"fmt"
	"log"
	"net/http"

	"ctfserver/handlers"
)

func main() {
	http.HandleFunc("/admin", handlers.AdminHandler)
	http.HandleFunc("/", handlers.HomeHandler)
	http.HandleFunc("/about", handlers.AboutHandler)
	http.HandleFunc("/request/", handlers.RequestHandler)
	http.HandleFunc("/whoami", handlers.UserHandler)
	http.HandleFunc("/disk", handlers.DiskHandler)
	http.HandleFunc("/list/", handlers.ListHandler)
	http.HandleFunc("/view/", handlers.ViewHandler)
	http.HandleFunc("/link", handlers.LinkHandler)

	fmt.Println("Starting CTF challenge server on :40048...")
	log.Fatal(http.ListenAndServe(":40048", nil))
}
