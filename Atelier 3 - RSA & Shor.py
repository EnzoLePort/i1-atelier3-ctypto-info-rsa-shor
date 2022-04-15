import math
from operator import mod
import random

print('Atelier 3 Crypto & Info Quantique - RSA & Shor')
print("by Romain & Enzo.")

### encrypt it : c = m^e mod n ###
### de crypt it  : m = c^d mod n ###
message = "LABEILLEBUTINE"

class RSAGenerator :

    lowerPrimeInRange = 1
    higherPrimeInRange = 100
    primeList = []

    p = 3       # a Prime number
    q = 11      # a Prime number
    n = p*q     # a part of the public & private key
    m = (p-1)*(q-1)

    ### if : PGCD(e, m) == 1 ###
    ### foundE(m,primeList) return e ###
    e = 3

    ### d = (1 + entier * m)/e ###
    ### (1 + entier * m)%e == 0 ###
    d = 0

    aphabetToIntDictionary = {}
    upperAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self) :
        self.primesInRange(self.lowerPrimeInRange, self.higherPrimeInRange)
        self.foundE()
        self.foundD()
        self.aphabetToInt()

    def primesInRange(self, min, max):
        self.primeList = []
        for n in range(min, max):
            isPrime = True

            for num in range(2, n):
                if n % num == 0:
                    isPrime = False

            if isPrime:
                self.primeList.append(n)

    def foundE(self) :
        for prime in self.primeList :
            if (self.m%prime != 0) :
                self.e = prime
                break

    def foundD(self) :
        for entier in range(self.lowerPrimeInRange,self.higherPrimeInRange) :
            dTest = (1 + entier * self.m)
            if(dTest%self.e == 0) :
                self.d = int(dTest/self.e)
                break

    def aphabetToInt(self) :
        _aphabetToIntDictionary = {}
        for index, letter in enumerate(self.upperAlphabet) :
            _aphabetToIntDictionary[letter] = index
        self.aphabetToIntDictionary = _aphabetToIntDictionary

    ### encrypt it : c = m^e % n ###
    def encrypt(self,message) :
        crypt = []
        for letter in message :
            cryptedItem = math.pow(self.aphabetToIntDictionary[letter], self.e) % self.n
            crypt.append(cryptedItem)
        return crypt

    ### de crypt it  : m = c^d % n ###
    def decrypt(self, cryptedMessage):
        decryptedList = []
        message = ""

        for c in cryptedMessage :
            decryptedItem = math.pow(c, self.d) % self.n
            decryptedList.append(decryptedItem)

            for letter, index in self.aphabetToIntDictionary.items() :
                if index == decryptedItem :
                    message += letter

        print(decryptedList)
        return message

    def printAll(self):
        print('p :', self.p)
        print('q :', self.q)
        print('m :', self.m)
        print('n :', self.n)
        print('e :', self.e)
        print('d :', self.d)

    def printKeys(self) :
        print('Public Key : (%s,%s)' % (self.n,self.e))
        print('Private Key : (%s,%s)' % (self.n,self.d))

class Shor :

    n = 143

    ### a < n ; a % 2 !=0 ; a can't be a n^2 ###
    a = 3 # 5

    ### a^r % n = 1 ; r % 2 != 0 ###
    r = 15 # 20

    # pgcd

    def __init__(self) :
        self.foundAR()

    def foundAR(self) :
        self.foundAWithAscendantMethod(1)
        self.foundR()

        while self.r % 2 != 0 :
            self.a += 1
            self.foundAWithAscendantMethod(self.a)
            self.foundR()

    def foundAWithDescendantMethod(self) :
        _a = self.n - 1
        search = True
        while search :
            if _a % 2 != 0 :
                root_a = math.sqrt(_a)
                if int(root_a + 0.9) ** 2 != _a:
                    self.a = _a
                    search = False
                    break
            _a -= 1

    def foundAWithAscendantMethod(self, minA) :
        for _a in range(minA,self.n) :
            if _a % 2 != 0 :
                root_a = math.sqrt(_a)
                if int(root_a + 0.9) ** 2 != _a:
                    self.a = _a
                    break

    ### a^r % n = 1 ###
    def foundR(self) :
        _r = 1
        search = True
        while search :
            if math.pow(self.a,_r) % self.n == 1 :
                self.r = _r
                search = False
                break
            _r += 1

    def PGCD(self, a,b) :
        r = a%b
        if 0 == r :
            return b
        else :
            return self.PGCD(b,r)

    def printAll(self):
        print('a :', self.a)
        print('r :', self.r)
        print('n :', self.n)


if __name__ == "__main__":

    print('RSA PART :')

    myRSA = RSAGenerator()
    myRSA.printAll()
    myRSA.printKeys()

    print(myRSA.aphabetToIntDictionary)

    cryptedMessage = myRSA.encrypt(message)
    print(cryptedMessage)

    decryptedMessage = myRSA.decrypt(cryptedMessage)
    print(decryptedMessage)

    print('#####')
    print('SHOR PART :')
    
    myShor = Shor()
    myShor.printAll()

    pgcd1 = myShor.PGCD(math.pow(myShor.a,myShor.r/2)-1,myShor.n)
    print(pgcd1)
    pgcd2 = myShor.PGCD(math.pow(myShor.a,myShor.r/2)+1,myShor.n)
    print(pgcd2)
