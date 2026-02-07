# SSH Agent
if test -z "$SSH_ENV"
    set -xg SSH_ENV $HOME/.ssh/environment
end

if not __ssh_agent_is_started
    __ssh_agent_start
end

alias vim='nvim'
set -x GPG_TTY (tty)

# Add pipx to PATH
fish_add_path /home/henrique/.local/bin

# Starship prompt
starship init fish | source
