# Eng-Beam: Beam Analysis Tool

#Welcome to Eng-Beam, a tool for analyzing beam properties and performing engineering calculations. This tool supports various beam cross-sections and input methods, making it versatile for different engineering applications.

## Features

#**CSV File Input**: Analyze beam data from CSV files for solid rectangular, circular, and circular tube sections.
#**Manual Input**: Perform beam analysis with manually entered dimensions and forces.
#**Results Output**: Outputs analyzed results to CSV files for easy reference and further analysis.
#**Beam Types Supported**: Solid Rectangular, Circular, and Circular Tube cross-sections.

import time
import math
import numpy as np
import csv

def main():
    """
    Main function to initiate the Eng-Beam tool.
    """
    print("Welcome to Eng-Beam: Beam Analysis Tool")
    print("Please select your input method:")
    print("1. CSV File")
    print("2. Manual Input")
    option = input("Choice: ")

    try:
        option = int(option)
    except ValueError:
        print("Error: Your choice must be a valid option (integer).")
        return

    if option == 1:
        csv_input_method()
    elif option == 2:
        manual_input_method()
    else:
        print("Error: Your choice must be a valid option (integer).")

def csv_input_method():
    """
    Function to handle beam analysis using input from a CSV file.
    """
    print("Please select your Beam Cross-Section from the following options:")
    print("1. Solid Rectangular")
    print("2. Circular")
    print("3. Circular Tube")
    print("0. Exit")
    option = input("Choice: ")

    try:
        option = int(option)
    except ValueError:
        print("Error: Your choice must be a valid option (integer).")
        return

    if option == 0:
        print("Bye!")
        return

    input_filename = input("Enter the name of your input file: ")
    try:
        with open(input_filename, 'r') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            process_data(option, data)
    except FileNotFoundError:
        print("Error: The file was not found.")
        return

def process_data(option, data):
    """
    Function to process the selected beam cross-section data.
    """
    if option == 1:
        output_filename = 'results.csv'
        process_rectangular_beam(data, output_filename)
    elif option == 2:
        output_filename = 'results(Circular).csv'
        process_circular_beam(data, output_filename)
    elif option == 3:
        output_filename = 'results(CircularTube).csv'
        process_circular_tube_beam(data, output_filename)
    else:
        print("Error: Your choice must be a valid option (integer).")

def process_rectangular_beam(data, output_filename):
    """
    Function to process rectangular beam data and perform analysis.
    """
    start = time.time()
    with open(output_filename, 'w', newline='') as output:
        output_data = csv.writer(output)
        line_count = 0
        for row in data:
            if line_count == 0:
                # Adding headers for the computed values
                row.extend(['Area (m^2)', 'Moment of Inertia (m^4)', 'Bending Moment (N*m)',
                            'Maximum Shear Stress (Pascals)', 'Maximum Bending Stress (Pascals)',
                            'Beam Deflection (m)', 'Natural Frequency (Hz)'])
                output_data.writerow(row)
                line_count += 1
                print(row[4:11])
            else:
                process_rectangular_row(row, output_data)
                line_count += 1
                print(row[4:11])
    print('Analysis Complete: Your results were saved in the results.csv file')
    end = time.time()
    print('Duration (seconds)', end - start)

def process_rectangular_row(row, output_data):
    Force = float(row[3])
    width = float(row[1])
    height = float(row[2])
    length = float(row[0])
    E = 210e9  # Young's Modulus for steel in Pascals
    density = 7850  # Density of steel in kg/m^3

 # Calculating Moment of Inertia (MOI), Bending Moment, Area, Deflection, and Natural Frequency
    MOI = (1/12) * (width * height**3)
    bendingMoment = length * Force
    Area = width * height
    deflection = (Force * length**3) / (3 * E * MOI)
    mass_per_unit_length = Area * density
    natural_frequency = (1 / (2 * math.pi)) * math.sqrt((3 * E * MOI) / (mass_per_unit_length * length**3))

 # Appending computed values to the row
    row.extend([Area, MOI, bendingMoment,
                ((3/2) * Force) / Area,
                ((bendingMoment) * (height/2)) / MOI,
                deflection,
                natural_frequency])
    output_data.writerow(row)

def process_circular_beam(data, output_filename):
    """
    Process circular beam data from CSV and perform analysis.

    Parameters:
    - data: CSV data iterator
    - output_filename: Name of the output CSV file
    """
    start = time.time()
    with open(output_filename, 'w', newline='') as output:
        output_data = csv.writer(output)
        line_count = 0
        for row in data:
            if line_count == 0:
                # Adding headers for computed values
                row.extend(['Area (m^2)', 'Moment of Inertia (m^4)', 'Bending Moment (N*m)',
                            'Maximum Shear Stress (Pascals)', 'Maximum Bending Stress (Pascals)',
                            'Beam Deflection (m)', 'Natural Frequency (Hz)'])
                output_data.writerow(row)
                line_count += 1
                print(row[3:10]) # Print relevant columns for the user to review
            else:
                process_circular_row(row, output_data)
                line_count += 1
                print(row[3:10]) # Print relevant columns for the user to review
    print('Analysis Complete: Your results were saved in the results(Circular).csv file')
    end = time.time()
    print('Duration (seconds)', end - start)

