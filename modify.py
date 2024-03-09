import csv
from xml.etree import ElementTree as ET

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

def process_csv_line(line, xml_folder_path):
    unique_id, original_xml_filename, var_name_1, var_value_1, var_name_2, var_value_2 = line
    # Evaluate mathematical expressions in variable values
    var_value_1 = evaluate_math(var_value_1)
    var_value_2 = evaluate_math(var_value_2)
    
    # Construct the path to the original XML file
    original_xml_path = f"{xml_folder_path}/{original_xml_filename}.scx" # Suffix: ".scx"
    # Load the XML file
    tree = ET.parse(original_xml_path)
    root = tree.getroot()
    
    # Replace variable names with their corresponding values
    xml_str = ET.tostring(root, encoding='unicode')
    xml_str = xml_str.replace(var_name_1, var_value_1)
    xml_str = xml_str.replace(var_name_2, var_value_2)
    
    # Save the modified XML to a new file
    new_xml_filename = f"{unique_id}_{original_xml_filename}"
    new_xml_path = f"{xml_folder_path}/{new_xml_filename}"
    with open(new_xml_path, "w", encoding="utf-8") as new_xml_file:
        new_xml_file.write(xml_str)

    final_xml_path = f"{new_xml_path}.scx" # Suffix: ".scx"
    compute_math_of_XML(new_xml_path, final_xml_path)

def main(csv_file_path, xml_folder_path):
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, quotechar='"')
        for line in csv_reader:
            process_csv_line(line, xml_folder_path)

if __name__ == "__main__":
    csv_file_path = 'CUTTING-LIST.csv'
    xml_folder_path = 'TEMPLATE'
    main(csv_file_path, xml_folder_path)
    # To prevent the window from closing immediately after run
    input("Finished. Press any key to continue . . .")
