from __future__ import annotations

from dataclasses import dataclass


DATA_FILE = "Studentdata.txt"


@dataclass
class Student:
    rollno: int
    name: str
    marks: float
    next: Student | None = None


class StudentDatabase:
    def __init__(self) -> None:
        self.head: Student | None = None
        self.count = 0
        self.load_student()

    def add_student(self) -> None:
        self.count += 1
        print("Enter the name and marks of the student:")
        name = input("Name: ").strip()
        marks = float(input("Marks: "))
        new_student = Student(self.count, name, marks)

        if self.head is None or new_student.rollno < self.head.rollno:
            new_student.next = self.head
            self.head = new_student
        else:
            current = self.head
            while current.next is not None and new_student.rollno > current.next.rollno:
                current = current.next
            new_student.next = current.next
            current.next = new_student

        print("Data recorded successfully.")

    def delete_student(self) -> None:
        if self.head is None:
            print("No Student records found.")
            return

        print("Delete student by \n1) Rollno\n2) Name")
        choice = input("Choice: ").strip()

        if choice == "1":
            self._delete_by_rollno(int(input("Enter Rollno: ")))
        elif choice == "2":
            self._delete_by_name(input("Enter Name: ").strip())
        else:
            print("Invalid option.")

    def _delete_by_rollno(self, rollno: int) -> None:
        previous: Student | None = None
        current = self.head

        while current is not None:
            if current.rollno == rollno:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                self._update_roll_numbers()
                self.count -= 1
                print("Record is deleted.")
                return
            previous, current = current, current.next

        print("Roll number not found.")

    def _delete_by_name(self, name: str) -> None:
        previous: Student | None = None
        current = self.head

        while current is not None:
            if current.name == name:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                self._update_roll_numbers()
                self.count -= 1
                print("Record is deleted.")
                return
            previous, current = current, current.next

        print("Name not found.")

    def show_student(self) -> None:
        if self.head is None:
            print("No records found.")
            return

        current = self.head
        while current is not None:
            print(
                f"Rollno: {current.rollno} "
                f"Name: {current.name} "
                f"Marks: {current.marks}"
            )
            current = current.next

    def modify_student(self) -> None:
        if self.head is None:
            print("No Student records found.")
            return

        print("Modify student by \n1) Rollno\n2) Name")
        choice = input("Choice: ").strip()

        if choice == "1":
            self._modify_by_rollno(int(input("Enter Rollno: ")))
        elif choice == "2":
            self._modify_by_name(input("Enter Name: ").strip())
        else:
            print("Invalid option.")

    def _modify_by_rollno(self, rollno: int) -> None:
        current = self.head
        while current is not None:
            if current.rollno == rollno:
                print("Enter new name and marks:")
                current.name = input("Name: ").strip()
                current.marks = float(input("Marks: "))
                print("Record updated.")
                return
            current = current.next

        print("Record not found.")

    def _modify_by_name(self, name: str) -> None:
        current = self.head
        while current is not None:
            if current.name == name:
                print("Enter new marks:")
                current.marks = float(input("Marks: "))
                print("Record updated.")
                return
            current = current.next

        print("Record not found.")

    def save_student(self) -> None:
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as writer:
                writer.write("RollNo->Name->Marks\n")
                current = self.head
                while current is not None:
                    writer.write(f"{current.rollno}->{current.name}->{current.marks}\n")
                    current = current.next
            print("Data saved successfully.")
        except OSError as error:
            print(f"Could not save student data: {error}")

    def delete_all(self) -> None:
        self.head = None
        self.count = 0
        print("Deleted all records.")
        self.save_student()

    def reverse_list(self) -> None:
        if self.head is None:
            print("No records found.")
            return

        previous: Student | None = None
        current = self.head
        while current is not None:
            next_student = current.next
            current.next = previous
            previous = current
            current = next_student

        self.head = previous
        print("List is reversed.")

    def _update_roll_numbers(self) -> None:
        rollno = 1
        current = self.head
        while current is not None:
            current.rollno = rollno
            rollno += 1
            current = current.next

    def load_student(self) -> None:
        try:
            with open(DATA_FILE, encoding="utf-8") as reader:
                next(reader, None)  # Skip the header.
                for line_number, line in enumerate(reader, start=2):
                    parts = line.rstrip("\r\n").split("->")
                    if len(parts) != 3:
                        print(f"Skipping malformed student record on line {line_number}.")
                        continue

                    try:
                        rollno = int(parts[0])
                        marks = float(parts[2])
                    except ValueError:
                        print(f"Skipping malformed student record on line {line_number}.")
                        continue

                    student = Student(rollno, parts[1], marks)
                    if self.head is None:
                        self.head = student
                    else:
                        current = self.head
                        while current.next is not None:
                            current = current.next
                        current.next = student
                    self.count = max(self.count, rollno)

            print("Data loaded from file.")
        except FileNotFoundError:
            print("No previous data found. Starting fresh.")
        except OSError as error:
            print(f"Could not load student data: {error}")


def main() -> None:
    database = StudentDatabase()
    actions = {
        "1": database.add_student,
        "2": database.delete_student,
        "3": database.show_student,
        "4": database.modify_student,
        "5": database.save_student,
        "6": database.delete_all,
        "7": database.reverse_list,
    }

    while True:
        print(
            "\n1) AddStudent 2) DeleteStudent 3) ShowStudent "
            "4) ModifyStudent 5) SaveStudent 6) DeleteAll "
            "7) ReverseList 8) ExitProgram"
        )
        choice = input("Enter your choice: ").strip()

        if choice == "8":
            return
        action = actions.get(choice)
        if action is None:
            print("Invalid option.")
        else:
            action()


if __name__ == "__main__":
    main()