package handlers

import (
	"fmt"
	"net/http"
)

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "text/html")
	fmt.Fprintf(w, `
		<html>
		<head><title>UVT-CTF Challenge</title></head>
		<body style="font-family: monospace; background: #121212; color: #f8f8f8; padding: 20px;">
			<h1>UVT-CTF Challenge Server</h1>
			<p>Welcome to the server. Here are some available endpoints:</p>
			<ul>
				<li><a href="/about" style="color:#00ffea;">About</a></li>
				<li><a href="/list/public" style="color:#00ffea;">List /public folder as admin</a></li>
				<li><a href="/whoami" style="color:#00ffea;">Current user</a></li>
				<li><a href="/disk" style="color:#00ffea;">Disk usage</a></li>
			</ul>
			<p>Use /view/&lt;filepath&gt; to view file content as admin</p>
		</body>
		</html>
	`)
}
