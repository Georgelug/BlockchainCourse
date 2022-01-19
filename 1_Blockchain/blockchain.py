# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 13:43:26 2022

@author: Jorge L. Esparza
"""

# Modulo 1 - creando una cadena de bloques

# Se usa la biblioteca o modulo Flask y el cliente HTTP Postman

# modulos
import datetime # modulo que se va utilizar para las datestamp
import hashlib # modulo para aplicar los algoritmos de hashing
import json # modulo para crear ficheros json para codificar y empaquetar en json las cadenas de bloque
from flask import Flask, jsonify # modulo del cual se importa el constructor y jsonify para transformar la peticion en json

# =============================================================================
# class Block:
#     def __init__(self, number, nonce, data, prevHashCode = '0'):
#         self.number = number
#         self.nonce = nonce
#         self.data = data
#         self.hashCode = '0'
#         self.prevHashCode = prevHashCode
#     
#     def setHasCode(self):
#         self.hashCode = '0'
# =============================================================================
        
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, prevHashCode = '0') # se crea el bloque genesis
    
    #getter y setter de chain
    def setChain(self,chain): 
        self.chain = chain
    def getChain(self):
        return self.chain
    
    def addBlockToChain(self,block): # metodo para agregar un bloque a la cadena
        tmp = self.getChain()
        tmp.append(block)
        self.setChain(tmp)
        
    def create_block(self,proof,prevHashCode):
        newblock = {
                    'index': len(self.chain)+1, # numero del bloque
                    'timestamp': str(datetime.datetime.now()), # fecha exacta del minado del bloque
                    'proof': proof, # proof of work, es el nonce obtenido del minado
                    'prevHashCode' : prevHashCode,
                    #data : data
                }
        self.addBlockToChain(newblock)
        
        return newblock
    
    def getPreviousBlock(self): # metodo para obtener el ultimo bloque de la cadena
        return self.getChain()[-1]
    
    def proofOfWork(self, previous_proof): # metodo que a partir de la prueba anterior se intenta resolver el problema y por ende devuelve este metodo la nueva prueba o nonce
        newProof = 1
        checkProof = False
        while not checkProof:
            hash_operation = hashlib.sha256(str(newProof**2 - previous_proof**2).encode()).hexdigest() # se crea un nuevo numero codificado a partir del hash256 y con base en las pruebas nueva y la anterior
            if hash_operation[:4] == '0000': # se verifica que el hash obtenido empieza con 0000
                checkProof = True # el minero a ganado o resuelto el puzzle criptografico
            else:
                newProof += 1
        
        return newProof
    
    def hashOfBlock(self, block): # Metodo que permite obtener el hash de un bloque en cuestion, nota: se transforma en una cadena json el bloque y despues se codifica y finalmente se formatea a hexadecimal el hash code
         return hashlib.sha256(json.dumps(block,sort_keys= True).encode()).hexdigest()
    
    # Metodo que sirve para validar si una cadena es valida
    def is_chain_valid(self, chain): # nota: en caso de que algun bloque no cumpla la igualdad del hash previo del bloque actual y el hash del bloque anterior o en caso de que al minar las pruebas del bloque anterior y el bloque actual no cumplen con que el hash obtenido contiene 0000 ceros a la iquierda entonces la cadena de bloques no sera valida
        previous_block = chain[0]
        for block_index in range(1,len(chain)):
            current_block = chain[block_index]
            if current_block['prevHashCode'] != self.hashOfBlock(previous_block) or hashlib.sha256(str(current_block['proof']**2 - previous_block['proof']**2).encode()).hexdigest()[:4] != '0000':
                return False
            previous_block = current_block
        return True
    
            
     
        
    
