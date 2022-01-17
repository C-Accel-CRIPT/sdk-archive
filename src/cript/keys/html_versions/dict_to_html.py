"""
Generates html tables for key tables.

"""

from typing import Callable, List, Dict, Optional, Union
from pathlib import Path

TABLE_STYLE = '<style type="text/css"> ' \
        'table.styled-table caption {padding-bottom: 0.5em; font-weight: bold; font-size: 28px;} ' \
        'table.styled-table {border-collapse: collapse; margin: 25px 0; font-size: ' \
        '0.9em; font-family: sans-serif; min-width: 400px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);} ' \
        'table.styled-table thead tr {background-color: #A31F34; color: #ffffff;text-align: left;} ' \
        'table.styled-table th {padding: 12px 15px;} ' \
        'table.styled-table td {padding: 12px 15px;} ' \
        'table.styled-table tr {border-bottom: 1px solid #dddddd;} ' \
        'table.styled-table tbody tr:last-of-type {border-bottom: 2px solid #A31F34;} ' \
        'table.styled-table tbody tr:nth-of-type(even) {background-color: #f3f3f3;} ' \
        '</style>'


def save_html(html: str, path: Union[Path, str] = "temp.html"):
    """ Saves html. """
    with open(path, "w", encoding="utf-8") as file:
        file.write(html)


def generate_html(dict_: dict, title: Optional[str] = None, table_style: str = None) -> str:
    """ Generates html from dictionary.

    Parameters
    ----------
    dict_: dict
        dictionary to be converted into a table
        single layer dict[str, str]
        double layer dict[str:dict]
    title: str
        title for table
    table_style: str
        html formatting of table

    Returns
    -------
    html: str
        table html

    """
    if not isinstance(dict_, dict):
        raise TypeError("Input must be a dictionary.")

    # start generating html table
    html = ['<table class="styled-table">']
    if title is not None:
        html.append(f"<caption>{title}</caption>")

    # generating main part of table
    formater = _get_table_formater(dict_)
    html += formater(dict_)

    # add formatting to table
    html.append("</table>")
    if table_style is not None:
        html.append(table_style)

    return ''.join(html)


def _get_table_formater(dict_) -> Callable:
    """ Determines weather the table is a single layer dict[str, str] or is a  double layer dict[str:dict]. """
    if isinstance(list(dict_.values())[0], dict):
        return _double_level_table
    else:
        return _single_level_table


def _single_level_table(dict_) -> List[str]:
    """ Generates main body of a table. """
    html = []

    # Headers
    headers = ["key", "Description"]
    html += _generate_head(headers)

    # Rows
    html.append("<tbody>")
    for k, v in dict_.items():
        row_data = [k, v]
        html += _generate_row(row_data)
    html.append("</tbody>")

    return html


def _double_level_table(dict_) -> List[str]:
    """ Generates main body of a table. """
    html = []
    # Headers
    headers = _get_headers(dict_)
    html += _generate_head(headers)

    # Rows
    html.append("<tbody>")
    for k, v in dict_.items():
        row_data = [k] + _get_row_data(v, headers)[1:]
        html += _generate_row(row_data)
    html.append("</tbody>")

    return html


def _get_headers(dict_) -> List[str]:
    headers = []
    for entry in dict_.values():
        for key in entry.keys():
            if key not in headers:
                headers.append(key)

    headers.insert(0, "keys")
    return headers


def _get_row_data(row_dict: Dict, headers: List[str]) -> List[str]:
    row = []
    for header in headers:
        if header in row_dict:
            if str(row_dict[header]) == "<class 'pint.quantity.build_quantity_class.<locals>.Quantity'>":
                row.append("Quantity")
            elif str(row_dict[header]) == "<class 'src.cript.material.Unit'>":
                row.append("Unit")
            elif str(row_dict[header]) == "<class 'src.cript.material.Material'>":
                row.append("Material")
            else:
                row.append(row_dict[header])
        else:
            row.append(" ")

    return row


def _generate_row(row_data: List[str]) -> List[str]:
    html = ["<tr>"]
    for entry in row_data:
        html.append("<td>{0}</td>".format(entry))
    html.append("</tr>")
    return html


def _generate_head(row_data: List[str]) -> List[str]:
    html = ["<thead>", "<tr>"]
    for entry in row_data:
        html.append("<th>{0}</th>".format(entry))
    html.append("</tr>")
    html.append("</thead>")
    return html


def generate_all_CRIPT_html():
    """ Generates html for all of CRIPT keys. """
    from cript.keys.cond import cond_keys
    from cript.keys.prop import property_process_keys, property_material_keys
    from cript.keys.methods import method_keys
    from cript.keys.data import data_keys
    from cript.keys.material import material_keywords
    from cript.keys.process import process_keywords
    from cript.keys.ingr import ingredient_keywords

    list_of_dict = [
        [cond_keys, "cond_keys"],
        [property_process_keys, "property_process_keys"],
        [property_material_keys, "property_material_keys"],
        [method_keys, "method_keys"],
        [data_keys, "data_keys"],
        [material_keywords, "material_keywords"],
        [ingredient_keywords, "ingredient_keywords"],
        [process_keywords, "process_keywords"],
    ]

    for dict_ in list_of_dict:
        html = generate_html(dict_[0], title=dict_[1].replace("_", " "), table_style=TABLE_STYLE)
        save_html(html, f"{dict_[1]}.html")
        print("Saved: " + dict_[1])

    print("done")


if __name__ == '__main__':
    generate_all_CRIPT_html()