def process_circular_row(row, output_data):
    """
    Calculate circular beam parameters and append results to the row.

    Parameters:
    - row: Data row from CSV
    - output_data: CSV writer object for output file
    """
    Force = float(row[2])
    diameter = float(row[1])
    length = float(row[0])
    E = 210e9  # Young's Modulus for steel in Pascals
    density = 7850  # Density of steel in kg/m^3

 # Calculate Area, Moment of Inertia (MOI), Bending Moment, Deflection, and Natural Frequency
    MOI = (math.pi / 64) * (diameter**4)
    bendingMoment = length * Force
    Area = (math.pi / 4) * diameter**2
    deflection = (Force * length**3) / (3 * E * MOI)
    mass_per_unit_length = Area * density
    natural_frequency = (1 / (2 * math.pi)) * math.sqrt((3 * E * MOI) / (mass_per_unit_length * length**3))

    # Append computed values to the row
    row.extend([Area, MOI, bendingMoment,
                (4/3) * Force / Area,
                (bendingMoment * (diameter / 2)) / MOI,
                deflection,
                natural_frequency])
    output_data.writerow(row)

def process_circular_tube_beam(data, output_filename):
    """
    Process circular tube beam data from CSV and perform analysis.

    Parameters:
    - data: CSV data iterator
    - output_filename: Name of the output CSV file
    """
    start = time.time()
    with open(output_filename, 'w', newline='') as output:
        output_data = csv.writer(output)
        line_count = 0
        for row in data:
            if line_count == 0:
                # Adding headers for computed values
                row.extend(['Area (m^2)', 'Moment of Inertia (m^4)', 'Bending Moment (N*m)',
                            'Maximum Shear Stress (Pascals)', 'Maximum Bending Stress (Pascals)',
                            'Beam Deflection (m)', 'Natural Frequency (Hz)'])
                output_data.writerow(row)
                line_count += 1
                print(row[4:11]) # Print relevant columns for the user to review
            else:
                process_circular_tube_row(row, output_data)
                line_count += 1
                print(row[4:11]) # Print relevant columns for the user to review
    print('Analysis Complete: Your results were saved in the results(CircularTube).csv file')
    end = time.time()
    print('Duration (seconds)', end - start)

def process_circular_tube_row(row, output_data):
    """
    Calculate circular tube beam parameters and append results to the row.

    Parameters:
    - row: Data row from CSV
    - output_data: CSV writer object for output file
    """
    Force = float(row[3])
    outer_diameter = float(row[1])
    inner_diameter = float(row[2])
    length = float(row[0])
    E = 210e9  # Young's Modulus for steel in Pascals
    density = 7850  # Density of steel in kg/m^3

# Calculate Area, Moment of Inertia (MOI), Bending Moment, Deflection, and Natural Frequency
    Area = (math.pi / 4) * (outer_diameter**2 - inner_diameter**2)
    MOI = (math.pi / 64) * (outer_diameter**4 - inner_diameter**4)
    bendingMoment = length * Force
    deflection = (Force * length**3) / (3 * E * MOI)
    mass_per_unit_length = Area * density
    natural_frequency = (1 / (2 * math.pi)) * math.sqrt((3 * E * MOI) / (mass_per_unit_length * length**3))

# Numerator and denominator for Maximum Shear Stress formula
    num = (outer_diameter/2)**2 + (1/4)*outer_diameter*inner_diameter + (inner_diameter/2)**2
    den = (outer_diameter/2)**2 + (inner_diameter/2)**2

# Append computed values to the row
    row.extend([Area, MOI, bendingMoment,
                (4/3) * (Force / Area) * (num / den),
                (bendingMoment * (outer_diameter / 2)) / MOI,
                deflection,
                natural_frequency])
    output_data.writerow(row)

def manual_input_method():
    """
    Function to handle manual input for selecting beam cross-sections.
    """
    print("Please select your Beam Cross-Section from the following options:")
    print("1. Solid Rectangular")
    print("2. Circular")
    print("3. Circular Tube")
    print("0. Exit")
    option = input("Choice: ")

    try:
        option = int(option)
    except ValueError:
        print("Error: Your choice must be a valid option (integer).")
        return

    if option == 0:
        print("Bye!")
        return

    if option == 1:
        process_rectangular_beam_manual()
    elif option == 2:
        process_circular_beam_manual()
    elif option == 3:
        process_circular_tube_beam_manual()
    else:
        print("Error: Your choice must be a valid option (integer).")

