# Start fresh or target the current session
# 1. Split the screen into two equal vertical halves (TL/BL vs TR/BR)
tmux split-window -h

# 2. Select the left half and split it horizontally (Creating TL and BL)
tmux select-pane -t 0
tmux split-window -v

# 3. Select the right half and split it horizontally (Creating TR and BR)
tmux select-pane -t 2
tmux split-window -v
