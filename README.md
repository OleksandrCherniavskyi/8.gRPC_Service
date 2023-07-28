
## Description 
This project is a service that allows you to add items to a database and search for similar items. 

### The main features of the service
- Add Item 
- Search Items
- Get Search Results
- When you add a new item to the database, you can see the coefficient of how similar it is to other items in the database.



The service is based on gRPC and is developed in Python. 
The service consists of two parts - the ```server``` and the```client```.
The database used is PostgreSQL because it is a good scalable database.



# To run project with Docker Desktop

- Clone repository
- ```git clone https://github.com/OleksandrCherniavskyi/8.gRPC_Service.git```
- ```docker-compose up -d```


- In Docker Desktop run ```app-1``` and ```db-1```container
![img.png](img.png)
- `some time you need wait 1 min and manually start app-1`

- open terminal in ```app-1``` container

- run ```python similarity_client.py```
![img_1.png](img_1.png)
