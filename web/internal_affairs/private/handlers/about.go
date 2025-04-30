package handlers

import (
	"fmt"
	"net/http"
)

func AboutHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	fmt.Fprintf(w, `
		<html>
		<head><title>About</title></head>
		<body style="font-family: monospace; background: #121212; color: #f8f8f8; padding: 20px;">
			<h1>About This CTF Server</h1>
			<p>This is a remote management site made by UVT-CTF for UVT-CTF. Have fun!</p>
			<a href="/" style="color:#00ffea;">Back to Home</a>
		</body>
		</html>
	`)
}
