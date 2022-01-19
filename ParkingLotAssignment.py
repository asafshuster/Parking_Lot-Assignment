# Imports
import sys
import os

# Constant
COMMANDS_LST = ['create_parking_lot', 'leave', 'slot_numbers_for_cars_with_color', 'park', 'status',
                'slot_number_for_registration_number', 'registration_numbers_for_cars_with_color']


class ParkingLot:

    def __init__(self):
        self.number_of_slots = 0
        self.registration_number = 0
        self.cars_colors = {}
        self.parking = {}

    def _is_color_valid(self, color):
        """
        check for invalid color type.
        :param color: A given color
        :return: False

        """
        if not isinstance(color, str):
            print("Error: Invalid color input.")
            return False

    def _is_registration_n_already_exist(self, registration_n):
        """
        Check if a given registration number of a car is already in self.parking.
        :param registration_n: A given registration number.
        :return: False

        """
        if registration_n in self.parking:
            print(f"Error: The Registration number {registration_n} is already parking in the Parking lot")
            return False

    def _is_slot_n_valid(self, slot):
        """
        Check for invalid slot number type or value.
        :param slot: A given slot number
        :return: False

        """
        if slot < 0 or not isinstance(slot, int):
            print("Error: Invalid slot number")
            return False

    def _delete_registration_n_form_cars_colors(self, registration_n):
        """
        Remove a given registration number from the value of specific color in self.cars_colors.
        :param registration_n: A given registration number
        :return: None

        """
        for color in self.cars_colors:
            if registration_n in self.cars_colors[color]:
                self.cars_colors[color].remove(registration_n)
                if len(self.cars_colors[color]) == 0:
                    self.cars_colors.pop(color)
                    break

    def create_parking_lot(self, n):
        """
        Update the variable self.number_of_slots
        :param n: A number of slots
        :return: None

        """
        if n > 0 and isinstance(n, int):
            self.number_of_slots = n
            print(f"creates parking lot with {n} slots")
        else:
            print(f"Invalid parameter {n}")

    def add_car_to_cars_color(self, color, registration_n):
        """
        Add the a given registration number to value of color key in self.cars_colors
        :param color: A given color
        :param registration_n: A given registration number
        :return: None

        """
        if color in self.cars_colors:
            self.cars_colors[color].append(registration_n)
        else:
            self.cars_colors[color] = [registration_n]

    def park(self, registration_number, color):
        """
        Check for empty place in the parking lot, if no car is parking, park at slot 0,
        else check for the closest slot from the entry (or at the end).
        :param registration_number: A given registration number
        :param color: A given color
        :return: None

        """
        if self._is_registration_n_already_exist(registration_number) is False:
            return

        if len(self.parking) < self.number_of_slots:
            if len(self.parking) == 0:
                self.parking[registration_number] = 0
                print("Parking in slot number o")
            else:
                check = 0
                self.parking = {k: v for k, v in sorted(self.parking.items(), key=lambda item: item[1])}
                for slot in list(self.parking.values()):
                    if check == slot:
                        if list(self.parking.values())[-1] == slot:
                            self.parking[registration_number] = check + 1
                            print(f"Parking in slot {check + 1}")
                        else:
                            check += 1
                    else:
                        self.parking[registration_number] = check
                        print(f"Parking in slot number {check}")
                        break
            self.add_car_to_cars_color(color, registration_number)
        else:
            print("Sorry, the parking lot is full")
            return

    def leave(self, slot):
        """
        Delete key of registration number belong to a car that parking in a given slot.
        :param slot: A slot number
        :return: None

        """
        if self._is_slot_n_valid(slot) is False:
            return

        registration_number = list(self.parking.keys())[list(self.parking.values()).index(slot)]
        delete = self.parking.pop(registration_number, None)
        if delete is not None:
            print(f"Leaving car {registration_number} from slot {slot}")
        else:
            print(f"Unexist slot number {slot}")
        self._delete_registration_n_form_cars_colors(registration_number)

    def status(self):
        """
        Print the number of free slots at the parking lot, also an info about each car in the parking lot.
        :return: None

        """
        available_slots = self.number_of_slots - len(self.parking)
        print(f"The parking lot have {available_slots}/{self.number_of_slots} free slots.")
        for color in self.cars_colors:
            print(f"The cars registration numbers with the color {color}"
                  f" in the parking lot is {self.cars_colors[color]} ")

    def slot_numbers_for_cars_with_color(self, color):
        """
        Print the registration number of the cars for the given color
        :param color: A color
        :return: None

        """
        if self._is_color_valid(color) is False:
            return
        try:
            [print(registry) for registry in self.cars_colors[color]]
        except KeyError:
            print(f"There are no cars with the color {color} in the parking lot.")

    def slot_number_for_registration_number(self, registration_number):
        """
        Prints the slot number of the cars for the given number.
        :param registration_number: A registration number
        :return: None

        """
        try:
            print(self.parking[registration_number])
        except KeyError:
            print(f"No car with the registration number {registration_number}"
                  f" is parking in the parking lot")

    def registration_numbers_for_cars_with_color(self, color):
        """
        Print the slot number of the cars for the given color.
        :param color: A color
        :return: None

        """
        try:
            for registry in self.cars_colors[color]:
                print(f"The the slot number of the {color} car with registration number {registry} is"
                      f" {self.parking[registry]}")
        except KeyError:
            print(f"There is no any car with the color {color}")


def is_file_mode():
    """
    Check for input argument for the execution of the script, check for spaces in the file name.
    :return: (False)/ (True, file path)

    """
    if len(sys.argv) > 1:
        input_file = sys.argv[1:]
        if isinstance(input_file, list):
            file_without_space = "".join(input_file)
            return True, file_without_space
        else:
            return True, input_file
    else:
        return False


def read_input_file(file_path):
    """
    Open a given file, read lines, remove all '\n' from each line.
    :param file_path: A file path of input file.
    :return: A list of code lines.

    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as input_f:
            lines = input_f.readlines()
            formated_lines = [line.replace("\n", "") for line in lines]
            return formated_lines
    else:
        return f"The file {file_path} not exist"


def file_mode(code_lines):
    """
    Create an instance of ParkingLot class, run on each line of code from the input file and operate exec on it.
    :param code_lines: A list of lines of code form the input file.
    :return: None

    """
    my_parking_lot = ParkingLot()
    for line in code_lines:
        exec(f"my_parking_lot.{line}")


def interactive_mode():
    """
    Create an instance of ParkingLot class, exec in each iteration the input func until exit() input
    :return: None

    """
    my_parking_lot = ParkingLot()
    print("Interactive Mode \n- commends as the format: function(arg1, arg2, ...)\n- for exit: exit()")
    arg = input(">>> ")
    while arg != 'exit':
        only_func_name = arg.split("(")[0]
        if only_func_name in COMMANDS_LST:
            exec(f"my_parking_lot.{arg}")
        else:
            print(f"Invalid commend {only_func_name}")
        arg = input(">> ")


def main():
    return_file_mode_func = is_file_mode()
    file_mode_flag = return_file_mode_func

    if file_mode_flag:
        file_path = return_file_mode_func[1]
        code_lines = read_input_file(file_path)
        file_mode(code_lines)
    else:
        interactive_mode()



if __name__ == '__main__':
    main()