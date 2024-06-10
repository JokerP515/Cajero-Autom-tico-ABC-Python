from abc import ABC, abstractmethod
#https://python-course.eu/oop/the-abc-of-abstract-base-classes.php
#https://ellibrodepython.com/abstract-base-class

"""
Simplemente definen una forma de crear interfaces (a través de metaclases) en los que se definen unos métodos 
(pero no se implementan) y donde se fuerza a las clases que usan ese interfaz a implementar los métodos. 
Veamos unos ejemplos.
"""
"""
Los interfaces formales pueden ser definidos en Python 
utilizando el módulo por defecto llamado ABC (Abstract Base Classes).
"""
#Interfaz Command. En esencia, una interfaz en Java define un conjunto de métodos que deben ser implementados por cualquier clase que implemente esa interfaz

 
# Interfaz Command
class Command(ABC):
    @abstractmethod
    def ejecutar(self):
        pass



# Comandos concretos
class RetirarDinero(Command):
    def __init__(self, cajero, monto):
        self.cajero = cajero
        self.monto = monto
        
    def ejecutar(self):
        self.cajero.retirar_dinero(self.monto)

class ConsultarSaldo(Command):
    def __init__(self, cajero):
        self.cajero = cajero

    def ejecutar(self):
        self.cajero.consultar_saldo()


# Ingresar dinero al CajeroAutomatico
class IngresarDinero(Command):
    def __init__(self, cajero):
        self.cajero = cajero
    def ejecutar(self):
        self.cajero.ingresar_billetes()


# Receptor
class CajeroAutomatico:
    def __init__(self):
        #self.saldo = saldo_inicial
        self.billetes_disp = []
        self.saldo = 0
        
    def ingresar_billetes(self):
        billete = int(input("Ingrese el billete (o 0 para dejar de ingresar): "))
        if(billete % 10 == 0):
            self.billetes_disp.append(billete)
        else:
            print("Ingresa un billete que sea multiplo de 10")
        while billete != 0:
            billete = int(input("Ingrese el billete (o 0 para dejar de ingresar): "))
            if(billete % 10 == 0):
                self.billetes_disp.append(billete)
            else:
                print("Ingresa un billete que sea multiplo de 10")
        self.saldo = sum(self.billetes_disp)

    def retirar_dinero(self, monto):
        
        if monto <= self.saldo:
            billetesAux = self.calcular_billetes(monto)
            if billetesAux:
                print("Retirando billetes: ")
                for billete in billetesAux:
                    self.billetes_disp.remove(billete)
                    print(f"${billete}, ")
                
                self.saldo -= monto
                print(f"Se ha retirado ${monto}")
                    
            #self.saldo -= monto
            #print(f"Se han retirado ${monto}")
        else:
            print("Saldo insuficiente")
            
    def calcular_billetes(self, monto):
        billetesAux = []
        for billete in sorted(self.billetes_disp, reverse=True):
            cantidad = min(self.billetes_disp.count(billete), monto // billete)
            for i in range(cantidad):
                billetesAux.append(billete)
                monto -= billete
                if monto == 0:
                    break
            if monto == 0:
                break
            
        if monto == 0:
            return billetesAux
        else:
            return []

    def consultar_saldo(self):
        self.saldo = sum(self.billetes_disp)
        print(f"El saldo actual es ${self.saldo}")

# Invoker
class TerminalCajero:
    def __init__(self):
        self.comando = None

    def set_comando(self, comando):
        self.comando = comando

    def ejecutar_comando(self):
        if self.comando:
            self.comando.ejecutar()
        else:
            print("No se ha asignado ningún comando.")

# Uso
if __name__ == "__main__":
    
    cajero = CajeroAutomatico()
    terminal = TerminalCajero()
    
    #Insertar Billetes al cajero
    terminal.set_comando(IngresarDinero(cajero))
    terminal.ejecutar_comando()

    # Retirar dinero
    terminal.set_comando(RetirarDinero(cajero, 200))
    terminal.ejecutar_comando()
    
    # Consultar saldo
    terminal.set_comando(ConsultarSaldo(cajero))
    terminal.ejecutar_comando()

    
    
