import unittest
import os
from data import Data
from rooms import Rooms


class RoomTest(unittest.TestCase):
    """Test for rooms (living spaces and Office spaces)"""

    def setUp(self):
        self.data = Data()

    def test_create_rooms(self):
        """
        Create test database and assert that there are no rooms in that table.

        Create 3 rooms and assert that there are now 3 rooms.

        Assert that woodwing is the first room in the list of rooms.

        Assert that woodwing is of type living space (L)
        """
        all_rooms = self.data.fetch_data("rooms", False)
        self.assertEqual(0, len(all_rooms))

        new_rooms = self.data.create_living_spaces(
            ['woodwing', 'westwing', 'eastwing'])
        self.assertEqual('New rooms succesfully created', new_rooms)

        all_rooms = self.data.fetch_data("rooms", False)
        self.assertEqual(3, len(all_rooms))
        self.assertTrue('woodwing' in all_rooms[0])
        self.assertTrue('L' in all_rooms[0])

    def test_duplicate_room_error(self):
        """
        Assert that an error is thrown on creating duplicate rooms
        """
        self.data.create_living_spaces(['woodwing'])

        with self.assertRaises(ValueError) as e:
            self.data.create_living_spaces(['woodwing'])
            self.assertEqual(
                'Duplicate entries: A room already exist with provided name',
                e.exception)

    def test_room_allocations(self):
        """
        Test that a user can view a list of room allocations
        """
        self.data.create_office_spaces(['midgar'])
        self.data.create_living_spaces(['woodwing'])

        rooms = Rooms()
        rooms.room_allocations({'--o': 'allocations.txt'})
        with open('allocations.txt') as f:
            lines = f.readlines()
            self.assertTrue('no office spaces are occupied\n' in lines)
            self.assertTrue('no living spaces are occupied' in lines)
        os.remove('allocations.txt')

        self.data.create_fellow("John", "Kariuki", "y")
        self.data.create_fellow("Penny", "Wanjiru", "y")
        self.data.create_fellow("Blue", "October", "n")

        self.data.create_staff("June", "Bag")
        self.data.create_staff("Blue", "October")

        rooms.room_allocations({'--o': 'allocations.txt'})
        self.assertTrue(os.path.exists('allocations.txt'))

        with open('allocations.txt') as f:
            lines = f.readlines()
            self.assertTrue('John Kariuki, Penny Wanjiru\n' in lines)
            self.assertTrue('Blue October, June Bag\n' in lines)
        os.remove('allocations.txt')

    def test_room_allocation(self):
        """
        Test that a user can view the allocation of a particular room
        """
        self.data.create_office_spaces(['midgar'])
        self.data.create_living_spaces(['woodwing'])

        self.data.create_fellow("John", "Kariuki", "y")
        self.data.create_fellow("Penny", "Wanjiru", "y")
        self.data.create_fellow("Blue", "October", "n")

        self.data.create_staff("June", "Bag")
        self.data.create_staff("Blue", "October")

        rooms = Rooms()
        rooms.room_allocation({'--o': 'y', '<room_name>': 'midgar'})
        self.assertTrue(os.path.exists('midgar.txt'))
        with open('midgar.txt') as f:
            lines = f.readlines()
            self.assertTrue('MIDGAR (OFFICE SPACE)\n' in lines)
            self.assertTrue('June Bag, Blue October' in lines)
        os.remove('midgar.txt')

        invalid_room = rooms.room_allocation(
            {'--o': 'y', '<room_name>': 'randomnam3'})
        self.assertEqual(
            'No room exists in amity with that name. please try again',
            invalid_room)

        self.data.create_living_spaces(['bluewing'])
        rooms.room_allocation(
            {'--o': 'y', '<room_name>': 'bluewing'})
        with open('bluewing.txt') as f:
            lines = f.readlines()
            self.assertTrue('bluewing has no occupants' in lines)
        os.remove('bluewing.txt')

        rooms.room_allocation({'--o': 'y', '<room_name>': 'woodwing'})
        self.assertTrue(os.path.exists('woodwing.txt'))
        with open('woodwing.txt') as f:
            lines = f.readlines()
            self.assertTrue('WOODWING (LIVING SPACE)\n' in lines)
            self.assertTrue('John Kariuki, Penny Wanjiru' in lines)
        os.remove('woodwing.txt')

    def tearDown(self):
        """Delete the test database"""
        if os.path.exists('room_alloc.db'):
            os.remove('room_alloc.db')

if __name__ == '__main__':
    unittest.main()
