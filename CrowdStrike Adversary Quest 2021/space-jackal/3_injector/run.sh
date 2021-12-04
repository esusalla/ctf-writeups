#!/bin/sh

IMAGE=art_ctf_injector_local.qcow2
SNAPSHOT=compromised

stty intr ^]

echo "Restoring snapshot $SNAPSHOT ($IMAGE)"
echo "Press Return..."

qemu-system-x86_64 -enable-kvm -machine pc-i440fx-4.2 -nodefaults -nographic \
	-chardev stdio,id=c1 -monitor tcp:127.0.0.1:55555,server,nowait \
	--device isa-serial,chardev=c1 -m size=512M,maxmem=512M \
	-netdev user,id=n1,net=192.168.76.0/24,dhcpstart=192.168.76.9,hostfwd=tcp::3322-:3322,hostfwd=tcp::4321-:4321 \
	-device virtio-net,netdev=n1 -object rng-random,filename=/dev/urandom,id=rng0 \
	-device virtio-rng-pci,rng=rng0 -boot order=c -hda $IMAGE -loadvm $SNAPSHOT

stty intr ^C
