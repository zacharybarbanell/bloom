import random
from math import log

class LinearHash(): #turns out this performs really poorly, around 3* expected false positive rate
    def __init__(self, n):
        random.seed()
        self.n = n
        self.a = random.randrange(1,n)
        self.b = random.randrange(n)
    def __call__(self, x):
        return (self.a * x + self.b) % self.n

class PRGHash(): #approximately matches expected false positive rate
    def __init__(self, n):
        random.seed()
        self.n = n
        self.s = random.randrange(1<<20000) #magic constant based on PRG details
    def __call__(self, x):
        random.seed(self.s + x)
        rv = random.randrange(self.n)
        random.seed() #don't want to break other randomness
        return rv

def false_positive(n, m, k):
    return (1 - ((1 - 1/n)**(m * k)))**k 

def optimize_k(n, m):
    exact_solution = (0-log(2)) / (m * log((n-1)/n))
    v1 = int(exact_solution)
    v2 = v1 + 1
    return min(v1, v2, key=lambda x: false_positive(n, m, x))
    

class BloomFilter():
    def __init__(self, n, values, hash_class=PRGHash, k=None):
        m = len(set(values))
        if k == None:
            k = optimize_k(n, m)
        self.hashes = []
        for i in range(k):
            self.hashes.append(hash_class(n))
        self.table = [False] * n
        for v in values:
            for h in self.hashes:
                self.table[h(v)] = True
    def __getitem__(self, v):
        return all(self.table[h(v)] for h in self.hashes)

def test_false_positive_rate(N,n,m,t,h=PRGHash,override_k=None): 
    assert n**2 < N and m**2 < N #unreasonable without these conditions
    s = set()
    while len(s) < m:
        s.add(random.randrange(N))
    bf = BloomFilter(n, s, h, override_k)
    expected_false_positives = round(false_positive(n, m, optimize_k(n, m))* t)
    actual_false_positives = 0
    for _ in range(t):
        x = random.randrange(N)
        while x in s: x = random.randrange(N)
        actual_false_positives += bf[x]
    print('Expected false positives:',expected_false_positives)
    print('Actual false positives:',actual_false_positives)

    
        
    
        
