#   Name: faultSim
#   Paramaters:
#       ckt: ciruit object
#       input_vectors: list of input vectors
#       fault_list: list of faults to check
#   Description:
#       Function takes in TVs, list of faults, and circuit
#       then will run the basic simulator with a modified circuit
#       object for each fault in fault_list and on each input_vector.
#       Keep track of all the results of basic_sim with our modified
#       ciruit object and return a results object that contains all the
#       results of the TVs with faults.
from pprint import pprint
from copy import deepcopy
from sim_functions.better_sim import better_sim
from sim_functions.gate_calc import gateCalc

# accepts a file path as a parameter and a returns a list
# of the faults in the file located at that path


def readFaultListFromFile(filePath):
    faultList = list()
    with open(filePath, "r") as f:
        for _, line in enumerate(f):
            line = line.strip()
            # skip comments
            if "#" in line:
                continue
            # check if line exists
            if not line:
                continue
            # assume rest of the lines are
            # formatted correctly
            faultList.append(line)
    return faultList


def __formatOutput__(outputList, outputDict):
    string = ""
    for output in outputList[::-1]:
        string += outputDict[output]
    return string


def writeFaultSimResultToFile(filePath, faultResult, files):
    with open(filePath, "w+") as f:
        f.write("# fault sim result\n")
        f.write(f'# input: {files["benchFile"]}\n')
        f.write(f'# input: {files["inputFile"]}\n')
        f.write(f'# input: {files["faultFile"]}\n\n')

        for index, test in enumerate(faultResult["testVectors"]):
            f.write("\n")
            f.write(
                f'tv{index} = {test} -> {__formatOutput__(faultResult["outputs"], faultResult[test]["initialOutput"])}\n')
            f.write("detected:\n")
            if "detected" not in faultResult[test]:
                f.write("None\n")
                continue
            for output in faultResult[test]["detected"]:
                f.write(
                    f'{output["fault"]}: {test} -> {__formatOutput__(faultResult["outputs"], output["result"])}\n')
        f.write("\n\n")
        f.write(f'# total detected faults: {len(faultResult["detected"])}\n\n')
        f.write(
            f'undetected faults: {len(faultResult["faults"]) - len(faultResult["detected"])}\n')
        for fault in faultResult["faults"]:
            if fault in faultResult["detected"]:
                continue
            f.write(f'{fault}\n')
        f.write("\n")
        f.write(
            f'fault coverage: {len(faultResult["detected"])}/{len(faultResult["faults"])}')
        f.write(
            f' {(len(faultResult["detected"])/len(faultResult["faults"])) * 100}%\n')


def __getoutputs__(ckt):
    outputs = ckt['OUTPUTS'][1]
    outputValues = dict()
    for output in outputs:
        outputValues[output] = ckt[output][3]
    return outputValues


def __compareoutputs__(ckt, initial_output, test_output):
    outputWires = ckt["OUTPUTS"][1]
    for wire in outputWires:
        if initial_output[wire] != test_output[wire]:
            return False
    return True

# fault list strings are in the form
#   - {OUTPUT_WIRE}-SA-{Value}
#   - {OUTPUT_WIRE}-IN-{INPUT_WIRE}-SA-{Value}
# input vectors are in the form
#   - LSB 00...00 MSB
#   - Length of vector is N (N = # of inputs for ckt)


def faultSim(ckt, input_vectors, fault_list):
    # results is a dictionary with vectors
    # used for the key and the value will be
    # a list of faults the test vector could
    # detect
    results = dict()
    results["detected"] = list()
    results["faults"] = fault_list
    results["testVectors"] = input_vectors
    results["outputs"] = ckt["OUTPUTS"][1]
    # Test for every input vector
    for vector in input_vectors:
        results[vector] = dict()
        # Get ckt ready for computation by
        # placing test vector into circuit
        inputWidth = ckt["INPUT_WIDTH"][1] - 1
        cktInputs = ckt["INPUTS"][1]
        for bit in vector:
            ckt[cktInputs[inputWidth]][3] = bit
            ckt[cktInputs[inputWidth]][2] = True
            inputWidth -= 1
        # keep initial state of ckt
        initialCkt = deepcopy(ckt)

        # Now we have a ckt that has the test
        # vector already inputted into ckt
        # We need to get an initial value for
        # circuit with no faults

        initialOutput = __getoutputs__(better_sim(ckt))

        # add initial output ot results object
        results[vector]["initialOutput"] = initialOutput

        # reset circuit
        ckt = deepcopy(initialCkt)
        # initialOutput is dictionary with the
        # outputs of the circuit with no fault
        # we will use this to compare against the
        # other circuits with faults to see if the
        # can find the fault.
        # Loop through all the faults to be tested.
        for fault in fault_list:
            if "-IN-" in fault:
                # Get all chars between start of string and -IN-
                outputWire = f'wire_{fault[:fault.find("-IN-")]}'
                # Get input wire
                inputWire = f'wire_{fault[fault.find("-IN-") + len("-IN-"):fault.find("-SA-")]}'
                # Get value for wire
                inputValue = fault[fault.find("-SA-") + len("-SA-"):]
                # Create new wire inside ckt
                ckt[fault] = [None, None, True, inputValue]
                # Switch out input wire with new faulty wire
                for index, x in enumerate(ckt[outputWire][1]):
                    if x == inputWire:
                        ckt[outputWire][1][index] = fault
            else:
                # Get the wire that needs to be changed
                wireToChange = f'wire_{fault[:fault.find("-SA-")]}'
                # Get the SA value
                inputValue = fault[fault.find("-SA-") + len("-SA-"):]
                # Change the wire with the SA value
                ckt[wireToChange][2] = True
                ckt[wireToChange][3] = inputValue
            # Run the faulty circuit
            faultyOutput = __getoutputs__(better_sim(ckt))
            # compare the ouputs
            if __compareoutputs__(ckt, initialOutput, faultyOutput) == False:
                # if the key in results doesn't exist then create it
                if "detected" not in results[vector]:
                    results[vector]["detected"] = list()
                # append the result of the vector
                results[vector]["detected"].append(
                    {"fault": fault, "result": faultyOutput})
                if fault not in results["detected"]:
                    results["detected"].append(fault)
            # reset circuit
            ckt = deepcopy(initialCkt)
    return results
