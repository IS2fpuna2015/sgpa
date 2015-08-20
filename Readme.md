## Requisitos:
* Postgresql-9.3
* Python 2.7
* Pip para manejar las dependencias y VirtualEnv para crear un entorno virtual para      python y los paquetes del proyecto.

> # **Nota:**
> Los paquetes de python necesarios estan en el requirements.txt

### Pasos y Comandos utiles(para distribuciones basadas en debian):
1. instalar base datos postgresql-9.3
	* sudo apt-get install postgresql-9.3
2. crear base de datos sgpa
	* sudo -u postgres createdb sgpa
3. cambiar password 'postgres' a usuario postgres
	* sudo -u postgres psql
	* ALTER USER postgres WITH PASSWORD 'postgres';
4. instalar pip
	* sudo apt-get install python-pip
5.  instalar virtualenv
	* sudo pip install virtualenv
7. crear un entorno virtual 
	* virtualenv -p python env // asegurarse de usar la version 2.7 de python
8. activar el entorno virtual
  	* source ./env/bin/activate
9. descargar el proyecto de github
	* git clone https://github.com/IS2fpuna2015/sgpa.git
10. installar los paquetes necesarios para el proyecto
	* pip install -r requirements.txt
11. crear tablas, cargar datos e iniciar el servidor 
	* ./manage.py makemigrations
	* ./manage.py migrate
	* ./manage.py loaddata datosiniciales/datos.json
	* ./manage.py runserver 



