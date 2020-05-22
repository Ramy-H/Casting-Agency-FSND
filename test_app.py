import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

producer_token = {"Authorization": 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRkdnVOYm1qODlDSnlUemp0R0Z5bCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzE1MmE2NDBmYTU2MGM3NTY0NmZmMiIsImF1ZCI6IkNhcHN0b25lUHJvamVjdCIsImlhdCI6MTU5MDE3NjM5MywiZXhwIjoxNTkwMjYyNzkzLCJhenAiOiJxT0VlT0w0RTVwbnpkT0pxY0o0eHZxV1YyT1JOVU44ZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzX2RldGFpbHMiLCJnZXQ6bW92aWVzX2RldGFpbHMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.oQpSRYVgEbPcyTQU4ohSYngOx8TJYHsCfFYAIvLnYtNWD92tkCda6T20fZKQ2HQbLc9gWBM6iES0QvKqF2-G3fUTJ93Nkjr21-r6qrpv77LT8E_KTU-do_HoWBAfMNyKz4YNQsc_wbt1wT0H_nfbMpPuHshUeMI0HS3Kr4fEWPA6YzJYghAsOIKDLYLAtVkw6iTgCmZ4JxHyMHmS1w_fuFNNlGu05zx20O6kj2Y73qnhhcxan4ETL-ASvGPwvPuYdPd_keJ6ckJrla4RsBYMPdq0xAXxOa5jva2jwRkab4Ybg5j_NIMcGGTHMRSjBo_5vEunRzQLo1ixY1UnbKXZXQ'}
director_token = {"Authorization": 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRkdnVOYm1qODlDSnlUemp0R0Z5bCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzE1MWZlNDUzZTIzMGM3MWQ5MmViNiIsImF1ZCI6IkNhcHN0b25lUHJvamVjdCIsImlhdCI6MTU5MDE3Nzc0NywiZXhwIjoxNTkwMjY0MTQ3LCJhenAiOiJxT0VlT0w0RTVwbnpkT0pxY0o0eHZxV1YyT1JOVU44ZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnNfZGV0YWlscyIsImdldDptb3ZpZXNfZGV0YWlscyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.nEGpkTy-mkKL1H7sIrnwq8O4zztsZ1uqM9WDkD3dQqhIF1bvy67hLW_yPVdZGlHluSyb23ymMyQdWDah9gsu3nnNnChRCEFnl0lrWHRi5PrNAJk3HycrDig7PBd54cgEy14buzuR-8uel-ESGNzURRu4--_5SZAC6mNjmTq87x1eotoamgEkigVFd5XKld3991S4TOBNPfqlA5JVeo5wDc6y8ZBg4RWsjs518_k5IIS__RM7M-lfl8SuJvHAePlBXY-OarYbTw1-xZ5XlL_jdmBpPProaY5OvVkhc0MAty-HiOCqOoIqJhwUeVeXAZL8ANYqFfkucp8vd8C33dV59A'}
assitant_token = {"Authorization": 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRkdnVOYm1qODlDSnlUemp0R0Z5bCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzE1MTllNTgzMGE5MGM2ZmU5Yjg2YiIsImF1ZCI6IkNhcHN0b25lUHJvamVjdCIsImlhdCI6MTU5MDE3NzU4OSwiZXhwIjoxNTkwMjYzOTg5LCJhenAiOiJxT0VlT0w0RTVwbnpkT0pxY0o0eHZxV1YyT1JOVU44ZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yc19kZXRhaWxzIiwiZ2V0Om1vdmllc19kZXRhaWxzIl19.ElhDOL58HvzNtbzU26ogKxzbYoDiIdPErH4KeJ4KSBZlrFtoU2x3pKYhCby_dGr6Hz6_-64uaaEz0qOgF8cYPk3nhhalU7ZskhMmf2VPGxYc3hPuokNVbGxT_czSVeYC-iWNx4jXaw3UxxZdi0VZqRf2uVW2_Cm5wD38QcxKqCHgSTAL4sOzgWaLj880yb0mACgqeGcFlq-5eWFEaYs7JoSO6TyqqZtUboWIJvxxZcUKrwS7WLpBMQVe7YTbdvskkYdaEpJbhor1WsudWXoHlCnCjJq_RFHimbrcUYGzKn18DmfL7hpP4MYpukaHj2XyVhJKoRvr0EZRwzpRGk3epA'}


class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = 'postgres://postgres@localhost:5432/agency_test'
        # db_drop_and_create_all()
        setup_db(self.app, self.database_path)

        self.new_movie = {
            "title": "New movie",
            "date": "30-5-2020"
        }

        self.patch_movie = {
            "title": "patched movie",
            "date": "22-5-2020"
        }

        self.new_actor = {
            "name": "New actor",
            "age": "27",
            "gender": "Male"
        }
        self.patch_actor = {
            "name": "patched actor",
            "age": "30",
            "gender": "Male"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_post_a_movie(self):
        res = self.client().post('/post_movie', json=self.new_movie, headers=producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_actor(self):
        res = self.client().post('/post_actor', json=self.new_actor, headers=director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers=assitant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_all_movies_fail(self):
        res = self.client().get('/moviess', headers=assitant_token)
        self.assertEqual(res.status_code, 404)

    def test_get_all_actors(self):
        res = self.client().get('/actors', headers=assitant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_all_actors_fail(self):
        res = self.client().get('/actorss', headers=assitant_token)
        self.assertEqual(res.status_code, 404)

    def test_patch_movie(self):
        res = self.client().patch('/movies/11', json=self.patch_movie, headers=director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors(self):
        res = self.client().patch('/actors/11', json=self.patch_actor, headers=director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie_fail(self):
        res = self.client().patch('/movies/100', json=self.patch_movie, headers=director_token)
        self.assertEqual(res.status_code, 404)

    def test_patch_actors_fail(self):
        res = self.client().patch('/actors/100', json=self.patch_actor, headers=director_token)
        self.assertEqual(res.status_code, 404)

    def test_delete_actor_by_ID(self):
        res = self.client().delete('/actors/9', headers=director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/1000', headers=director_token)
        self.assertEqual(res.status_code, 404)

    def test_delete_movie_by_ID(self):
        res = self.client().delete('/movies/9', headers=producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/1000', headers=producer_token)
        self.assertEqual(res.status_code, 404)

    def test_post_a_movie_error_401(self):
        res = self.client().post('/post_movie', json=self.new_movie, headers=assitant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_a_movie_error_401(self):
        res = self.client().delete('/movies/9', headers=director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
