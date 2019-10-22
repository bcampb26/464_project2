from __future__ import print_function
import os
from pprint import pprint
from fault_list import findFaultList, saveFaultList
from fault_sim import faultSim, readFaultListFromFile, writeFaultSimResultToFile
from sim_functions.basic_sim import basic_sim
from sim_functions.net_read import netRead
from sim_functions.print_ckt import printCkt
from sim_functions.input_read import inputRead
from sim_functions.lfsr import lfsr_fun


def faultListGeneration():
    script_dir = os.path.dirname(__file__)

    while True:
        cktFile = "circuit.bench"
        print("\n Read circuit benchmark file: use " + cktFile +
              "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            cktFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(cktFile):
                print("File does not exist. \n")
                raise FileExistsError
            else:
                break

    print("\n Reading " + cktFile + " ... \n")
    circuit = netRead(cktFile)
    print("\n Finished processing benchmark file and built netlist dictionary: \n")
    pprint(circuit)

    if "ERROR" in circuit:
        raise Exception

    faultList = findFaultList(circuit)

    print(f'Fault List ({len(faultList)}):')

    pprint(faultList)

    while True:
        outputFile = "full_f_list.txt"
        print("\n Write full fault list: use " + outputFile +
              "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            cktFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(outputFile):
                print("File does not exist. \n")
                raise FileExistsError
            else:
                break

    saveFaultList(faultList, f'./{outputFile}')


def faultSimulation():
    script_dir = os.path.dirname(__file__)

    # Get user information about file paths
    while True:
        cktFile = "circuit.bench"
        print("\n Read circuit benchmark file: use " + cktFile +
              "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            cktFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(cktFile):
                print("File does not exist. \n")
                raise FileExistsError
            else:
                break

    print("\n Reading " + cktFile + " ... \n")
    circuit = netRead(cktFile)
    print("\n Finished processing benchmark file and built netlist dictionary: \n")
    pprint(circuit)

    # input list
    while True:
        inputFile = "input.txt"
        print("\n Read input file file: use " + inputFile +
              "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            inputFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(inputFile):
                print("File does not exist. \n")
                raise FileExistsError
            else:
                break

    print(f'Reading {inputFile} ... \n')
    testVectors = readFaultListFromFile(inputFile)
    print("Finished reading input file: \n")
    pprint(testVectors)

    # fault list
    while True:
        faultFile = "f_list.txt"
        print("\n Read fault list file: use " + faultFile +
              "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            faultFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(faultFile):
                print("File does not exist. \n")
                raise FileExistsError
            else:
                break

    print(f'Reading {faultFile} ... \n')
    faultList = readFaultListFromFile(faultFile)
    print("Finished reading fault file: \n")
    pprint(faultList)

    print("Running")

    faultResult = faultSim(circuit, testVectors, faultList)

    writeFaultSimResultToFile("./fault_sim_result.txt", faultResult, {
        "benchFile": cktFile,
        "inputFile": inputFile,
        "faultFile": faultFile
    })

    print("Completed")

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Main Function


def main():
    print("What would you like to do? (0/1:")
    print("0: Fault Simulation")
    print("1: Fault List Generation")
    userSimulationChoice = input()

    if userSimulationChoice.strip() == "0":
        faultSimulation()
        return
    elif userSimulationChoice.strip() == "1":
        faultListGeneration()
        return
    # **************************************************************************************************************** #
    # NOTE: UI code; Does not contain anything about the actual simulation

    # Used for file access
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    print("Circuit Simulator:")

    # Select circuit benchmark file, default is circuit.bench
    while True:
        cktFile = "test.bench"
        print("\n Read circuit benchmark file: use " + cktFile +
              "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            cktFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(cktFile):
                print("File does not exist. \n")
            else:
                break

    print("\n Reading " + cktFile + " ... \n")
    circuit = netRead(cktFile)
    print("\n Finished processing benchmark file and built netlist dictionary: \n")
    pprint(circuit)

    # keep an initial (unassigned any value) copy of the circuit for an easy reset
    newCircuit = circuit

    # Select input file, default is input.txt
    while True:
        inputName = "test_input.txt"
        print("\n Read input vector file: use " + inputName +
              "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            inputName = os.path.join(script_dir, userInput)
            if not os.path.isfile(inputName):
                print("File does not exist. \n")
            else:
                break

    # Select output file, default is output.txt
    while True:
        outputName = "test_output.txt"
        print("\n Write output file: use " + outputName +
              "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            break
        else:
            outputName = os.path.join(script_dir, userInput)
            break

    print("Circuit:")
    pprint(circuit)

    # Note: UI code;
    # **************************************************************************************************************** #

    print("\n *** Simulating the" + inputName +
          " file and will output in" + outputName + "*** \n")
    inputFile = open(inputName, "r")
    outputFile = open(outputName, "w")

    # Runs the simulator for each line of the input file
    for line in inputFile:
        # Initializing output variable each input line
        output = ""

        # Do nothing else if empty lines, ...
        if (line == "\n"):
            continue
        # ... or any comments
        if (line[0] == "#"):
            continue

        # Removing the the newlines at the end and then output it to the txt file
        line = line.replace("\n", "")
        outputFile.write(line)

        # Removing spaces
        line = line.replace(" ", "")

        print("\n before processing circuit dictionary...")
        # Uncomment the following line, for the neater display of the function and then comment out print(circuit)
        pprint(circuit)
        # printCkt(circuit)
        # print(circuit)
        print("\n ---> Now ready to simulate INPUT = " + line)
        circuit = inputRead(circuit, line)
        # Uncomment the following line, for the neater display of the function and then comment out print(circuit)
        # printCkt(circuit)
        pprint(circuit)
        # print(circuit)

        if circuit == -1:
            print("INPUT ERROR: INSUFFICIENT BITS")
            outputFile.write(" -> INPUT ERROR: INSUFFICIENT BITS" + "\n")
            # After each input line is finished, reset the netList
            circuit = newCircuit
            print("...move on to next input\n")
            continue
        elif circuit == -2:
            print("INPUT ERROR: INVALID INPUT VALUE/S")
            outputFile.write(" -> INPUT ERROR: INVALID INPUT VALUE/S" + "\n")
            # After each input line is finished, reset the netList
            circuit = newCircuit
            print("...move on to next input\n")
            continue

        circuit = basic_sim(circuit)
        print("\n *** Finished simulation - resulting circuit: \n")
        # Uncomment the following line, for the neater display of the function and then comment out print(circuit)
        printCkt(circuit)
        # print(circuit)

        for y in circuit["OUTPUTS"][1]:
            if not circuit[y][2]:
                output = "NETLIST ERROR: OUTPUT LINE \"" + y + "\" NOT ACCESSED"
                break
            output = str(circuit[y][3]) + output

        print("\n *** Summary of simulation: ")
        print(line + " -> " + output + " written into output file. \n")
        outputFile.write(" -> " + output + "\n")

        # After each input line is finished, reset the circuit
        print("\n *** Now resetting circuit back to unknowns... \n")

        for key in circuit:
            if (key[0:5] == "wire_"):
                circuit[key][2] = False
                circuit[key][3] = 'U'

        print("\n circuit after resetting: \n")
        # Uncomment the following line, for the neater display of the function and then comment out print(circuit)
        printCkt(circuit)
        # print(circuit)

        print("\n*******************\n")

    outputFile.close()
    inputFile.close()

    # exit()


if __name__ == "__main__":
    main()
