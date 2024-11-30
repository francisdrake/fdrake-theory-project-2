'''
INPUTS:
  The inputs to your program should include:
  The name of the file describing the machine
  The input string to run
  A ”termination” flag that will stop execution under some circumstance such as if the
  depth of the configuration tree exceeds a limit, or the total number of transitions
  simulated exceeds some number.
  You may have some other flags which activate some debugging or expanded tracing
  option that help you follow what your code is doing.
  You may want to design it so that you can enter multiple strings one after another.
'''

'''
OUPUTS:
    All runs should first echo the name of the machine (from line 1), the initial string, the
depth of the tree of configurations, and the total number of transitions simulated. If the
machine is deterministic the latter two numbers should be the same.
If the simulation halts because of reaching an accept configuration, print out the following:
• ”String accepted in ” and then the number of transitions from the start to the accept
on just the accepting path (the depth of the tree).
• Starting at the starting configuration, print out each configuration in the format: left
of head string, state, head character and right of string..
If the simulation halts because of all paths lead to reject, ” String rejected in ”, followed
the number of steps from the start to the last reject (this should be the max depth).
If the step limit is exceeded, print out something like ”Execution stopped after” the
max step limit.
For example inputting the string ”aaaaa” for the aplus machine should accept at a
depth of 4 and the number of transitions should be somewhere between 4 and 15.
'''
