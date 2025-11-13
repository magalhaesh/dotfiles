function nixos-test -d "Test NixOS configuration with nom progress tracking"
    sudo cp ~/projects/nixOS-personal-docs/configuration.nix /etc/nixos/
    and sudo nixos-rebuild test 2>&1 | nom
end
