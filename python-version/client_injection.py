# Huge credit to https://ancat.github.io/python/2019/01/01/python-ptrace.html
import ctypes  # To interface with native APIs to use ptrace
import sys
import os

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

