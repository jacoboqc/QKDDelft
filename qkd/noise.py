from random import choice

def testround(filt_count, filtered):
    test = []
    testindex = []
    filtered_update = []
    numberset = list(range(0, filt_count))
    if filt_count == 1:
        test = "Not enough common basis to test"
    else:
        for i in range(int(filt_count / 2)):
            rannum = choice(numberset)
            numberset.remove(rannum)
            testindex.append(rannum)
            test.append(filtered[rannum])
        for i in range(filt_count):
            if not i in testindex:
                filtered_update.append(filtered[i])
            else:
                continue
    return test, testindex, filtered_update


def testing(test_alice, test_bob, testindex, commonbasis, filtered, basis):
    counter = -1
    errors = 0
    errorh = 0
    for i in testindex:
        counter += 1
        if not test_alice[counter] == test_bob[counter]:
            if basis[commonbasis[i]] == 0:
                errors += 1
            elif basis[commonbasis[i]] == 1:
                errorh += 1
    return errors, errorh


def update_filtered(testindex, filtered):
    filtered_update = []
    for i in range(len(filtered)):
        if not i in testindex:
            filtered_update.append(filtered[i])
        else:
            continue
    return filtered_update


def errorconversion(e_s, e_h, test):
    e_t = round(((e_s + e_h) / len(test)) * 100, 2)
    e_s2 = 0;
    e_h2 = 0

    if not e_t == 0:
        e_s2 = (e_s / (e_s + e_h)) * 100
        e_h2 = (e_h / (e_s + e_h)) * 100
    return e_t, round(e_s2, 2), round(e_h2, 2)