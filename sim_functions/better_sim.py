from sim_functions.gate_calc import gateCalc


def better_sim(circuit):
    queue = list(circuit["GATES"][1])
    i = 1

    while True:
        i -= 1
        if len(queue) == 0:
            break

        curr = queue[0]
        queue.remove(curr)

        term_has_value = True

        if circuit[curr][2]:
            continue

        for term in circuit[curr][1]:
            if not circuit[term][2]:
                term_has_value = False
                break

        if term_has_value:
            circuit[curr][2] = True
            circuit = gateCalc(circuit, curr)
            if isinstance(circuit, str):
                raise Exception
        else:
            queue.append(curr)

    return circuit
