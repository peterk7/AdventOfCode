#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
from collections import defaultdict, deque
import pprint

import math
import pdb

# import traceback
# import logging
# import json
# import functools
from tqdm import tqdm, trange
import heapq

DAY = "10"
DEV = True  # Enable development logging

# Define test cases: (input_num, expected_part1, expected_part2)
test_cases = [
    # (3, 2, 10),
    # (4, 3, 12),
    # (5, 2, 11),
    # (1, 7, 33),
    # (6, 1, 112),  # 112?
    # (8, 1, 168),
    (2, 527, None),
    # (7, 2, 0),
]

# Set recursion limit as needed
# sys.setrecursionlimit(5000)
print(f"Recursion limit is: {sys.getrecursionlimit()}")

# Enable ANSI color codes on Windows
if os.name == "nt":
    os.system("")


# ANSI color codes
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def log(*args, **kwargs):
    """Log output only if DEV mode is enabled"""
    if DEV:
        print(*args, **kwargs)


class System:
    def __init__(self):
        self.challenge = Challenge()
        return

    def __str__(self):
        return f"System"

    def reset(self):
        """Reset the system state for a new test run"""
        self.challenge = Challenge()

    def processFile(self, input_path):
        """Read and process an input file"""
        with open(input_path, "r") as f:
            for line in f:
                if line == "\n":
                    log("Empty line")
                else:
                    line = line.strip()
                    self.challenge.processLine(line)

    def getResults(self):
        """Return the results as a tuple (part1, part2)"""
        return (self.part1(), self.part2())

    def part1(self):
        return self.challenge.processPart1()

    def part2(self):
        return self.challenge.processPart2()


class Challenge:

    def __init__(self):
        self.machines = []
        return

    def __str__(self):
        return f""

    def processLine(self, line):
        # log("\nProcessing line: ", line)
        lineSplit = line.split(" ")
        expectedState = lineSplit[0]
        buttons = lineSplit[1:-1]
        jolts = lineSplit[-1]
        # log(f"Expected Config: {expectedState}")
        # log(f"Buttons: {buttons}")
        # log(f"Jolts: {jolts}")

        # Process expected config
        expectedState = list(expectedState.strip("[]"))
        expectedState = list(map(lambda state: state == "#", expectedState))
        # log(f"Expected Config: {expectedState}")

        # Process Buttons
        buttons = list(map(lambda button: button.strip("()").split(","), buttons))
        buttons = list(
            map(lambda button: list(map(lambda btn: int(btn), button)), buttons)
        )
        # log(f"Buttons: {buttons}")

        # Process Jots
        jolts = jolts.strip("{}").split(",")
        jolts = list(map(int, jolts))
        # log(f"Jolts: {jolts}")

        self.machines.append(Machine(expectedState, buttons, jolts))

        return

    def processPart1(self):
        sum = 0
        for machine in tqdm(self.machines):
            # log(f"{machine}")
            results = machine.calculatePresses()
            minPresses = min(results.keys())
            # log(f"Min presses: {minPresses}")
            sum += minPresses
        return sum

    def processPart2(self):
        sum = 0
        for machine in tqdm(self.machines):
            log(f"Checking machine: {machine.jolts}")
            presses, combination = machine.calculatePressesForJolts()
            if presses is None:
                log(f"No solution found for machine: {machine.jolts}")
                continue
            sum += presses
        return sum