def process_rectangular_beam_manual():
    """
    Function to perform manual input and analysis for rectangular beam.

    Prompts user for beam dimensions and applied force, calculates:
    - Area
    - Moment of Inertia (MOI)
    - Bending Moment
    - Maximum Shear Stress
    - Maximum Bending Stress
    - Beam Deflection
    - Natural Frequency

    Prints and displays results.
    """
    length = float(input("Enter the length of the beam (m): "))
    width = float(input("Enter the width of the beam (m): "))
    height = float(input("Enter the height of the beam (m): "))
    force = float(input("Enter the force applied on the beam (N): "))

    E = 210e9  # Young's Modulus for steel in Pascals
    density = 7850  # Density of steel in kg/m^3

    # Calculating beam properties
    area = width * height
    moi = (1/12) * (width * height**3)
    bending_moment = length * force
    deflection = (force * length**3) / (3 * E * moi)
    mass_per_unit_length = area * density
    natural_frequency = (1 / (2 * math.pi)) * math.sqrt((3 * E * moi) / (mass_per_unit_length * length**3))

    #Printing results
    print("\nResults:")
    print(f"Area: {area:.6f} m^2")
    print(f"Moment of Inertia: {moi:.6f} m^4")
    print(f"Bending Moment: {bending_moment:.6f} N*m")
    print(f"Maximum Shear Stress: {(3/2) * force / area:.6f} Pascals")
    print(f"Maximum Bending Stress: {(bending_moment * (height/2)) / moi:.6f} Pascals")
    print(f"Beam Deflection: {deflection:.6f} m")
    print(f"Natural Frequency: {natural_frequency:.6f} Hz")

def process_circular_beam_manual():
    """
    Function to perform manual input and analysis for circular beam.

    Prompts user for beam diameter and applied force, calculates:
    - Area
    - Moment of Inertia (MOI)
    - Bending Moment
    - Maximum Shear Stress
    - Maximum Bending Stress
    - Beam Deflection
    - Natural Frequency

    Prints and displays results.
    """
    length = float(input("Enter the length of the beam (m): "))
    diameter = float(input("Enter the diameter of the beam (m): "))
    force = float(input("Enter the force applied on the beam (N): "))

    E = 210e9  # Young's Modulus for steel in Pascals
    density = 7850  # Density of steel in kg/m^3

    # Calculating beam properties
    area = (math.pi / 4) * diameter**2
    moi = (math.pi / 64) * diameter**4
    bending_moment = length * force
    deflection = (force * length**3) / (3 * E * moi)
    mass_per_unit_length = area * density
    natural_frequency = (1 / (2 * math.pi)) * math.sqrt((3 * E * moi) / (mass_per_unit_length * length**3))

    # Printing results
    print("\nResults:")
    print(f"Area: {area:.6f} m^2")
    print(f"Moment of Inertia: {moi:.6f} m^4")
    print(f"Bending Moment: {bending_moment:.6f} N*m")
    print(f"Maximum Shear Stress: {(4/3) * force / area:.6f} Pascals")
    print(f"Maximum Bending Stress: {(bending_moment * (diameter / 2)) / moi:.6f} Pascals")
    print(f"Beam Deflection: {deflection:.6f} m")
    print(f"Natural Frequency: {natural_frequency:.6f} Hz")

def process_circular_tube_beam_manual():
    """
    Function to perform manual input and analysis for circular tube beam.

    Prompts user for tube dimensions and applied force, calculates:
    - Area
    - Moment of Inertia (MOI)
    - Bending Moment
    - Maximum Shear Stress
    - Maximum Bending Stress
    - Beam Deflection
    - Natural Frequency

    Also provides option to generate and display Bending Moment and Shear Force Diagram.

    Prints and displays results and diagrams.
    """
    length = float(input("Enter the length of the beam (m): "))
    outer_diameter = float(input("Enter the outer diameter of the tube (m): "))
    inner_diameter = float(input("Enter the inner diameter of the tube (m): "))
    force = float(input("Enter the force applied on the tube (N): "))

    E = 210e9  # Young's Modulus for steel in Pascals
    density = 7850  # Density of steel in kg/m^3

    # Calculating beam properties
    area = (math.pi / 4) * (outer_diameter**2 - inner_diameter**2)
    moi = (math.pi / 64) * (outer_diameter**4 - inner_diameter**4)
    bending_moment = length * force
    deflection = (force * length**3) / (3 * E * moi)
    mass_per_unit_length = area * density
    natural_frequency = (1 / (2 * math.pi)) * math.sqrt((3 * E * moi) / (mass_per_unit_length * length**3))

    # Numerator and denominator for Maximum Shear Stress formula
    num = (outer_diameter/2)**2 + (1/4)*outer_diameter*inner_diameter + (inner_diameter/2)**2
    den = (outer_diameter/2)**2 + (inner_diameter/2)**2

    # Printing results
    print("\nResults:")
    print(f"Area: {area:.6f} m^2")
    print(f"Moment of Inertia: {moi:.6f} m^4")
    print(f"Bending Moment: {bending_moment:.6f} N*m")
    print(f"Maximum Shear Stress: {(4/3) * (force / area) * (num / den):.6f} Pascals")
    print(f"Maximum Bending Stress: {(bending_moment * (outer_diameter / 2)) / moi:.6f} Pascals")
    print(f"Beam Deflection: {deflection:.6f} m")
    print(f"Natural Frequency: {natural_frequency:.6f} Hz")

if __name__ == "__main__":
    main()