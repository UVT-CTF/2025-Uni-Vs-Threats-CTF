package handlers

import (
	"fmt"
	"io"
	"net/http"
)

// RequestHandler handles the /request/* route
func RequestHandler(w http.ResponseWriter, r *http.Request) {
	if len(r.URL.Path) <= len("/request/") {
		http.Error(w, "Missing URL parameter", http.StatusBadRequest)
		return
	}

	targetPath := r.URL.Path[len("/request/"):]

	var targetURL string

	// Special handling for internal services
	if targetPath == "whoami" || targetPath == "disk" {
		targetURL = "http://127.0.0.1:40048/" + targetPath
	} else {
		targetURL = targetPath

	}

	method := r.URL.Query().Get("method")
	if method == "" {
		method = "GET"
	}

	client := &http.Client{}
	req, err := http.NewRequest(method, targetURL, nil)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error creating request: %v", err), http.StatusInternalServerError)
		return
	}

	// Forward only Cookie and Authorization headers
	for name, values := range r.Header {
		if name == "Cookie" || name == "Authorization" {
			for _, value := range values {
				req.Header.Add(name, value)
			}
		}
	}

	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error making request: %v", err), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error reading response: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", resp.Header.Get("Content-Type"))
	w.WriteHeader(resp.StatusCode)
	w.Write(body)
}
