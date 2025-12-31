import numpy

A = numpy.array([0], dtype=int)
flag = int(input("Give me a number and I give u my flag\n"))
if(flag < 0):
    print("Nope")
    exit(1)
    
A[0] = flag
A[0] = A[0] + 1

if(A[0] < 0):
    print("Flag is in your hand")