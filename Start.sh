#!/bin/bash
X=$1
#env=source ~/VirtualEnvironments/Python3.12_Venvs/WebDemo_temp/bin/activate

if [ $X == '1' ]; then
	echo $X
	source ~/VirtualEnvironments/Python3.12_Venvs/WebDemo_temp/bin/activate
	python manage.py runserver
elif [ $X == '2' ]; then 
	echo $X
	source ~/VirtualEnvironments/Python3.12_Venvs/WebDemo_temp/bin/activate 
	daphne -p 8001 auth.asgi:application
elif [ $X == '3' ]; then
	echo $X
	source ~/VirtualEnvironments/Python3.12_Venvs/WebDemo_temp/bin/activate
	sudo service redis-server start
fi	
