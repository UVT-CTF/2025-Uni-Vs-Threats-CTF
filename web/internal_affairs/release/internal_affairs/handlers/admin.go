package handlers

import (
	"fmt"
	"net/http"
)

// AdminHandler for debugging and admin access
func AdminHandler(w http.ResponseWriter, r *http.Request) {
	if !IsLocalhost(r) {
		http.Error(w, "Forbidden: Admin endpoint only accessible from localhost", http.StatusForbidden)
		return
	}

	CheckAuthorization(w, r)
	
	fmt.Fprintf(w, "Congratulations! You are admin ! \n")
}
