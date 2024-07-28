import re
import math

def fundamental(val, D):
    # Calculate fundamental deviations of shafts
    b = val.lower()
    dic = {
        "a": -(265 + 1.3 * D) if D <= 120 else -3.5 * D,
        "b": -12 * (D ** 0.56),
        "c": -6 * (D ** 0.44),
        "d": -16 * (D ** 0.44),
        "e": -8 * (D ** 0.34),
        "f": -2.5 * (D ** 0.34),
        "g": -2.5 * (D ** 0.34),
        "h": 0,
        "i": -0.6 * (D ** 0.5),
        "j": -0.4 * (D ** 0.4),
        "k": -0.2 * (D ** 0.3),
        "l": -0.1 * (D ** 0.2),
        "m": -0.08 * D,
        "n": -0.04 * D,
        "o": 0,
        "p": 0,
        "q": 0,
        "r": 0,
        "s": 0,
        "t": 0,
        "u": 0,
        "v": 0,
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
        "CD": -(12 + 0.8 * D) if D <= 120 else -2 * D,
        "EF": -6 * (D ** 0.44),
        "FG": -2.5 * (D ** 0.34),
        "JS": -0.8 * (D ** 0.5),
    }
    try:
        return round(float(dic.get(b)), 2)
    except:
        raise ValueError('Enter a valid value.')


def check_range(number):
    ranges = {
        (1, 3): "1-3",
        (3, 6): "3-6",
        (6, 10): "6-10",
        (10, 18): "10-18",
        (18, 30): "18-30",
        (30, 50): "30-50",
        (50, 80): "50-80",
        (80, 120): "80-120",
        (120, 180): "120-180",
        (180, 250): "180-250",
        (250, 315): "250-315",
        (315, 400): "315-400",
        (400, 500): "400-500"
    }

    for bounds in ranges:
        if bounds[0] < number <= bounds[1]:
            return (int(bounds[0]), int(bounds[1]))

    raise ValueError("Input number is out of range.")


def get_range_value(it_number):
    ranges = {
        "IT6": 10,
        "IT7": 16,
        "IT8": 25,
        "IT9": 40,
        "IT10": 64,
        "IT11": 100,
        "IT12": 160,
        "IT13": 250,
        "IT14": 400,
        "IT15": 640,
        "IT16": 1000
    }
    return ranges.get(it_number, "Invalid input.")


def evaluate_limits_and_fit(assembly_pair):
    extraction_num = [int(num) for num in re.findall(r'\d+', assembly_pair)]
    extraction_var = [char for char in assembly_pair if re.match(r'[a-zA-Z]', char)]

    if len(extraction_num) < 1 or len(extraction_var) < 2:
        raise ValueError("Enter a valid assembly pair (e.g., 6 H7/g6 mm)")

    Zero_line = extraction_num[0]
    Dcalc = extraction_num[0]
    range_result = check_range(Dcalc)

    D = round((range_result[0] * range_result[1]) ** (1 / 2), 3)
    # Calculate standard tolerance unit (i)
    i = round((0.45 * (D ** (1 / 3)) + 0.001 * D), 5)
    # Calculate the alphabetic values
    try:
        shaft_var=fundamental(extraction_var[1], D)
        hole_var = fundamental(extraction_var[0], D)
    except ValueError:
        raise ValueError("Enter valid alphabetic values.")

    it_hole = 'IT' + str(extraction_num[1])
    IT_HOLE = get_range_value(it_hole)
    tol_hole = math.ceil((IT_HOLE * i))
    it_shaft = 'IT' + str(extraction_num[2])
    IT_SHAFT = get_range_value(it_shaft)
    tol_shaft = math.ceil((IT_SHAFT * i))
    # Calculate maximum and minimum sizes for hole and shaft
    hole_max_size = Zero_line + (tol_hole * (10 ** (-3)))
    hole_min_size = Zero_line + hole_var
    shaft_min_size = round((Zero_line - ((tol_shaft-shaft_var) * (10 ** (-3)))), 3)
    shaft_max_size = round((Zero_line + (shaft_var * (10 ** (-3)))), 3)

    # Calculate maximum and minimum clearances
    max_clearance = hole_max_size - shaft_min_size
    print(f"The max clearance = {math.ceil(max_clearance*10**(3))} μm" )
    min_clearance = hole_min_size - shaft_max_size
    print(f"The min clearance = {math.ceil(min_clearance*10**(3))} μm")

    # Determine the fit type based on the clearances
    if max_clearance > 0 and min_clearance > 0:
        fit_type = "Clearance Fit"
    elif max_clearance <= 0 and min_clearance <= 0:
        fit_type = "Interference Fit"
    else:
        fit_type = "Transition Fit"

    # Return the limits, fit type, standard tolerance unit, diameter steps, and fundamental deviations
    return hole_min_size, hole_max_size, shaft_min_size, shaft_max_size, fit_type, i, tol_hole, tol_shaft


try:
    assembly_pair = input("Enter the assembly pair (e.g., 6 H7/g6 mm): ")
    hole_min, hole_max, shaft_min, shaft_max, fit_type, i, TolHole, TolShaft = evaluate_limits_and_fit(assembly_pair)
    print(f"Limits for the hole: {hole_min} mm - {hole_max} mm")
    print(f"Limits for the shaft: {shaft_min} mm - {shaft_max} mm")
    print(f"Fit type: {fit_type}")
    print(f"Standard Tolerance Unit (i): {i} μm")
    print(f"Tolerance for hole {assembly_pair.split('/')[0].split(' ')[1]} is {TolHole} μm")
    print(f"Tolerance for shaft {assembly_pair.split('/')[1].split(' ')[0]} is {TolShaft} μm")
except ValueError as e:
    print(f"Error: {str(e)}")
