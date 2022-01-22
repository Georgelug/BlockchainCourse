# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 13:43:26 2022

@author: Jorge L. Esparza
"""

# Modulo 1 - creando una cadena de bloques


# modulos
import datetime # modulo que se va utilizar para las datestamp
import hashlib # modulo para aplicar los algoritmos de hashing
import json # modulo para crear ficheros json para codificar y empaquetar en json las cadenas de bloque
from flask import Flask, jsonify # modulo del cual se importa el constructor y jsonify para transformar la peticion en json

# =============================================================================
# Estrucutra de la cadena bloques
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

# =============================================================================
# Aplicacion
# =============================================================================

#se inicializa la  app web
app = Flask(__name__)
app.config['JSONFY_PRETTYPRINT_REGULAR'] = False 
# se inicializa la blockchain
blockchain = Blockchain()     

#funcion que sirve para minar y por ende agregar un nuevo bloque a la cadena por medio de peticiones http usando FLASK
@app.route('/mine_block',methods = ['GET'])# direccion de URL la cual invoca una funcion , y que esta a su vez sera utilizando el metodo get que sirve para obtener informacion con ayuda postman
def mine_block():
    previous_block = blockchain.getPreviousBlock()
    previous_proof = previous_block['proof']
    newProof = blockchain.proofOfWork(previous_proof)
    previous_hash = blockchain.hashOfBlock(previous_block)
    block = blockchain.create_block(newProof, previous_hash)
    response = {
            'message' : 'A new block has been mined successfully',
            'index' : block['index'],
            'timestamp' : block['timestamp'],
            'proof' : block['proof'],
            'prevHashCode' : block['prevHashCode'],
            'HashCode' : blockchain.hashOfBlock(block),
        }
    return jsonify(response), 200

#Funcion que sirve para obtener y mostrar la cadena completa por medio de peticiones http usando FLASK
@app.route('/get_chain',methods = ['GET'])
def get_chain():
    response = {
           'chain' : blockchain.getChain(),
           'length': len(blockchain.getChain())
        }
    return jsonify(response), 200 # 200 es por que es un codigo que da el servidor cuando todo va ok

#Funcion que sirve para verificar si la cadena es valida o no
@app.route('/is_valid',methods = ['GET'])
def is_valid():
    response = {
           'state of the chain': 'Is valid' if blockchain.is_chain_valid(blockchain.getChain()) else " Is not valid"
        }
    return jsonify(response), 200 # 200 es por que es un codigo que da el servidor cuando todo va ok


# =============================================================================
# Ejecucion de la app
# =============================================================================
# app.run(host = '0.0.0.0', port = 5000) #se ejecuta en el host 0.0.0.0 y en el puerto 5000
app.run(host = '127.0.0.1', port = 5000) #se ejecuta en el host 0.0.0.0 y en el puerto 5000

