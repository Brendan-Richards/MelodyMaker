import math

# implementation of equation 2 from Sethares
# calculates the dissonance between two frequencies f1 and f2 with amplitudes v1 and v2
def d(f1, f2, v1, v2):
    a = 3.5
    b = 5.75
    s1 = 0.021
    s2 = 19
    dMax = 0.24
    v12 = v1*v2
    s = dMax/(s1*f1+s2) # equation 3 from Sethares
    diff = math.fabs(f2-f1)

    return v12*(math.exp(-1*a*s*diff) - math.exp(-1*b*s*diff))

def dtotal(note_pairs):
    freqs = []
    amps = []
    for pair in note_pairs:
        f, a = partials(*pair)
        freqs += f
        amps += a

    total = 0
    for i in range(len(freqs)):
        for j in range(i, len(freqs)):
            total += d(freqs[i], freqs[j], amps[i], amps[j])

    return total
    # return total/len(freqs) if len(freqs)>0 else total


def partials(fundamental, t_type):
    amps = []
    if t_type == 'piano':
        amps = [1, 0.501092611, 0.812856003, 0.391979785, 0.40992112, 0.222737719, 0.261336265, 0.15929054]
    elif t_type == 'guitar':
        amps = [1, 0.548278121, 0.163137188, 0.13617664, 0.216986343, 0.410905253, 0.395508627,
                     0.144049132, 0.169127337, 0.259490366]
    else:
        print('error, dont understand the timbre type')
        exit(-1)
    freqs = []
    for i in range(1, len(amps) + 1):
        freqs.append(fundamental * i)

    return freqs, amps
