# Defined in - @ line 2
function fish_prompt
	test $SSH_TTY
    and printf (set_color red)(whoami)(set_color white)'@'(set_color yellow)(hostname)' '

    test $USER = 'root'
    and echo (set_color red)"#"

    # Main
    echo -n (set_color cyan)(prompt_pwd)(set_color white)
    echo -n (__fish_git_prompt) (set_color 6272a4)'❯'(set_color bd93f9)'❯'(set_color ff79c6)'❯ '
end
