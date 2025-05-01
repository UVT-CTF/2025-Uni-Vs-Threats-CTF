package handlers

import (
	"net/http"
	"strings"
)

// IsLocalhost checks if the request comes from localhost
func IsLocalhost(r *http.Request) bool {
	host := r.RemoteAddr
	return strings.HasPrefix(host, "127.0.0.1") || strings.HasPrefix(host, "[::1]") || strings.HasPrefix(host, "localhost:")
}

// CheckAuthorization validates the Authorization header
func CheckAuthorization(w http.ResponseWriter, r *http.Request) bool {
	authHeader := r.Header.Get("Authorization")
	if authHeader != "Bearer YWRtaW46YWRtaW4=" {
		http.Error(w, "Unauthorized: Invalid or missing authorization", http.StatusUnauthorized)
		return false
	}
	return true
}