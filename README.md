# Casting-Agency-FSND

Casting Agency API is the Udacity Full Stack Nanodegree Capstone Project and it models a company that is responsible for creating, updating, deleting movies and actors.

It contains permissions assigned to users according to each role.
This project uses flask and postgresql for it's backend and hosted on heruko.

### Roles:
- Casting Assistant:
    - Can view actors and movies

- Casting Director:
    - All permissions a Casting Assistant has.
    - Add or delete an actor from the database.
    - Modify actors or movies

- Executive Producer
    - All permissions a Casting Director has.
    - Add or delete a movie from the database


### Deployment:
- This API is deployed on heruko with this link as its base URL: https://castingagency-fsnd.herokuapp.com/
- The Flask app used for this project consists of a simple API with three endpoints:
- `GET '/'`: This is a simple health check, which returns the response {"message":"Hello"}.
- `GET '/movies'`
    - retrieve all movies from database 
    - returning response:
    ```json
    {
      "movies": [
        {
            "date": "22-5-2020",
            "id": 1,
            "title": "New Movie"
        },
        {
            "date": "22-5-2020",
            "id": 2,
            "title": "patched movie"
        }
      ],
      "success": true
    }
    ```
    
- `GET '/actors'`
    - retrieve all actors from database 
    - returning response:
    ```json
  {
    "actors": [
        {
            "age": "27",
            "gender": "Male",
            "id": 1,
            "name": "New actor"
        },
        {
            "age": "27",
            "gender": "Male",
            "id": 2,
            "name": "ramy"
        }
    ],
    "success": true,
    "total_actors": 2
  }
    ```
    
- `POST '/post_movie'`:
    - insert movie into database 
    - returning response:
    ```json
    {
      "success": true
    }  
    ```
    
- `POST '/post_actor'`:
    - insert actor into database 
    - returning response:
    ```json
    {
      "success": true
    }    
    ```
    
- `PATCH '/actors/<actor_id>`:
    - patch actor in database 
    - returning response:
    ```json
     {
       "success": true
     }   
    ```
- `PATCH '/movies/<movie_id>'`:
    - patch movie in database 
    - returning response:
    ```json
    {
      "success": true
    }    
    ```
    
- `DELETE '/actors/<int:actor_id>'`:
    - delete actors from database 
    - returning response:
    ```json
    {
      "success": true
    }    
    ```
    
- `DELETE '/movies/<int:movie_id>'`:
    - delete movie from database 
    - returning response:
    ```json
    {
      "success": true
    }
    ```

### Getting Started:
- Installing Dependencies: <br>Follow instructions to install the latest version of python for your platform in the [here](https://docs.python.org/3/using/windows.html)

- Virtual Enviornment:<br>We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found [here](https://docs.python.org/3/library/venv.html?#module-venv)

- PIP Dependencies:<br>
After setting up the virtual environment, install dependencies by running: `pip install -r requirements.txt`

### Running server:
  First ensure that you are working in the created virtual environment.
  To run the server, execute: <br>
  `export FLASK_APP=app.py`<br>
  `export FLASK_ENV=development`<br>
  `flask run`

### Testing:

  If you only want to test the API, you can simply use the bearer tokens that existing in `test_app.py`. 
  <br> - `cd <path of the file>`
  <br> - `python test_app.py`
  <br> - It should give this response if everything went fine: <br>
  
  ```json
   ................
   ----------------------------------------------------------------------
   Ran 16 tests in 19.503s
   OK
   ```
