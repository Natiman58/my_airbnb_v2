#!/usr/bin/python3
"""
    A module for the console
"""

import cmd
from models.base_model import BaseModel
from datetime import datetime
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.review import Review
import re


class HBNBCommand(cmd.Cmd):
    """
        A class representing the console
    """
    prompt = '(hbnb) '
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        "Place": Place,
        "State": State,
        "amenity": Amenity,
        "Review": Review,
        "City": City,
    }

    def do_EOF(self, arg):
        """ EOF command interpreter """
        return True

    def do_quit(self, arg):
        """ Quit command to exit the program """
        return True

    def do_create(self, arg):
        """
        Creates a new instance of the BaseModel class
        and saves it to a json file and prints the id
        """
        if len(arg) == 0:
            print("** class name missing **")
            return
        try:
            obj = eval(arg)()
            obj.save()
            print(obj.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
            prints the string representation of an instance based on
            the class name and id
        """
        from models import storage
        args = arg.split()
        if len(args) == 0:
            print("** class name missing ** ")
        elif len(args) == 1 and args[0] in self.classes:
            print("** instance id missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            key = args[0] + '.' + args[1]
            if key not in storage.all():
                print("** no instance found **")
            else:
                each_obj = storage.all()[key]
                print(each_obj)

    def do_destroy(self, arg):
        """
            deletes an instance based on calss name and id
        """
        from models import storage
        args = arg.split()
        if len(args) == 0:
            print(" ** class name missing ** ")
        elif len(args) == 1 and args[0] in self.classes:
            print("** instance id missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            key = args[0] + '.' + args[1]
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, arg):
        """
            prints all instance objs based on class name or
            'all' command
        """
        from models import storage
        obj_list = []
        if arg == "":
            all_objs = storage.all()
            for obj in all_objs.values():
                obj_dict = obj.to_dict()
                obj_dict.pop('__class__', None)
                for key, value in obj_dict.items():
                    if key in ['created_at', 'updated_at']:
                        date_format = '%Y-%m-%dT%H:%M:%S.%f'
                        obj_dict[key] = datetime.strptime(value, date_format)
                obj_name = obj.__class__.__name__
                obj_str = f"[{obj_name}] ({obj.id}) {obj_dict}"
                obj_list.append(obj_str)
            print(obj_list)
        else:
            args = arg.split()
            class_name = args[0]
            if class_name in self.classes:
                all_objs = storage.all()
                for obj in all_objs.values():
                    obj_dict = obj.to_dict()
                    obj_dict.pop('__class__', None)
                    for key, value in obj_dict.items():
                        if key in ['created_at', 'updated_at']:
                            date_format = '%Y-%m-%dT%H:%M:%S.%f'
                            date_obj = datetime.strptime(value, date_format)
                            obj_dict[key] = date_obj
                    obj_name = obj.__class__.__name__
                    obj_str = f"[{obj_name}] ({obj.id}) {obj_dict}"
                    obj_list.append(obj_str)
                print(obj_list)
            else:
                print(" ** class doesn't exist ** ")

    def do_update(self, arg):
        """
            updates the instance based on the class name and id
            by adding or updating attribute and
            save the changes to json file
        """
        from models import storage
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        if len(args) > 4:
            print("** All other arguments shouldn't be used once **")
            return
        obj_id = args[1]
        input_key = class_name + '.' + obj_id
        all_objs = storage.all()

        if input_key not in all_objs:
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print(" ** value missing ** ")
            return
        else:
            try:
                attr_name = args[2]
                attr_value_str = args[3]
                if attr_name in ['id', 'created_at', 'updated_at']:
                    print("** cannot update attribute **")
                    return
                for o in all_objs.values():
                    obj_dict = o.to_dict()
                    obj_dict.pop('__class__', None)
                    for key, value in obj_dict.items():
                        if key in ['created_at', 'updated_at']:
                            date_format = '%Y-%m-%dT%H:%M:%S.%f'
                            date_obj = datetime.strptime(value, date_format)
                            obj_dict[key] = date_obj

                obj = all_objs[input_key]
                setattr(obj, attr_name, attr_value_str)
                obj.save()
            except ValueError:
                pass

    def do_User(self, arg):
        """
            handle the user commands
        """
        args = arg.split('.')
        if args[1] == 'all()':
            return User.all(self)
        if args[1] == 'count()':
            return User.count(self)
        try:
            # regx pattern to match uuid format
            pattern = r'([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})'
            match = re.search(pattern, args[1])
            if match:
                id = match.group()
                if args[1] == f'show("{id}")':
                    return User.show(self, id)
                if args[1] == f'destroy("{id}")':
                    return User.destroy(self, id)

                #  section for updating using attribute and value
                # remove white space around
                attr = arg.split(',')[1].strip()[1:-1]

                # to remove the ')' in the end
                value = arg.split(',')[2].strip()[: -1]
                if(args[1] == f'update("{id}", "{attr}", {value})'):
                    return User.update(self, id, attr, value)

                #  section for updating using id and dict input
                dict_input = arg.split('{')[1].strip()[:-1]
                full_dict = '{' + dict_input
                if (args[1] == f'update("{id}", {full_dict})'):
                    return User.update_dict(self, id, full_dict)
                else:
                    print("None here")

            else:
                print("** no intance found **")
        except UnboundLocalError:
            pass

    def do_Place(self, arg):
        """
            handle the user commands
        """
        args = arg.split('.')
        if args[1] == 'all()':
            return Place.all(self)
        if args[1] == 'count()':
            return Place.count(self)
        try:
            # regx pattern to match uuid format
            pattern = r'([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})'
            match = re.search(pattern, args[1])
            if match:
                id = match.group()
                if args[1] == f'show("{id}")':
                    return Place.show(self, id)
                if args[1] == f'destroy("{id}")':
                    return Place.destroy(self, id)

                #  section for updating using attribute and value
                # remove white space around
                attr = arg.split(',')[1].strip()[1:-1]

                # to remove the ')' in the end
                value = arg.split(',')[2].strip()[: -1]
                if(args[1] == f'update("{id}", "{attr}", {value})'):
                    return Place.update(self, id, attr, value)

                #  section for updating using id and dict input
                dict_input = arg.split('{')[1].strip()[:-1]
                full_dict = '{' + dict_input
                if (args[1] == f'update("{id}", {full_dict})'):
                    return Place.update_dict(self, id, full_dict)
            else:
                print("** no intance found **")
        except UnboundLocalError:
            pass

    def do_State(self, arg):
        """
            Handels the State commands
        """
        args = arg.split('.')
        if args[1] == 'all()':
            return State.all(self)
        if args[1] == 'count()':
            return State.count(self)
        try:
            # regx pattern to match uuid format
            pattern = r'([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})'
            match = re.search(pattern, args[1])
            if match:
                id = match.group()
                if args[1] == f'show("{id}")':
                    return State.show(self, id)
                if args[1] == f'destroy("{id}")':
                    return State.destroy(self, id)

                # section for updating using attribute and value
                # remove white space around
                attr = arg.split(',')[1].strip()[1:-1]
                # to remove the ')' in the end
                value = arg.split(',')[2].strip()[: -1]
                if(args[1] == f'update("{id}", "{attr}", {value})'):
                    return State.update(self, id, attr, value)

                #  section for updating using id and dict input
                dict_input = arg.split('{')[1].strip()[:-1]
                full_dict = '{' + dict_input
                if (args[1] == f'update("{id}", {full_dict})'):
                    return State.update_dict(self, id, full_dict)
                else:
                    print("None here")
            else:
                print("** no intance found **")
        except UnboundLocalError:
            pass

    def do_City(self, arg):
        """
            Handles the City commands
        """
        args = arg.split('.')
        if args[1] == 'all()':
            return City.all(self)
        elif args[1] == 'count()':
            return City.count(self)
        try:
            # regx pattern to match uuid format
            pattern = r'([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})'
            match = re.search(pattern, args[1])
            if match:
                id = match.group()
                if args[1] == f'show("{id}")':
                    return City.show(self, id)
                if args[1] == f'destroy("{id}")':
                    return City.destroy(self, id)

                # remove white space around
                attr = arg.split(',')[1].strip()[1:-1]
                # to remove the ')' in the end
                value = arg.split(',')[2].strip()[:-1]
                if args[1] == f'update("{id}", "{attr}", {value})':
                    return City.update(self, id, attr, value)
                #  section for updating using id and dict input
                dict_input = arg.split('{')[1].strip()[:-1]
                full_dict = '{' + dict_input
                if (args[1] == f'update("{id}", {full_dict})'):
                    return City.update_dict(self, id, full_dict)
                else:
                    print("None here")
            else:
                print("** no intance found **")
        except UnboundLocalError:
            pass

    def do_Review(self, arg):
        """
            Handle the review object
        """
        args = arg.split('.')
        if args[1] == 'all()':
            return Review.all(self)
        elif args[1] == 'count()':
            return Review.count(self)
        try:
            # regx pattern to match uuid format
            pattern = r'([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})'
            match = re.search(pattern, args[1])
            if match:
                id = match.group()
                if args[1] == f'show("{id}")':
                    return Review.show(self, id)
                if args[1] == f'destroy("{id}")':
                    return Review.destroy(self, id)

                # remove white space around
                attr = arg.split(',')[1].strip()[1:-1]
                # to remove the ')' in the end
                value = arg.split(',')[2].strip()[:-1]
                if args[1] == f'update("{id}", "{attr}", {value})':
                    return Review.update(self, id, attr, value)
                #  section for updating using id and dict input
                dict_input = arg.split('{')[1].strip()[:-1]
                full_dict = '{' + dict_input
                if (args[1] == f'update("{id}", {full_dict})'):
                    return Review.update_dict(self, id, full_dict)
                else:
                    print("None here")
            else:
                print("** no intance found **")
        except UnboundLocalError:
            pass

    def do_Amenity(self, arg):
        """
            Handles the Amenity object
        """
        args = arg.split('.')
        if args[1] == 'all()':
            return Amenity.all(self)
        elif args[1] == 'count()':
            return Amenity.count(self)
        try:
            # regx pattern to match uuid format
            pattern = r'([a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})'
            match = re.search(pattern, args[1])
            if match:
                id = match.group()
                if args[1] == f'show("{id}")':
                    return Amenity.show(self, id)
                if args[1] == f'destroy("{id}")':
                    return Amenity.destroy(self, id)

                # remove white space around
                attr = arg.split(',')[1].strip()[1:-1]
                # to remove the ')' in the end
                value = arg.split(',')[2].strip()[:-1]
                if args[1] == f'update("{id}", "{attr}", {value})':
                    return Amenity.update(self, id, attr, value)
                #  section for updating using id and dict input
                dict_input = arg.split('{')[1].strip()[:-1]
                full_dict = '{' + dict_input
                if (args[1] == f'update("{id}", {full_dict})'):
                    return Amenity.update_dict(self, id, full_dict)
                else:
                    print("None here")
            else:
                print("** no intance found **")
        except UnboundLocalError:
            pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
