# Environment variables for Fish shell

# Go workspace path
set -gx GOPATH /home/henrique/projects/go_workspace

# npm global packages location
set -gx npm_config_prefix /home/henrique/.node_modules

# Add npm bin to PATH
fish_add_path /home/henrique/.node_modules/bin
