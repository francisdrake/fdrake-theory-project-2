import sys
import argparse
import csv
from dataclasses import dataclass
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

@dataclass
class Machine:
    desc: str
    states: list
    sigma: list
    gamma: list
    start: str
    accept: list
    reject: list
    transitions: list

def process_machine(machine_file):
    with open(machine_file, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

        # Formal definition of the TM
        machine = Machine(
          desc=rows[0][0],
          states=rows[1],
          sigma=rows[2],
          gamma=rows[3],
          start=rows[4][0],
          accept=rows[5],
          reject=rows[6],
          transitions=rows[7:] # For now going to use a list but may change
        )

        print(machine)
        return machine

def main():
    # To run: python3 traceTM_fdrake_program.py machine.csv input_string -t {depth}
    parser = argparse.ArgumentParser()

    # Positional arguments
    parser.add_argument('machine_file', type=str, help="Name of the file describing the machine")
    parser.add_argument('input_string', type=str, help="Input string to run")

    # Termination flag (optional)
    parser.add_argument('-t', '--depth', type=int, help="Stop at certain depth")

    # Parse arguments
    args = parser.parse_args()

    # Access parsed arguments
    print("Machine file:", args.machine_file)
    print("Input string:", args.input_string)
    print("Termination condition:", args.depth)

    # Process machine
    machine = process_machine(args.machine_file)

if __name__ == "__main__":
    main()
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
