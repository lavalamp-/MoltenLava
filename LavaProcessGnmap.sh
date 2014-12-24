#!/bin/bash

file="$1"

cat "$file" | grep 80/open/tcp | awk '{print $2}' | sort | uniq > http_hosts
cat "$file" | grep 443/open/tcp | awk '{print $2}' | sort | uniq > https_hosts
cat "$file" | grep 21/open/tcp | awk '{print $2}' | sort | uniq > ftp_hosts
cat "$file" | grep 22/open/tcp | awk '{print $2}' | sort | uniq > ssh_hosts
cat "$file" | grep 23/open/tcp | awk '{print $2}' | sort | uniq > telnet_hosts
cat "$file" | grep 8080/open/tcp | awk '{print $2}' | sort | uniq > http_8080_hosts
cat "$file" | grep 8443/open/tcp | awk '{print $2}' | sort | uniq > https_8443_hosts
cat "$file" | grep 3389/open/tcp | awk '{print $2}' | sort | uniq > rdp_hosts
cat "$file" | grep 445/open/tcp | awk '{print $2}' | sort | uniq > smb_hosts
cat "$file" | grep 135/open/tcp | awk '{print $2}' | sort | uniq > dcom_hosts
cat "$file" | grep 139/open/tcp | awk '{print $2}' | sort | uniq > rpc_hosts
cat "$file" | grep 3306/open/tcp | awk '{print $2}' | sort | uniq > mysql_hosts
cat "$file" | grep 512/open/tcp | awk '{print $2}' | sort | uniq > rexec_hosts
cat "$file" | grep 1433/open/tcp | awk '{print $2}' | sort | uniq > mssql_hosts
cat "$file" | grep 1521/open/tcp | awk '{print $2}' | sort | uniq > oracle_hosts
cat "$file" | grep 2049/open/tcp | awk '{print $2}' | sort | uniq > nfs_hosts
cat "$file" | grep 4899/open/tcp | awk '{print $2}' | sort | uniq > radmin_hosts
cat "$file" | grep 5631/open/tcp | awk '{print $2}' | sort | uniq > pcanywhere_hosts
cat "$file" | grep 6000/open/tcp | awk '{print $2}' | sort | uniq > x11_hosts
cat "$file" | grep 5800/open/tcp | awk '{print $2}' | sort | uniq > vnc_5800_hosts
cat "$file" | grep 5900/open/tcp | awk '{print $2}' | sort | uniq > vnc_5900_hosts
cat "$file" | grep 5060/open/tcp | awk '{print $2}' | sort | uniq > SIP_hosts
cat "$file" | grep 5061/open/tcp | awk '{print $2}' | sort | uniq > SIPTLS_hosts
cat "$file" | grep 1720/open/tcp | awk '{print $2}' | sort | uniq > h323_hosts
cat http_hosts | sed 's/^/http:\/\//' > eyewitness_endpoints
cat https_hosts | sed 's/^/https:\/\//' >> eyewitness_endpoints
cat http_8080_hosts | sed 's/^/http:\/\//' | sed 's/$/:8080/' >> eyewitness_endpoints
cat https_8443_hosts | sed 's/^/https:\/\//' | sed 's/$/:8443/' >> eyewitness_endpoints

rm -f $(find . -empty)