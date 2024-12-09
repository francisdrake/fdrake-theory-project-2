# Theory Project 2 - Tracing NTM Behavior
# Francis Drake (fdrake)

# example to run:
# python3 traceTM_program_fdrake.py traceTM_testfiles_fdrake/equal_01s_fdrake.csv traceTM_testfiles_fdrake/equal_01s_input_fdrake.txt -t 50 -o accuracy_output_fdrake.txt

import argparse
import csv
from dataclasses import dataclass
import os
import time

@dataclass
class Machine:
    desc: str
    states: list
    sigma: list
    gamma: list
    start: str
    accept: list
    reject: list
    transitions: dict

def process_machine(machine_file):
    '''Reads in info from csv file into formatted machine data class'''
    with open(machine_file, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

        # Read in transitions
        transition_dict = {}
        for row in rows[7:]:
            curr_state = row[0]
            read_symbol = row[1]
            next_state = row[2]
            write_symbol = row[3]
            direction = row[4]

            if curr_state not in transition_dict:
                transition_dict[curr_state] = {}
            if read_symbol not in transition_dict[curr_state]:
                transition_dict[curr_state][read_symbol] = []

            transition_dict[curr_state][read_symbol].append((next_state, write_symbol, direction))

            # Visualization of the structure:
            # transitions = {
            #     'q0': {
            #         'a': ('q1', 'b', 'R'),
            #         'b': ('q2', 'a', 'L'),
            #     },
            # }

        # Formal definition of the TM
        machine = Machine(
          desc=rows[0][0],
          states=rows[1],
          sigma=rows[2],
          gamma=rows[3],
          start=rows[4][0],
          accept=rows[5],
          reject=rows[6],
          transitions=transition_dict
        )

        return machine
    
def run_machine_on_string(string, start_state, transitions, qacc, qrej, max_depth=None, time_limit=None):
    '''Performs a breadth first exploration of a given TM transitions'''
    configurations = [["", start_state, string]] # [”aa”,”q1”, ”a”] <-- this is a configuration
    bfs_tree = []
    curr_state = start_state
    depth = 0
    num_transitions = 0
    degree_of_nondeterminism = 0

    # Record start time
    start_time = time.time()

    # Breadth first search
    while configurations:
        temp_degree_count = 0
        moves = []

        for c in configurations: # Explore every node at this level
            left_tape, curr_state, right_tape = c

            if not right_tape: # Add another blank if necessary
                right_tape = "_"

            next_char_to_process = right_tape[0] # Char under the head

            # Look for possible moves and loop through them if there are any
            temp_degree_count = 0
            if curr_state in transitions and next_char_to_process in transitions[curr_state]:
                temp_degree_count = len(transitions[curr_state][next_char_to_process])
                for transition in transitions[curr_state][next_char_to_process]:
                    new_state, write_char, direction = transition

                    tape_after_transition = write_char + right_tape[1:] # Add new char to leftmost part of the right side of the tape
                    # Consume the read char with right_tape[1:] as the tape under the head is right_tape[0]

                    # Adjust the tape based on left or right move
                    if direction == "R":
                        new_left_tape = left_tape + tape_after_transition[0] # Get the leftmost char on the right side of the tape
                        # For example, 01 q1 01 on a right move becomes 010 q1 1
                        new_right_tape = tape_after_transition[1:] if len(tape_after_transition) > 1 else ""
                    elif direction == "L":
                        # Get rid of rightmost char on left tape
                        # For example, 01 q1 01 on a left move becomes 0 q1 101
                        # ^ Add that char to the right side
                        if left_tape:
                            new_left_tape = left_tape[:-1]
                            new_right_tape = left_tape[-1] + tape_after_transition
                        else:
                            new_left_tape = "_"
                            new_right_tape = "_" + tape_after_transition

                    if new_state == qacc:
                        new_move = [new_left_tape, new_state, new_right_tape]
                        moves.append(new_move)
                        bfs_tree.append(moves)
                        print(f"Accepted: {new_state}")
                        return bfs_tree, depth, num_transitions, degree_of_nondeterminism, True
                    if new_state == qrej: # most reject states are not specified
                        # so this case will likely never be reached
                        print("String not accepted")
                        return bfs_tree, depth, num_transitions, degree_of_nondeterminism, False
                    if max_depth and depth >= max_depth:
                        print("Max depth reached")
                        return bfs_tree, depth, num_transitions, degree_of_nondeterminism, False
                    
                    num_transitions += 1
                    new_move = [new_left_tape, new_state, new_right_tape]
                    moves.append(new_move)
                
                degree_of_nondeterminism = max(degree_of_nondeterminism, temp_degree_count)

        # Check time limit
        elapsed_time = time.time() - start_time
        if time_limit and elapsed_time > time_limit:
            print(f"Timit limit exceeded. Execution stopped after {elapsed_time:.2f} seconds.")
            return bfs_tree, depth, num_transitions, False

        depth += 1
        bfs_tree.append(configurations)
        configurations = moves

    # Triggered when there are no more moves --> implying rejection
    return bfs_tree, depth, num_transitions, degree_of_nondeterminism, False

def main():
    # To run: python3 traceTM_program_fdrake.py traceTM_testfiles_fdrake/a_plus_fdrake.csv traceTM_testfiles_fdrake/a_plus_input_fdrake.txt -t 50 -o output.txt
    parser = argparse.ArgumentParser()

    # Positional arguments
    parser.add_argument('machine_file', type=str, help="Name of the file describing the machine")
    parser.add_argument('input_strings', nargs='+', help="Input strings to run OR file name containing strings")

    # Termination flag (optional)
    parser.add_argument('-t', '--depth', type=int, help="Stop at certain depth")
    parser.add_argument('--time', type=int, help="Stop at certain time")
    parser.add_argument('-o', '--output', type=str, help="File to write output to")

    # Parse arguments
    args = parser.parse_args()

    # Input strings handling - list or file
    input_strings = []
    expected_results = []
    if len(args.input_strings) == 1 and os.path.isfile(args.input_strings[0]):
        # Read input strings and expected results from file
        with open(args.input_strings[0], 'r', encoding='utf-8') as f:
            for line in f.readlines():
                string, expected = line.strip().split(', ')
                input_strings.append(string)
                expected_results.append(expected == "accept")  # Store True for accept, False for reject
    else:
        # Otherwise assume it's a list of strings with no expected results
        input_strings = args.input_strings
        expected_results = [None] * len(input_strings)  # No expected results in this case
    num_strings = len(input_strings)

    # Get machine formal definition
    machine = process_machine(args.machine_file)

    # Prepare output file if given
    output_file = args.output
    if output_file:
        output_f = open(output_file, 'a', encoding='utf-8')

    # Output
    num_wrong = 0
    for index, input_string in enumerate(input_strings):
        # Run the machine on the string
        tree, depth, num_transitions, degree_nondet, status = run_machine_on_string(
            input_string, 
            machine.start, 
            machine.transitions, 
            machine.accept[0], 
            machine.reject[0], 
            args.depth, 
            args.time
        )
        depth = depth - 1 # Because the depth accounted for the first state before any transitions

        # Prepare results
        result = []
        result.append(f"Name of machine: {machine.desc}")
        result.append(f"Input string: {input_string}")
        result.append(f"Tree depth: {depth}")
        result.append(f"Total number of transitions simulated: {num_transitions}")
        result.append(f"Degree of nondeterminism: {degree_nondet}")

        # Accepted or rejected
        if status:
            result.append(f"String accepted in {depth} transitions")
        else:
            result.append(f"String rejected in {depth} transitions")

        # Check answer
        expected = expected_results[index] if expected_results else None
        if expected is not None:
            result.append("Expected result: " + ("accept" if expected else "reject"))
            if status != expected:
                num_wrong += 1

        # Tree structure
        result.append("Tree levels:")
        for level in tree:
            result.append(str(level))

        # Stdout
        for line in result:
            print(line)

        # Write to file
        if output_file:
            output_f.write("\n".join(result) + "\n\n")

        # Separator between inputs
        if index + 1 != num_strings:
            print()
            if output_file:
                output_f.write("\n")

    if expected is not None:
        print(f"{num_wrong} wrong")
        if output_file:
            output_f.write(f"{num_wrong} wrong")

    # Close file
    if output_file:
        output_f.close()

if __name__ == "__main__":
    main()