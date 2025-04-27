#!/usr/bin/python3

import sys, signal, string, random

ALL_CHARACTERS = string.ascii_letters + string.digits + string.punctuation

def handlerExit(sig, frame):
    print("\n\n[!] Aborting...\n")
    sys.exit(0)

signal.signal(signal.SIGINT, handlerExit)

def makePassword():
  longitudPass = int(input("Ingrese la longitud de la contraseña: "))
  password = "".join(random.choice(ALL_CHARACTERS) for i in range(longitud_pass))
  return password

def main():
    while True:
        password = makePassword()
        print(f"\n[+] La contraseña creada es:\n{password}\n")
        
        option = input("¿Desea generar otra contraseña? (s/n): ").strip().lower()
        if option != 's':
            print("\n[!] Saliendo del generador de contraseñas. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
