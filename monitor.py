from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Value
from multiprocessing import Array

import random

class Table():
    def __init__(self, NPHIL, stora, ind):
        self.storage = stora
        self.nphil = NPHIL-1
        self.index = ind
        self.mutex = Lock()
        self.hay_cubiertos = Condition(self.mutex)
        
    def si_hay_cubiertos(self):
        if self.index.value == self.nphil:
            return (self.storage[self.index.value] == 1) and (self.storage[0] == 1)
        if self.index.value < self.nphil:
            return (self.storage[self.index.value] == 1) and (self.storage[self.index.value+1] == 1)
           
    def wants_eat(self,num):
        self.mutex.acquire()
        self.index.value = num
        print(f"{self.si_hay_cubiertos()} para {num} {self.storage[:]}")
        print(self.storage[:])
        self.hay_cubiertos.wait_for(self.si_hay_cubiertos)
        if num == self.nphil: #Se ocupan los tenedores
            self.storage[num] = 0
            self.storage[0] = 0
        if num < self.nphil:
            self.storage[num] = 0
            self.storage[num+1] = 0
        self.mutex.release()
        
    def wants_think(self,num):
        self.mutex.acquire()
        self.index.value = num
        if num == self.nphil: #Se liberan los tenedores
            self.storage[num] = 1
            self.storage[0] = 1
        if num < self.nphil:
            self.storage[num] = 1
            self.storage[num+1] = 1
        self.hay_cubiertos.notify()
        self.mutex.release()
       
               
        
        
        
        
