#!/bin/bash

SESSION="bootdev_parallel"

# Check if the session already exists to avoid errors
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
  # 1. Start a new session (Top-Left corner)
  tmux new-session -d -s $SESSION -n "Modules"
  
  # 2. Split horizontally (Creates Top-Right)
  tmux split-window -h
  
  # 3. Split the left side vertically (Creates Bottom-Left)
  tmux select-pane -t 0
  tmux split-window -v
  
  # 4. Split the right side vertically (Creates Bottom-Right)
  tmux select-pane -t 2
  tmux split-window -v

  # Optional: Send commands to specific panes
  # Pane 0: Top-Left, Pane 1: Bottom-Left, Pane 2: Top-Right, Pane 3: Bottom-Right
  tmux send-keys -t 0 "echo 'Module 7 Focus'" C-m
  tmux send-keys -t 1 "echo 'Module 8 Focus'" C-m
  tmux send-keys -t 2 "echo 'Module 9 Focus'" C-m
  tmux send-keys -t 3 "echo 'Module 10 Focus'" C-m

  # Select the top-left pane before attaching
  tmux select-pane -t 0
fi

# Attach to the session
tmux attach-session -t $SESSION
