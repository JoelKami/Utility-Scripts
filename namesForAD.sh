#!/bin/bash
# Description: programa para formar nombres de usuarios de AD a partir de una lista de nombres y apellidos.

function helpPannel() {
	echo -e "\nHow to use $0?\n"
	echo -e "\tDado el nombre: Pedro Alonso.\n"
	echo -e "\t\tf) Indicar el formato de nombres."
	echo -e "\t\t\t[1] Formato: pAlonso\n"
	echo -e "\t\t\t[2] Formato: palonso\n"
	echo -e "\t\t\t[3] Formato: p.alonso\n"

	echo -e "\tIndicar el diccionario de nombres de acuerdo al formato Pedro Alonso.\n"
	echo -e "\t\td) Ruta del diccionario de nombres\n"

	echo -e "\tLlamar a este pannel de ayuda\n"
	echo -e "\t\th) Llamar a helpPannel\n"

	echo -e "Ejemplo: $0 -f 1 -d ./users"
	exit 1
}


function format1() {
    while IFS= read name; do
		namesMinus=$(echo $name | tr '[A-Z]' '[a-z]')
		firstNameLetter=$(echo $namesMinus | cut -d " " -f1 | head -c 1)
		lastName=$(echo $namesMinus | awk '{print $2}' | sed -e "s/\b\(.\)/\u\1/g")
		echo $firstNameLetter$lastName >> usersFormat1
	done < $routeFile
	echo "File usersFormat1 creado"
}

function format2() {
    while IFS= read name; do
        namesMinus=$(echo $name | tr '[A-Z]' '[a-z]')
        firstNameLetter=$(echo $namesMinus | cut -d " " -f1 | head -c 1)
        lastName=$(echo $namesMinus | awk '{print $2}')
        echo $firstNameLetter$lastName >> usersFormat2
    done < $routeFile
    echo "File usersFormat2 creado"
}

function format3() {
	while IFS= read name; do
        namesMinus=$(echo $name | tr '[A-Z]' '[a-z]')
        firstNameLetter=$(echo $namesMinus | cut -d " " -f1 | head -c 1)
        lastName=$(echo $namesMinus | awk '{print $2}')
        echo $firstNameLetter.$lastName >> usersFormat3
    done < $routeFile
    echo "File usersFormat3 creado"
}

declare -i param=0; while getopts ":f:d:h:" arg; do
	case $arg in
		f) format=$OPTARG && param+=1 ;;
		d) routeFile=$OPTARG && param+=1 ;;
		h) helpPannel ;;
		*) param=0 ;;
	esac
done

if [ $param -eq 0 ]; then
	helpPannel
fi

if [ $param -eq 2 ]; then
	case $format in
		1) format1 $routeFile ;;
		2) format2 $routeFile ;;
		3) format3 $routeFile ;;
		*) helpPannel ;;
	esac
fi
