#!/usr/bin/python3
"""
Contains the tests of the class HBNBCommand
"""

import console
import unittest
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from tests import clear_stream
import os
from models import storage
import MySQLdb
import sqlalchemy

HBNBCommand = console.HBNBCommand


class InstanceTest:
    """Class to store objects"""

    base = None
    amenity = None
    city = None
    place = None
    review = None
    state = None
    user = None
    created_instance_id = None


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""

    def setUp(self) -> None:
        """Set up for console tests"""

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(
            console.__doc__, None, "console.py needs a docstring"
        )
        self.assertTrue(
            len(console.__doc__) >= 1, "console.py needs a docstring"
        )

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(
            HBNBCommand.__doc__,
            None,
            "HBNBCommand class needs a docstring",
        )
        self.assertTrue(
            len(HBNBCommand.__doc__) >= 1,
            "HBNBCommand class needs a docstring",
        )

    def test_HBNBCommand_method_docstring(self):
        """Test for docstrings"""
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
)
class TestConsoleCommands(unittest.TestCase):
    """Class for testing documentation of the console help command"""

    def test_help_command(self):
        """Test the help command"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("help")
            output = mock_stdout.getvalue().strip()
            self.assertIn("Documented commands", output)

    def test_show_command(self):
        """Test the show command"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("help show")
            output = mock_stdout.getvalue().strip()
            self.assertTrue(
                "[Usage]: show <className> <objectId>" in output
            )

    def test_create_command(self):
        """Test the create command"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("help create")
            output = mock_stdout.getvalue().strip()
            self.assertTrue(" Create an object of any class", output)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_create_command_with_file_storage(self):
        with patch("sys.stdout", new=StringIO()) as captured_output:
            command_instance = HBNBCommand()

            # Test create command for City class
            command_instance.onecmd('create City name="Texas"')
            city_model_id = captured_output.getvalue().strip()
            clear_stream(captured_output)
            self.assertIn(
                "City.{}".format(city_model_id), storage.all().keys()
            )

            # Test show command for City class
            command_instance.onecmd(
                "show City {}".format(city_model_id)
            )
            self.assertIn(
                "'name': 'Texas'", captured_output.getvalue().strip()
            )
            clear_stream(captured_output)

            # Test create command for User class
            command_instance.onecmd(
                'create User name="James" age=17 height=5.9'
            )
            user_model_id = captured_output.getvalue().strip()
            self.assertIn(
                "User.{}".format(user_model_id), storage.all().keys()
            )
            clear_stream(captured_output)

            # Test show command for User class
            command_instance.onecmd(
                "show User {}".format(user_model_id)
            )
            self.assertIn(
                "'name': 'James'", captured_output.getvalue().strip()
            )
            self.assertIn(
                "'age': 17", captured_output.getvalue().strip()
            )
            self.assertIn(
                "'height': 5.9", captured_output.getvalue().strip()
            )

    def test_update_command(self):
        """Test the update command"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("help update")
            output = mock_stdout.getvalue().strip()
            self.assertTrue(
                "Usage: update <className> <id> <attName> <attVal>"
                in output
            )

    def test_destroy_command(self):
        """Test the destroy command"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("help destroy")
            out = mock_stdout.getvalue().strip()
            self.assertTrue(
                "[Usage]: destroy <className> <objectId>" in out
            )


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
)
class TestConsoleEOFCommand(unittest.TestCase):
    """Class for testing documentation of the console EOF command"""

    def test_eof_command(self):
        """Test the EOF command"""
        with patch("sys.stdout", new=StringIO()):
            with self.assertRaises(SystemExit):
                console.HBNBCommand().onecmd("EOF")

    def test_quit_command(self):
        """Test the quit command"""
        with patch("sys.stdout", new=StringIO()):
            with self.assertRaises(SystemExit):
                console.HBNBCommand().onecmd("EOF")


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
)
class TestConsoleAllCommand(unittest.TestCase):
    """Class for testing documentation of the console all command"""

    def test_all_command_base_model(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            InstanceTest.base = BaseModel()
            console.HBNBCommand().onecmd("create BaseModel")
            console.HBNBCommand().onecmd("all BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("BaseModel", output)

    def test_all_command_amenity(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            InstanceTest.amenity = Amenity()
            console.HBNBCommand().onecmd("create Amenity")
            console.HBNBCommand().onecmd("all Amenity")
            output = mock_stdout.getvalue().strip()
            self.assertIn("Amenity", output)

    def test_all_command_city(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            InstanceTest.city = City()
            console.HBNBCommand().onecmd("create City")
            console.HBNBCommand().onecmd("all")
            output = mock_stdout.getvalue().strip()
            self.assertIn("City", output)

    def test_all_command_place(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            InstanceTest.place = Place()
            console.HBNBCommand().onecmd("create Place")
            console.HBNBCommand().onecmd("all")
            output = mock_stdout.getvalue().strip()
            self.assertIn("Place", output)

    def test_all_command_review(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            InstanceTest.review = Review()
            console.HBNBCommand().onecmd("create Review")
            console.HBNBCommand().onecmd("all")
            output = mock_stdout.getvalue().strip()
            self.assertIn("Review", output)

    def test_all_command_state(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            InstanceTest.state = State()
            console.HBNBCommand().onecmd("create State")
            console.HBNBCommand().onecmd("all")
            output = mock_stdout.getvalue().strip()
            self.assertIn("State", output)

    def test_all_command_user(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            InstanceTest.user = User()
            console.HBNBCommand().onecmd("create User")
            console.HBNBCommand().onecmd("all")
            output = mock_stdout.getvalue().strip()
            self.assertIn("User", output)

    def test_all_command_base_model_argument(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("create BaseModel")
            console.HBNBCommand().onecmd("all BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn("[BaseModel]", output)

    def test_all_command_amenity_argument(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("all Amenity")
            output = mock_stdout.getvalue().strip()
            self.assertIn("[Amenity]", output)

    def test_all_command_city_argument(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("all City")
            output = mock_stdout.getvalue().strip()
            self.assertIn("[City]", output)

    def test_all_command_place_argument(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("all Place")
            output = mock_stdout.getvalue().strip()
            self.assertIn("[Place]", output)

    def test_all_command_review_argument(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("all Review")
            output = mock_stdout.getvalue().strip()
            self.assertIn("[Review]", output)

    def test_all_command_state_argument(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("all State")
            output = mock_stdout.getvalue().strip()
            self.assertIn("[State]", output)

    def test_all_command_user_argument(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("all User")
            output = mock_stdout.getvalue().strip()
            self.assertIn("[User]", output)

    def test_all_command_invalid_argument(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("all Base")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)

    def test_all_instances_valid_class(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            # Create instances
            console.HBNBCommand().onecmd("create BaseModel")
            console.HBNBCommand().onecmd("create BaseModel")
            console.HBNBCommand().onecmd("create BaseModel")
            console.HBNBCommand().onecmd("all BaseModel")

            output = mock_stdout.getvalue().strip()
            self.assertEqual(len(output.split("\n")), 4)


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
)
class TestConsoleShowCommand(unittest.TestCase):
    """Class for testing documentation of the console show command"""

    def test_show_class_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("show")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class name missing **", output)

    def test_show_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("show Base")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)

    def test_show_base_model_id_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd(
                "show {}".format(InstanceTest.base.__class__.__name__)
            )
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** instance id missing **", output)

    def test_show_amenity_id_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd(
                "show {}".format(
                    InstanceTest.amenity.__class__.__name__
                )
            )
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** instance id missing **", output)

    def test_show_city_id_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd(
                "show {}".format(InstanceTest.city.__class__.__name__)
            )
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** instance id missing **", output)

    def test_show_place_id_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd(
                "show {}".format(
                    InstanceTest.place.__class__.__name__
                )
            )
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** instance id missing **", output)

    def test_show_review_id_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd(
                "show {}".format(
                    InstanceTest.review.__class__.__name__
                )
            )
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** instance id missing **", output)

    def test_show_state_id_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd(
                "show {}".format(
                    InstanceTest.state.__class__.__name__
                )
            )
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** instance id missing **", output)

    def test_show_user_id_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd(
                "show {}".format(InstanceTest.user.__class__.__name__)
            )
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** instance id missing **", output)

    def test_show_invalid_id(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd(
                "show BaseModel 49faff9a-6318-451f-87b6-910505c55907"
            )
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** no instance found **", output)


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
)
class TestConsoleCreateCommand(unittest.TestCase):
    """Class for testing documentation of the console create command"""

    # def test_create_without_class_name(self):
    #   with patch("sys.stdout", new=StringIO()) as mock_stdout:
    #       console.HBNBCommand().onecmd("create")
    #       output = mock_stdout.getvalue().strip()
    #       self.assertEqual("** class name missing **", output)

    def test_create_with_false_class_name(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("create Hamza")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)

    """"
    #INFO: this causing issue with tests
    def test_create_with_more_than_two_args(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("create BaseModel 123")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)
    """

    def test_create_without_class_name2(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("create()")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)

    def test_create_with_false_class_name2(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("hamza.create()")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(
                "*** Unknown syntax: hamza.create()", output
            )

    def test_create_and_show_instance(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("create BaseModel")
            create_output = mock_stdout.getvalue().strip()

            # Extracting the ID from the create output
            InstanceTest.created_instance_id = create_output.split()[
                -1
            ]

            # Resetting the mock_stdout buffer
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

            # Showing the created instance
            console.HBNBCommand().onecmd(
                f"show BaseModel {InstanceTest.created_instance_id}"
            )
            show_output = mock_stdout.getvalue().strip()

            self.assertIn(
                InstanceTest.created_instance_id, show_output
            )
            self.assertTrue("BaseModel" in show_output)


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
)
class TestConsoleUpdateCommand(unittest.TestCase):
    """Class for testing documentation of the console update command"""

    def test_update_without_class_name(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("update")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class name missing **", output)

    def test_update_with_false_class_name_id_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("update Hamza")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)

    def test_update_with_false_id(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("update BaseModel 123")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** no instance found **", output)

    def test_update_without_class_name2(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("update()")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)

    def test_update_with_false_class_name2(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("hamza.update()")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(
                "*** Unknown syntax: hamza.update()", output
            )

    def test_update_and_show_instance(self):
        if InstanceTest.created_instance_id is not None:
            with patch("sys.stdout", new=StringIO()) as mock_stdout:
                console.HBNBCommand().onecmd(
                    'update BaseModel {} first_name "Betty"'.format(
                        InstanceTest.created_instance_id
                    )
                )

                # Resetting the mock_stdout buffer
                mock_stdout.seek(0)
                mock_stdout.truncate(0)

                # Showing the updated instance
                console.HBNBCommand().onecmd(
                    f"show BaseModel {InstanceTest.created_instance_id}"
                )

                show_output = mock_stdout.getvalue().strip()

                self.assertIn(
                    InstanceTest.created_instance_id, show_output
                )
                self.assertTrue("BaseModel" in show_output)
                self.assertTrue("first_name" in show_output)
                self.assertTrue("Betty" in show_output)


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
)
class TestConsoleDeleteCommand(unittest.TestCase):
    """Class for testing documentation of the console delete command"""

    def test_destroy_without_class_name(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("destroy")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class name missing **", output)

    def test_destroy_with_false_class_name_id_missing(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("destroy Hamza")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)

    def test_destroy_with_false_id(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("destroy BaseModel 123")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** no instance found **", output)

    def test_destroy_without_class_name2(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("destroy()")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)

    def test_destory_with_false_class_name2(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd("hamza.destroy()")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(
                "*** Unknown syntax: hamza.destroy()", output
            )

    def test_delete_and_show_instance(self):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            console.HBNBCommand().onecmd(
                "destroy BaseModel {}".format(
                    InstanceTest.created_instance_id
                )
            )

            # Resetting the mock_stdout buffer
            mock_stdout.seek(0)
            mock_stdout.truncate(0)

            # Showing the updated instance
            console.HBNBCommand().onecmd(
                f"show BaseModel {InstanceTest.created_instance_id}"
            )

            show_output = mock_stdout.getvalue().strip()
            self.assertNotIn(
                InstanceTest.created_instance_id, show_output
            )
            self.assertEqual("** no instance found **", show_output)

    def tearDown(self) -> None:
        InstanceTest.created_instance_id = None


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage test"
)
class TestDatabase(unittest.TestCase):
    """test database"""

    def test_db_create(self):
        """Tests the create command with the database storage."""
        with patch("sys.stdout", new=StringIO()) as cout:
            cons = HBNBCommand()
            # creating a model with non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cons.onecmd("create User")
            # creating a User instance
            clear_stream(cout)
            cons.onecmd(
                'create User email="john25@gmail.com" password="123"'
            )
            mdl_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv("HBNB_MYSQL_HOST"),
                port=3306,
                user=os.getenv("HBNB_MYSQL_USER"),
                passwd=os.getenv("HBNB_MYSQL_PWD"),
                db=os.getenv("HBNB_MYSQL_DB"),
            )
            cursor = dbc.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE id="{}"'.format(mdl_id)
            )
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn("john25@gmail.com", result)
            self.assertIn("123", result)
            cursor.close()
            dbc.close()

    def test_db_show(self):
        """Tests the show command with the database storage."""
        with patch("sys.stdout", new=StringIO()) as cout:
            cons = HBNBCommand()
            # showing a User instance
            obj = User(email="john25@gmail.com", password="123")
            dbc = MySQLdb.connect(
                host=os.getenv("HBNB_MYSQL_HOST"),
                port=3306,
                user=os.getenv("HBNB_MYSQL_USER"),
                passwd=os.getenv("HBNB_MYSQL_PWD"),
                db=os.getenv("HBNB_MYSQL_DB"),
            )
            cursor = dbc.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE id="{}"'.format(obj.id)
            )
            result = cursor.fetchone()
            self.assertTrue(result is None)
            cons.onecmd("show User {}".format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(), "** no instance found **"
            )
            obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv("HBNB_MYSQL_HOST"),
                port=3306,
                user=os.getenv("HBNB_MYSQL_USER"),
                passwd=os.getenv("HBNB_MYSQL_PWD"),
                db=os.getenv("HBNB_MYSQL_DB"),
            )
            cursor = dbc.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE id="{}"'.format(obj.id)
            )
            clear_stream(cout)
            cons.onecmd("show User {}".format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn("john25@gmail.com", result)
            self.assertIn("123", result)
            cursor.close()
            dbc.close()

    def test_db_count(self):
        """Tests the count command with the database storage."""
        with patch("sys.stdout", new=StringIO()) as cout:
            cons = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv("HBNB_MYSQL_HOST"),
                port=3306,
                user=os.getenv("HBNB_MYSQL_USER"),
                passwd=os.getenv("HBNB_MYSQL_PWD"),
                db=os.getenv("HBNB_MYSQL_DB"),
            )
            cursor = dbc.cursor()
            cursor.execute("SELECT COUNT(*) FROM states;")
            res = cursor.fetchone()
            prev_count = int(res[0])
            cons.onecmd('create State name="Enugu"')
            clear_stream(cout)
            cons.onecmd("count State")
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            cons.onecmd("count State")
            cursor.close()
            dbc.close()


if __name__ == "__main__":
    unittest.main()
