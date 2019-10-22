def findFaultList(ckt):
    faultList = list()
    gates = ckt["GATES"][1]
    inputs = ckt["INPUTS"][1]
    # Create TV for inputs
    for i in inputs:
        faultList.append(f'{i[5:]}-SA-0')
        faultList.append(f'{i[5:]}-SA-1')
    # Create TV for gates
    for gate in gates:
        faultList.append(f'{gate[5:]}-SA-0')
        faultList.append(f'{gate[5:]}-SA-1')
        for i in ckt[gate][1]:
            faultList.append(f'{gate[5:]}-IN-{i[5:]}-SA-0')
            faultList.append(f'{gate[5:]}-IN-{i[5:]}-SA-1')

    return faultList


def saveFaultList(faultList, filePath):
    with open(filePath, "w+") as f:
        f.write("# circuit.bench\n")
        f.write("# full SSA fault list\n\n")
        for fault in faultList:
            f.write(fault)
            f.write("\n")
        f.write("\n")
        f.write(f'# total faults: {len(faultList)}')
