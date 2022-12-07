from Pyro4 import expose 
from random import randint
import math
import random 
 
class Solver: 
    def __init__(self, workers=None, input_file_name=None, output_file_name=None): 
        self.input_file_name = input_file_name 
        self.output_file_name = output_file_name 
        self.workers = workers 
        print("Inited") 
     
    def solve(self): 
        print("Job Started") 
        print("Workers %d" % len(self.workers))
     
        data = self.read_input() 
        m = int(data[0])
        n = int(data[1])
        step = m * n / len(self.workers)
     
        matrix = []
        mapped = [] 
        for i in xrange(0, len(self.workers)):
            result = self.workers[i].my_map(i * step, i * step + step)
            mapped.append(result)
        
        reduced, values = self.my_reduce(mapped)
        norm = math.sqrt(reduced)
        for x in values:
            self.append_output(x)
        self.append_output(norm)
        print("Job Finished")
    
    @staticmethod
    @expose
    def my_map(a, b):
        matrixPart = []
        result = 0

        for i in xrange(a, b):
             matrixPart.append(random.randint(0, 1000))

        for i in xrange(len(matrixPart)):
            result += matrixPart[i] * matrixPart[i]

        return result

    @staticmethod
    @expose
    def my_reduce(mapped):
        output = 0
        values = []

        for x in mapped:
            output += x.value
            values.append(x.value)
        
        return output, values

    def read_input(self): 
        data = [] 
        f = open(self.input_file_name, 'r') 
        data.append(f.readline().strip('\n').strip('\r')) 
        data.append(f.readline().strip('\n').strip('\r')) 
        f.close() 
        return data 
             
    def append_output(self, output):
        f = open(self.output_file_name, 'a') 
        f.write(str(output) + '\n')
        f.close() 
        print("output done")
