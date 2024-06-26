from flask import Flask
from faker import Faker
import random
import os
import pickle
import json

class Id_counter:
    def __init__ (self, start_value=0):
        self.count = start_value
    

    def get_id(self):
        self.count += 1
        return self.count


class Group:
    def __init__(self, id, number):
        self.id = id
        self.number = number
    

    def __json__(self):
        return {
            'id': self.id,
            'number': self.number
        }


class Student:
    def __init__(self, id, group_id, full_name):
        self.id = id
        self.group_id = group_id
        self.full_name = full_name
    

    def __json__(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'full_name': self.full_name
        }

class Use_case:
    def __init__(self, groups):
        self.groups = groups


    def get_student_by_id(self, student_id):
        for group in self.groups:
            for student in group.students:
                if student.id == student_id:
                    return student
        return None


    def get_students_in_group(self, group_id):
        students_ids = []
        for group in self.groups:
            if group.id == group_id:
                for student in group.students:
                    students_ids.append(student.id)
        return students_ids
    

    def get_groups(self):
        groups_ids = []
        for group in self.groups:
            groups_ids.append(group.id)
        return groups_ids


    def get_group_by_id(self, group_id):
        for group in self.groups:
            if group.id == group_id:
                return group
        return None
    

    def get_schedule(self, group_id):
        return {
            'id': 0,
            'group_id': group_id,
            'days': {
                'Mon': [
                    {'number' : 2, 'name' : 'Основы военной подготовки', 'class' : '24-01', 'type': 'lecture'}
                ],
                'Tue' : [
                    {'number' : 2, 'name' : 'Микроконтроллерные системы', 'class' : '32-04', 'type' : 'lecture'},
                    {'number' : 3, 'name' : 'Корпоративные сети', 'class' : '32-04', 'type' : 'lecture'},
                    {'number' : 4, 'name' : 'Корпоративные сети', 'class' : '22-10', 'type' : 'labwork'},
                    {'number' : 5, 'name' : 'Моделирование', 'class' : '22-09', 'type' : 'labwork'}
                ],
                'Wed' : [
                    {'number' : 1, 'name' : 'Основы искусственного интеллекта', 'class' : '51-02в', 'type':'practice'},
                    {'number' : 2, 'name' : 'Микроконтроллерные системы', 'class' : '52-09', 'type' : 'labwork'},
                    {'number' : 4, 'name' : 'Основы искусственного интеллекта', 'class' : '32-04', 'type':'lecture'}
                ],
                'Fri' : [
                    {'number' : 1, 'name' : 'Системное программное обеспечение', 'class' : '32-04', 'type':'labwork'},
                    {'number' : 2, 'name' : 'Физическая культура', 'class' : 'Спортзал', 'type':'practice'},
                    {'number' : 3, 'name' : 'Моделирование', 'class' : '32-04', 'type':'lecture'},
                    {'number' : 4, 'name' : 'Схемотехника', 'class' : '22-09', 'type':'lecture'},
                ],
                'Sat' : [
                    {'number' : 1, 'name' : 'Основы военной подготовки', 'class' : '24-06', 'type':'practice'},
                    {'number' : 3, 'name' : 'Организация ЭВМ', 'class' : '32-04', 'type' : 'lecture'},
                    {'number' : 4, 'name' : 'Основы искусственного интеллекта', 'class' : '22-13', 'type':'labwork'}
                ]
            }
        }
    

fake = Faker('ru_RU')
group_id_counter = Id_counter(1000)
student_id_counter = Id_counter(10000)


def generate_students(num_students, group_id):
    global student_id_counter
    students = []
    for i in range(1, num_students + 1):
        full_name = fake.name()
        student = Student(id=student_id_counter.get_id(), group_id=group_id, full_name=full_name)
        students.append(student)
    return students


def setup_groups(num_groups, students_per_group):
    global group_id_counter
    groups = []
    for i in range(1, num_groups + 1):
        id = group_id_counter.get_id()
        group = Group(id=id, number=fake.pyint(1000,9999,1))
        group_students = generate_students(students_per_group, group.id)
        groups.append(group)
        group.students = group_students
    return groups


def save_students_to_file(students, filename):
    with open(filename, 'wb') as f:
        pickle.dump(students, f)


def load_students_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        return None


def setup_routes(app, use_case):
    @app.route('/')
    def index():
        return 'aboba'
    
    @app.route('/student/<int:student_id>', methods=['GET'])
    def get_student(student_id):
        student = use_case.get_student_by_id(student_id)
        if student:
            return json.dumps(student.__json__(), ensure_ascii=False), 200
        else:
            return json.dumps({'error': 'Student not found'}), 404
        
    @app.route('/group/<int:group_id>', methods=['GET'])
    def get_group(group_id):
        group = use_case.get_group_by_id(group_id)
        if group:
            return json.dumps(group.__json__(), ensure_ascii=False), 200
        else:
            return json.dumps({'error': 'Group not found'}), 404
        
    @app.route('/group/<int:group_id>/students', methods=['GET'])
    def get_group_students(group_id):
        students_ids = use_case.get_students_in_group(group_id)
        if students_ids:
            return json.dumps(students_ids), 200
        else:
            return json.dumps({'error': 'Group not found or has no students'}), 404
        
    @app.route('/group', methods=['GET'])
    def get_groups():
        groups_ids = use_case.get_groups()
        if groups_ids:
            return json.dumps(groups_ids), 200
        else:
            return json.dumps({'error': 'No groups (HOW?)'}), 404
        
    @app.route('/schedule/<int:group_id>', methods=['GET'])
    def get_schedule(group_id):
        schedule = use_case.get_schedule(group_id)
        if schedule:
            return json.dumps(schedule, ensure_ascii=False), 200
        else:
            return json.dumps({'error': 'Group not found'}), 404


if __name__ == '__main__':
    students_filename = 'students.pkl'

    saved_groupes = load_students_from_file(students_filename)

    if saved_groupes:
        print("Loaded students from file.")
    else:
        print("Generating new students.")
        saved_groupes = setup_groups(num_groups=3, students_per_group=random.randint(8, 10))
        save_students_to_file(saved_groupes, students_filename)

    use_case = Use_case(saved_groupes)
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    
    setup_routes(app, use_case)

    app.run(host='0.0.0.0', port=8080, debug=True)
