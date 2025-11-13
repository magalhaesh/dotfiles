function nixos-switch -d "Apply NixOS configuration with nom progress tracking"
    sudo cp ~/projects/nixOS-personal-docs/configuration.nix /etc/nixos/
    and sudo nixos-rebuild switch 2>&1 | nom
end
