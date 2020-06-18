# i3-panic

Have you ever had a need to hide what's on your screen with haste? Well, i3-panic is here to help. When invoked the script will throw all the windows on all your visible workspaces somewhere else, then when invoked again will bring them all back.

## Why can't I just switch to an empty workspace?

**Answer**: Of course you could, and that might equally as fast

## How's it work?

1. The script determines whether to hide or restore windows based on the existence of a temp file

### Hide
1. Determine all the workspaces that are visible (possible to have multiple with a multi-monitor setup)
2. Find a non-visible workspace `X`
3. Move all windows in the visible workspaces into `X` and save their id and original workspace

### Restore
1. Read window id / original workspace data from file
  1.1 Delete the data file
2. Move windows to original workspaces as appropriate