class Machine:
    def __init__(self, expectedState, buttons, jolts):
        self.expectedState = expectedState
        self.buttons = sorted(buttons, key=len, reverse=True)
        self.jolts = jolts
        return

    def __str__(self):
        return f"Machine(\n\texpectedState=[{self.expectedState}],\n\tbuttons={self.buttons},\n\tjolts={self.jolts}\n)"

    def calculatePresses(self, targetState=None):

        if targetState is None:
            targetState = self.expectedState

        # log(f"~" * 120)
        startingState = [False] * len(targetState)
        # log(f"Starting State: {startingState}")
        # log(f"Expected State: {targetState}")
        # log(f"Buttons: {self.buttons}")
        # visitedStates = defaultdict(bool)
        # visitedStates[tuple(startingState)] = True

        state = MachineState(startingState[:], 0)
        results = self.calculatePressesToTargetState(
            state, targetState, self.buttons[:]
        )
        # log(f"Results: {pprint.pprint(results)}")
        return results

    def calculatePressesToTargetState(self, machineState, targetState, possibleButtons):
        indent = "\t" * machineState.count
        results = defaultdict(list)

        if self.compareButtonsStates(machineState.state, targetState):
            # log(indent + f"Machine state: {machineState}")
            # log(indent + f"Reached target state!")
            results[machineState.count].append(machineState.pressedButtons)
            # return results

        if len(possibleButtons) == 0:
            # log(indent + f"No possible buttons, returning results: {results}")
            return results

        # log(indent + f"~" * 120)
        # log(indent + f"Possible buttons: {possibleButtons}")
        # log(indent + f"Machine state: {machineState}")
        # log(f"Target state: {targetState}")
        for index, button in enumerate(possibleButtons):

            newState = machineState.duplicate()
            newState.applyButton(button)
            nextbuttons = (
                possibleButtons[index + 1 :] if index + 1 < len(possibleButtons) else []
            )
            # log(
            #     indent
            #     + f"Applying button: {button} to machine state, remaining buttons: {nextbuttons}"
            # )
            newResults = self.calculatePressesToTargetState(
                newState, targetState, nextbuttons
            )
            for presses, buttons in newResults.items():
                results[presses] += buttons

        return results

    def compareButtonsStates(self, state1, state2):
        for i in range(len(state1)):
            if state1[i] != state2[i]:
                return False
        return True

    def calculateJoltsBFS(self):
        # log(f"~" * 120)
        startingState = [0] * len(self.jolts)
        # log(f"Starting State: {startingState}")
        # log(f"Expected Jolts: {self.jolts}")
        visitedStates = defaultdict(bool)
        visitedStates[tuple(startingState)] = True

        if self.compareJoltsStates(startingState, self.jolts) == 1:
            return 0

        # BFS over buttons untill reaching desired state
        queue = deque()
        for button in self.buttons:
            queue.append(MachineStatePart2(startingState[:], 0, button, True))

        while queue:
            currentState = queue.popleft()

            # Apply button to current state
            # log(
            #     f"Applying button: {currentState.nextButton} to state: {currentState.state}"
            # )
            currentState.applyButton()
            # log(f"New state: {currentState.state}")

            if visitedStates[tuple(currentState.state)]:
                # log(f"State {currentState.state} has been visited")
                continue
            visitedStates[tuple(currentState.state)] = True

            compareResult = self.compareJoltsStates(currentState.state, self.jolts)
            if compareResult == 1:
                return currentState.count
            if compareResult == -1:
                # log(
                #     f"State {currentState.state} is greater than expected jolts {self.jolts}"
                # )
                continue

            for button in self.buttons:
                queue.append(
                    MachineStatePart2(
                        currentState.state[:],
                        currentState.count,
                        button,
                        True,
                    )
                )
        return 0

    def compareJoltsStates(self, state1, state2):
        # log(f"Comparing states: {state1} and {state2}")
        # pdb.set_trace()
        equalCount = 0
        for i in range(len(state1)):
            if state1[i] > state2[i]:
                return -1
            if state1[i] == state2[i]:
                equalCount += 1
        if equalCount == len(state1):
            return 1
        return 0

    def calculateJoltsAStar(self):
        # log(f"~" * 120)
        startingState = [0] * len(self.jolts)
        # log(f"Starting State: {startingState}")
        # log(f"Expected Jolts: {self.jolts}")
        visitedStates = defaultdict(bool)
        visitedStates[tuple(startingState)] = True

        if self.compareJoltsStates(startingState, self.jolts) == 1:
            return 0

        # A* search
        priorityQueue = []
        distanceFromEnd = sum(self.jolts)
        for button in self.buttons:
            searchState = MachineStatePart2(startingState[:], 0, button, True)
            searchState.distanceFromEnd = distanceFromEnd
            heapq.heappush(priorityQueue, (searchState.distanceFromEnd, searchState))

        while priorityQueue:
            # pprint.pprint(priorityQueue)
            # pdb.set_trace()
            currentDistance, currentState = heapq.heappop(priorityQueue)
            # log(f"Current state: {currentState}")
            # pdb.set_trace()

            # Apply button to current state
            # log(
            #     f"Applying button: {currentState.nextButton} to state: {currentState.state}"
            # )
            currentState.applyButton()
            currentState.updateDistanceFromEnd(self.jolts)
            # log(f"New state: {currentState.state}")

            if visitedStates[tuple(currentState.state)]:
                # log(f"State {currentState.state} has been visited")
                continue
            visitedStates[tuple(currentState.state)] = True

            compareResult = self.compareJoltsStates(currentState.state, self.jolts)
            # log(f"Compare result: {compareResult}")
            if compareResult == 1:
                return currentState.count
            if compareResult == -1:
                # log(
                #     f"State {currentState.state} is greater than expected jolts {self.jolts}"
                # )
                continue

            for button in self.buttons:
                searchState = MachineStatePart2(
                    currentState.state[:],
                    currentState.count,
                    button,
                    True,
                    currentState.distanceFromEnd,
                )
                heapq.heappush(
                    priorityQueue,
                    (searchState.distanceFromEnd + searchState.count, searchState),
                )
        return 0

    def calculatePressesForJolts(self):
        return self.calculateJoltsForPressesStep(self.jolts)

    def calculateJoltsForPressesStep(self, targetJolts, depth=0):
        indent = "\t" * depth
        # log(indent + f"~" * 120)
        # log(indent + f"targetJolts: {targetJolts}")

        oddPlacements = []

        empty = True
        for jolts in targetJolts:
            oddPlacements.append(jolts % 2 == 1)
            if jolts > 0:
                empty = False

        # log(indent + f"Odd placements: {oddPlacements}")

        if empty:
            # log(indent + f"Empty target jolts, returning 0, []")
            return (0, [])

        startingState = [False] * len(targetJolts)
        stepState = MachineState(startingState[:], 0)
        results = self.calculatePressesToTargetState(
            stepState, oddPlacements, self.buttons[:]
        )
        # log(indent + f"Results:")
        # pprint.pprint(results)

        totalCounts = defaultdict(list)
        for count, combinations in results.items():
            for combination in combinations:
                # log(indent + f"Checking Combination: {combination}")
                # Calculate remainder after combination is applied
                remainder = targetJolts[:]
                for button in combination:
                    for index in button:
                        remainder[index] -= 1

                # Id any negative, continue
                if any(i < 0 for i in remainder):
                    # log(indent + f"Remainder is negative, continuing: {remainder}")
                    continue

                # log(indent + f"Remainder: {remainder}")
                remainderHalf = [i // 2 for i in remainder]
                remainderCount, remainderCombinations = (
                    self.calculateJoltsForPressesStep(remainderHalf, depth + 1)
                )
                if remainderCount is None:
                    # log(
                    #     indent
                    #     + f"No solution found for remainder half: {remainderHalf}"
                    # )
                    continue
                totalCount = count + 2 * remainderCount
                # log(indent + f"Remainder half count: {remainderCount}")
                # log(indent + f"Total count: {totalCount}")
                totalCombinations = combinations + remainderCombinations
                totalCounts[totalCount].append(totalCombinations)

        # log(indent + f"Total counts:")
        # pprint.pprint(totalCounts)
        if len(totalCounts) > 0:
            minCount = min(totalCounts.keys())
            combination = totalCounts[minCount][0]
            return minCount, combination
        return None, []

    def compareJoltsFromCombination(self, combination, targetJolts):
        jolts = [0] * len(self.jolts)
        for button in combination:
            for index in button:
                jolts[index] += 1
        return self.compareJoltsStates(jolts, targetJolts)


class MachineState:

    def __init__(
        self,
        state,
        count,
        pressedButtons=None,
    ):
        self.state = state
        self.count = count
        self.pressedButtons = pressedButtons if pressedButtons is not None else []
        return

    def __str__(self):
        return f"MachineState(\n\tstate={self.state},\n\tcount={self.count},\n\tpressedButtons={self.pressedButtons}\n)"

    def applyButton(self, button):
        for index in button:
            self.state[index] = not self.state[index]
        self.count += 1
        self.pressedButtons.append(button)
        return

    def duplicate(self):
        return MachineState(self.state[:], self.count, self.pressedButtons[:])


class MachineStatePart2:

    def __init__(
        self,
        state,
        count,
        nextButton,
        isJolts=False,
        distanceFromEnd=0,
        pressedButtons=None,
    ):
        self.state = state
        self.distanceFromEnd = distanceFromEnd
        self.count = count
        self.nextButton = nextButton
        self.isJolts = isJolts
        self.pressedButtons = pressedButtons if pressedButtons is not None else []
        return

    def __str__(self):
        return f"MachineStatePart2(\n\tstate={self.state},\n\tdistanceFromEnd={self.distanceFromEnd},\n\tcount={self.count},\n\tnextButton={self.nextButton},\n\tisJolts={self.isJolts},\n\tpressedButtons={self.pressedButtons}\n)"

    def applyButton(self):
        for index in self.nextButton:
            if self.isJolts:
                self.state[index] += 1
            else:
                self.state[index] = not self.state[index]
        self.count += 1
        self.pressedButtons.append(self.nextButton)
        return

    def updateDistanceFromEnd(self, endState):
        self.distanceFromEnd = 0
        for i in range(len(self.state)):
            self.distanceFromEnd += abs(endState[i] - self.state[i])
        return self.distanceFromEnd

    def __lt__(self, other):
        return len(self.nextButton) > len(other.nextButton)


def validatePart(part_name, result, expected):
    if expected is not None:
        passed = result == expected
        if passed:
            status = f"{Colors.GREEN}✓ PASS{Colors.RESET}"
            print(
                f"{part_name}: {Colors.GREEN}{result}{Colors.RESET} (expected {expected}) {status}"
            )
        else:
            status = f"{Colors.RED}✗ FAIL{Colors.RESET}"
            print(
                f"{part_name}: {Colors.RED}{result}{Colors.RESET} (expected {expected}) {status}"
            )
        return passed
    else:
        print(f"{part_name}: {Colors.YELLOW}{result}{Colors.RESET}")
        return True


def runTest(system, input_num, expected_part1=None, expected_part2=None):
    input_path = f"./day{DAY}/input{input_num}.txt"

    print(f"\n{'='*60}")
    print(f"Running test for Input {input_num}")
    print(f"{'='*60}")

    system.reset()
    system.processFile(input_path)
    part1_result, part2_result = system.getResults()

    part1_passed = validatePart("Part 1", part1_result, expected_part1)
    part2_passed = validatePart("Part 2", part2_result, expected_part2)

    return part1_passed and part2_passed


def main():
    print("Start")
    st = time.time()

    system = System()
    all_passed = True

    for input_num, expected_part1, expected_part2 in test_cases:
        passed = runTest(system, input_num, expected_part1, expected_part2)
        if not passed:
            all_passed = False

    print(f"\n{'='*60}")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}All tests PASSED ✓{Colors.RESET}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}Some tests FAILED ✗{Colors.RESET}")
    print(f"{'='*60}")

    elapsed_time = time.time() - st
    print("Execution time:", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print("End")


if __name__ == "__main__":
    main()


def isNumber(var):
    return type(var) == int or type(var) == float
