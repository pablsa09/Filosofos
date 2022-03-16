from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array, Value
import time
import random

from monitor import Table

NPHIL = 5 #Número de filósofos

def delay(n):
    time.sleep(random.random()/n)
    
def philosopher_task(num:int, table: Table):
    while True: #Los filósofos nunca paran de pensar y de comer
        print (f"Philosofer {num} thinking")
        print (f"Philosofer {num} wants to eat")
        table.wants_eat(num)
        print (f"Philosofer {num} eating")
        delay(3)
        table.wants_think(num)
        print (f"Philosofer {num} stops eating")
        
def main():
    index = Value('i', 0) #Índice que guarda la posición del filósofo que quiere comer
    storage = Array('i',NPHIL)
    """
    storage guarda la información sobre los tenedores disponibles. Para cada posición
    num<NPHIL-1, de un filósofo storage[num] y storage[num+1] indica la disponibilidad
    de tenedores a la izquierda y derecha respectivamente. Si num == NPHIL-1, entonces
    esto se indica en storage[num] y storage[0]. Con un 0 indicamos que el tenedor
    está ocupado y con un 1 que está libre.
    """
    for i in range(NPHIL):
        storage[i] = 1
    table = Table(NPHIL, storage, index)
    philosofers = [Process(target=philosopher_task, args=(i,table)) \
                   for i in range(NPHIL)]
    for i in range(NPHIL):
        philosofers[i].start()
    for i in range(NPHIL):
        philosofers[i].join()

if __name__ == '__main__':
    main()






