import csv
import os
import shutil
from xml.etree import ElementTree as ET

debugging = False

def evaluate_math(expr):
    try:
        # Evaluate the expression and return the result
        return str(eval(expr, {"__builtins__": None}, {}))
    except:
        # If there's an error (e.g., syntax), return the original expression
        return expr

def compute_expression(expression):
    try:
        # Safely evaluate the mathematical expression
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        # In case of any error, return the original expression
        return expression

def compute_math_of_XML(xml_path, final_xml_path):
    # Load your XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Iterate through all elements in the XML
    for elem in root.iter():
        # Iterate through each attribute of the element
        for attr in elem.attrib:
            # Get the attribute value
            attr_value = elem.get(attr)
            # Check if the attribute value contains a mathematical expression
            # Only consider + and - math operations:
            if "-" in attr_value or "+" in attr_value or "*" in attr_value or "/" in attr_value:
                # Compute the result and update the attribute value
                elem.set(attr, compute_expression(attr_value))

    # Save the modified XML back to the file
    tree.write(final_xml_path, encoding="utf-8")

    if debugging == False:
        if os.path.exists(xml_path):
            # Delete the file
            os.remove(xml_path)
        else:
            print(f"The file {xml_path} does not exist. It should. Are inputs alright?")

def process_csv_line(line, xml_folder_path, out_folder_path):
    unique_id, original_xml_filename, \
        var_name_1, var_value_1, var_name_2, var_value_2, \
            var_name_3, var_value_3, var_name_4, var_value_4, \
                var_name_5, var_value_5, var_name_6, var_value_6, \
                    var_name_7, var_value_7, var_name_8, var_value_8 = line
    # Evaluate mathematical expressions in variable values
    var_value_1 = evaluate_math(var_value_1)
    var_value_2 = evaluate_math(var_value_2)
    var_value_3 = evaluate_math(var_value_3)
    var_value_4 = evaluate_math(var_value_4)
    var_value_5 = evaluate_math(var_value_5)
    var_value_6 = evaluate_math(var_value_6)
    var_value_7 = evaluate_math(var_value_7)
    var_value_8 = evaluate_math(var_value_8)
    
    # Construct the path to the original XML file
    original_xml_path = f"{xml_folder_path}/{original_xml_filename}.scx" # Suffix: ".scx"
    
    if os.path.exists(original_xml_path):
        # Load the XML file
        tree = ET.parse(original_xml_path)
        root = tree.getroot()

        # Replace variable names with their corresponding values
        xml_str = ET.tostring(root, encoding='unicode')
        xml_str = xml_str.replace(var_name_1, var_value_1)
        xml_str = xml_str.replace(var_name_2, var_value_2)
        xml_str = xml_str.replace(var_name_3, var_value_3)
        xml_str = xml_str.replace(var_name_4, var_value_4)
        xml_str = xml_str.replace(var_name_5, var_value_5)
        xml_str = xml_str.replace(var_name_6, var_value_6)
        xml_str = xml_str.replace(var_name_7, var_value_7)
        xml_str = xml_str.replace(var_name_8, var_value_8)

        # Replace the panel name/ID inside XML too.
        xml_str = xml_str.replace(original_xml_filename, f"{unique_id}_{original_xml_filename}")
    
        # Save the modified XML to a new file
        new_xml_filename = f"{unique_id}_{original_xml_filename}"
        new_xml_path = f"{out_folder_path}/{new_xml_filename}"  # Use out_folder_path for saving
        with open(new_xml_path, "w", encoding="utf-8") as new_xml_file:
            new_xml_file.write(xml_str)

        final_xml_path = f"{new_xml_path}.scx" # Suffix: ".scx"
        compute_math_of_XML(new_xml_path, final_xml_path)
    else:
        # Print a warning if the file does not exist
        print(f"Warning: The file {original_xml_path} does not exist.")

def main(csv_file_path, xml_folder_path, out_folder_path):
    # Check if it exists, delete and recreate it if it does, or create it if it doesn't
    if os.path.exists(out_folder_path):
        shutil.rmtree(out_folder_path)
    os.makedirs(out_folder_path)

    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, quotechar='"')
        for line in csv_reader:
            process_csv_line(line, xml_folder_path, out_folder_path)

if __name__ == "__main__":
    csv_file_path = 'CUTTING-LIST.csv'
    xml_folder_path = 'TEMPLATE'
    out_folder_path = 'CadFiles'  # Define the output folder path
    try:
        main(csv_file_path, xml_folder_path, out_folder_path)
    except Exception as Ex:
        print(Ex)

    # To prevent the window from closing immediately after run
    input("Finished. Press any key to continue . . .")
