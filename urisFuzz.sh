#!/bin/bash
# Description: Fuzzear recursos de una web.

trap ctrl_c INT

function ctrl_c(){
  echo -e "\n\nAborting...\n"
  exit 1
}

function helpPanel(){
  echo -e "\nHow to use $0?\n"
  echo -e "\t-u) URL a auditar"
  echo -e "\t-w) Dictionary a utilizar"
  echo -e "\t-h) Panel de Ayuda\n"
  echo -e "[*] Example: $0 -u http://paginita.com -w /path/dictionary\n"
  exit 1
}

function principalFuzz(){
  statusCode=$(curl -s -k -X GET "$urlMain/$ruta" -I | head -n 1 | cut -d " " -f 2)

  if [ "$statusCode" -ne "404" ]; then
    echo -e "$ruta\t[/$statusCode]"
  fi
}

declare -i paramCounter=0; while getopts "u:w:h:" arg; do
  case $arg in
    u) urlMain=$OPTARG && paramCounter+=1;;
    w) dictionaryPath=$OPTARG && paramCounter+=1;;
    h) helpPanel;;
    *) paramCounter=0;;
  esac
done

maxProcess=10
counter=0

if [ $paramCounter -ne 2 ]; then
  helpPanel
else
  echo -e "\n待ってください...\n"; sleep 2
  clear; echo "FUZZING WEB"

  while IFS= read ruta; do
    principalFuzz $ruta &
    ((counter++))
  
    if [ $counter -ge $maxProcess ]; then
      wait
      counter=0
    fi
  done < $dictionaryPath
  wait
fi
