package handlers

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)



func UserHandler(w http.ResponseWriter, r *http.Request) {

	out, err := exec.Command("whoami").Output()
	if err != nil {
		http.Error(w, fmt.Sprintf("Failed to get user : %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/plain")
	w.Write(out)
}

func ReadLinkPath(path string) (string, error) {
	target, err := os.Readlink(path)
	if err != nil {
		return "", fmt.Errorf("failed to readlink %s: %w", path, err)
	}
	return target, nil
}

// Sometimes i need the full path of the file for debugging
func LinkHandler(w http.ResponseWriter, r *http.Request) {
	if !IsLocalhost(r) {
		http.Error(w, "Forbidden", http.StatusForbidden)
		return
	}
	if !CheckAuthorization(w, r) {
		return
	}

	userPath := r.URL.Query().Get("path")
	if userPath == "" {
		http.Error(w, "Missing path parameter", http.StatusBadRequest)
		return
	}

	target, err := ReadLinkPath(userPath)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error: %v", err), http.StatusInternalServerError)
		return
	}

	fmt.Fprintf(w, "Resolved path: %s\n", target)
}


func DiskHandler(w http.ResponseWriter, r *http.Request) {

	out, err := exec.Command("df", "-h").Output()
	if err != nil {
		http.Error(w, fmt.Sprintf("Failed to get disk usage: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/plain")
	w.Write(out)
}


func ListHandler(w http.ResponseWriter, r *http.Request) {

	if !IsLocalhost(r) {
		http.Error(w, "Forbidden: /list endpoint accessible only from localhost", http.StatusForbidden)
		return
	}
	if !CheckAuthorization(w, r) {
		return
	}
	path := strings.TrimPrefix(r.URL.Path, "/list/")
	if path == "" {
		http.Error(w, "No folder specified", http.StatusBadRequest)
		return
	}

	cleanPath := filepath.Clean(path)

	files, err := os.ReadDir(cleanPath)
	if err != nil {
		http.Error(w, fmt.Sprintf("Cannot list directory: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/plain")
	for _, f := range files {
		info := "file"
		if f.IsDir() {
			info = "dir"
		}
		fmt.Fprintf(w, "%s - %s\n", f.Name(), info)
	}
}


func ViewHandler(w http.ResponseWriter, r *http.Request) {
	if !IsLocalhost(r) {
		http.Error(w, "Forbidden: /view endpoint accessible only from localhost", http.StatusForbidden)
		return
	}

	if !CheckAuthorization(w, r) {
		return
	}
	path := strings.TrimPrefix(r.URL.Path, "/view/")

	log.Println("Requested file:", path)

	if path == "" {
		http.Error(w, "No file specified", http.StatusBadRequest)
		return
	}

	cleanPath := "./public/" + filepath.Clean(path)


	if strings.Contains(strings.ToLower(cleanPath), "self") {
		http.Error(w, "We don't leak the folder", http.StatusBadRequest)
		return
	}


	fileInfo, err := os.Stat(cleanPath)
	if err != nil {
		http.Error(w, fmt.Sprintf("Cannot stat file: %v", path), http.StatusNotFound)
		return
	}

	if fileInfo.IsDir() {
		http.Error(w, "Cannot view a directory", http.StatusBadRequest)
		return
	}

	content, err := os.ReadFile(cleanPath)
	if err != nil {
		http.Error(w, fmt.Sprintf("Cannot read file: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/plain")
	w.Write(content)
}
