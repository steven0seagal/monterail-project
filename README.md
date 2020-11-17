# monterail project

<p>This project is made for recruitment process for Monterail and uses Django REST FRAMEWORK</p>

<h1>Instalation process</h1>


<p>Please folow this instalation guide for this project</p>
<p>1. Clone this repository and go to decathlon folder </p>

```
https://github.com/steven0seagal/monterail-project.git
```

<p>2. Start new virtual environment and activate </p>

```
python3 -m venv venv
source venv/bin/activate
```

<p>3. Install libraries from requirements </p>

```
pip3 install -r requirements.txt
```

<p>4. Go to movies folder and migrate data</p>

```
cd proticket
python3 manage.py migrate
```
<p>5. Run server</p>

```
python3 manage.py runserver
```


<h1>Usage</h1>

<p>Below are listed all functionalities of this project and how to call them via curl command. Or you can call them using POSTMAN software and puting data to body </p>
<p>Before any testing please populate database by running command below</p>

```
curl -X GET -H 'Content-Type: application/json' http://localhost:8000/add_data/
```

<p>To view all avaiable events </p>

```
curl -X GET -H 'Content-Type: application/json' http://localhost:8000/event/
```

<p>To view single event by its id </p>

```
curl -X GET -H 'Content-Type: application/json' http://localhost:8000/event/1/
```

<p>Get info about available tickets in seletcet event by its id</p>

```
curl -X GET -H 'Content-Type: application/json' -d '{"id":"1"}' http://localhost:8000/tickets/
```

<p>Reserve ticket for 15 minutes by its event id and ticket type </p>

```
curl -X PUT -H 'Content-Type: application/json' http://localhost:8000/reserve_ticket/ -d '{"ticket_type":"PREMIUM", "event_id":1}'
```

<p>To pay for ticket by its id  </p>

```
curl -X PUT -H 'Content-Type: application/json' http://localhost:8000/payment/ -d '{"ticket_id":563}' 
```

<p>To chceck status of payed ticket by its reservation number obtained from previous method</p>

```
curl -X GET -H 'Content-Type: application/json' http://localhost:8000/status/ -d '{"reservation_number":"1LZO48KJ9N9ZB7SB84ORFWO4I"}'
```

<p>To get all statistics about tickets</p>

```
curl -X GET -H 'Content-Type: application/json' http://localhost:8000/statistics/
```