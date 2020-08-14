function prune_merged_branches
git branch --merged | egrep -v '^\*' | xargs git branch -d
end
