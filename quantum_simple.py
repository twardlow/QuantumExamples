import dimod
from dwave.system import DWaveSampler, EmbeddingComposite

#Define the BQM for our problem space
bqm = dimod.BinaryQuadraticModel({'x1': 0.0, 'x2': 0.0, 'y1': 6.0},
                  {('x2', 'x1'): 2.0, ('y1', 'x1'): -4.0, ('y1', 'x2'): -4.0},
                  0, 'BINARY')


# Use the default D-Wave sampler solver to solve the problem
sampler = EmbeddingComposite(DWaveSampler())

#Generate the response by using the sampler to sample the BQM
response = sampler.sample(bqm, num_reads=1000)

#Print the output
print(response)
