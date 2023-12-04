import unittest
from pymongo import MongoClient

# Assuming you have these classes or functions defined somewhere
from db_types import ExtendedUser, User, Topic
from connection import (
    client,
    staging,
    get_users,
    get_user_by_username,
    create_user,
    add_keyword_to_user,
    unexpand_keyword_for_user,
    remove_keyword_from_user,
    rebuild_sample_users_db,
    rebuild_keyword_expansion_db,
)


class TestMongoDBFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # tests are done on staging
        cls.client = client
        cls.db = staging

    def setUp(cls):
        # clear the users before each test
        print("Resetting DB")
        cls.db.users.delete_many({})
        # refresh the keyword expansions before each test
        rebuild_keyword_expansion_db(cls.db)

    def test_get_users(self):
        # should start empty
        users = get_users(self.db, aggregate=False)
        self.assertIsInstance(users, list)
        self.assertEqual(len(users), 0)

        # add some users
        rebuild_sample_users_db()
        users = get_users(self.db, aggregate=False)
        self.assertIsInstance(users, list)
        self.assertEqual(len(users), 2)

    def test_get_user_by_username(self):
        rebuild_sample_users_db()
        user = get_user_by_username(self.db, "123madskillz")
        self.assertIsNotNone(user)  # Ensure that a user is returned
        self.assertEqual(
            user["reddit_username"], "123madskillz"
        )  # Check if the username is correct

    def test_create_user(self):
        create_user(
            self.db, "new_user", True, [{"topic_name": "python", "is_expanded": True}]
        )

        user = get_user_by_username(self.db, "new_user")

        self.assertIsNotNone(user)  # Check that the user was created
        self.assertEqual(user["reddit_username"], "new_user")  # Verify username
        # check if public
        self.assertEqual(user["is_public"], True)
        # check if keyword is python
        self.assertEqual(user["subscribed_keywords"][0]["topic_name"], "python")
        # check if keyword is expanded
        self.assertEqual(user["subscribed_keywords"][0]["is_expanded"], True)

    def test_add_keyword_to_user(self):
        create_user(
            self.db, "new_user", True, [{"topic_name": "python", "is_expanded": True}]
        )

        add_keyword_to_user(self.db, "new_user", "ml")
        user = get_user_by_username(self.db, "new_user")
        self.assertIn(
            {"topic_name": "ml", "is_expanded": True}, user["subscribed_keywords"]
        )

    def test_unexpand_keyword_for_user(self):
        # Test the unexpand_keyword_for_user function
        create_user(
            self.db, "new_user", True, [{"topic_name": "python", "is_expanded": True}]
        )
        unexpand_keyword_for_user(self.db, "new_user", "python")
        user = get_user_by_username(self.db, "new_user")
        self.assertTrue(
            any(
                keyword["topic_name"] == "python" and not keyword["is_expanded"]
                for keyword in user["subscribed_keywords"]
            )
        )

        # test the unexpand keyword function if the keyword is already unexpanded
        create_user(
            self.db,
            "newwer_user",
            True,
            [{"topic_name": "python", "is_expanded": False}],
        )
        unexpand_keyword_for_user(self.db, "newwer_user", "python")
        user = get_user_by_username(self.db, "newwer_user")
        self.assertTrue(
            any(
                keyword["topic_name"] == "python" and not keyword["is_expanded"]
                for keyword in user["subscribed_keywords"]
            )
        )

    def test_remove_keyword_from_user(self):
        create_user(
            self.db,
            "test_user",
            True,
            [
                {"topic_name": "python", "is_expanded": False},
                {"topic_name": "javascript", "is_expanded": False},
            ],
        )
        remove_keyword_from_user(self.db, "test_user", "python")
        user = get_user_by_username(self.db, "test_user")
        self.assertNotIn(
            "python",
            [keyword["topic_name"] for keyword in user["subscribed_keywords"]],
        )
        self.assertIn(
            "javascript",
            [keyword["topic_name"] for keyword in user["subscribed_keywords"]],
        )

    @classmethod
    def tearDownClass(cls):
        # Clean up operations after all tests have run
        # Close the MongoDB connection
        cls.client.close()


if __name__ == "__main__":
    unittest.main()
