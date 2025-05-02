package handlers

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"strings"
)

// RequestHandler handles the /request/* route
func RequestHandler(w http.ResponseWriter, r *http.Request) {
	// Extract the raw request URI and strip off any query string
	raw := r.RequestURI
	if i := strings.Index(raw, "?"); i != -1 {
		raw = raw[:i]
	}

	const prefix = "/request/"
	// Check that there is something after "/request/"
	if len(raw) <= len(prefix) {
		http.Error(w, "Missing URL parameter", http.StatusBadRequest)
		return
	}

	// Raw target (still percent-encoded)
	rawTarget := raw[len(prefix):]

	// Allow exactly one level of percent-encoding, reject double-encoding
	decodedTarget, err := url.PathUnescape(rawTarget)
	if err != nil {
		http.Error(w, fmt.Sprintf("Invalid URL encoding: %v", err), http.StatusBadRequest)
		return
	}
	if strings.Contains(decodedTarget, "%") {
		http.Error(w, "Double-encoded sequences are not allowed", http.StatusBadRequest)
		return
	}

	// Build the actual target URL
	var targetURL string
	if decodedTarget == "whoami" || decodedTarget == "disk" {
		targetURL = "http://127.0.0.1:40048/" + decodedTarget
	} else {
		targetURL = decodedTarget
	}

	// Determine method (default GET)
	method := r.URL.Query().Get("method")
	if method == "" {
		method = "GET"
	}

	client := &http.Client{}
	log.Printf("Forwarding request to %s with method %s", targetURL, method)
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
