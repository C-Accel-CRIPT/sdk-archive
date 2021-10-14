from typing import Callable, List, Dict, Optional


def save_html(html: str, path: str):
    with open(path, "w", encoding="utf-8") as file:
        file.write(html)


class DictTable(dict):

    def generate_html(self, title: Optional[str] = None, table_style: str = None):
        formater = self._get_table_formater()
        
        html = []
        html.append('<table class="styled-table">')

        if title is not None:
            html.append(f"<caption>{title}</caption>")
        html += formater()

        html.append("</table>")

        if table_style is not None:
            html.append(table_style)

        return ''.join(html)

    def _get_table_formater(self) -> Callable:
        if isinstance(list(self.values())[0], dict):
            return self._double_level_table
        else:
            return self._single_level_table

    def _single_level_table(self) -> List[str]:
        html = []

        # Headers
        headers = ["key", "Description"]
        html += self._generate_head(headers)

        # Rows
        html.append("<tbody>")
        for k, v in self.items():
            row_data = [k, v]
            html += self._generate_row(row_data)
        html.append("</tbody>")

        return html

    def _double_level_table(self) -> List[str]:
        html = []
        # Headers
        headers = self._get_headers()
        html += self._generate_head(headers)

        # Rows
        html.append("<tbody>")
        for k, v in self.items():
            row_data = [k] + self._get_row_data(v, headers)[1:]
            html += self._generate_row(row_data)
        html.append("</tbody>")

        return html

    def _get_headers(self) -> List[str]:
        headers = []
        for entry in self.values():
            for key in entry.keys():
                if key not in headers:
                    headers.append(key)

        headers.insert(0, "keys")
        return headers

    @staticmethod
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

    @staticmethod
    def _generate_row(row_data: List[str]) -> List[str]:
        html = ["<tr>"]
        for entry in row_data:
            html.append("<td>{0}</td>".format(entry))
        html.append("</tr>")
        return html

    @staticmethod
    def _generate_head(row_data: List[str]) -> List[str]:
        html = ["<thead>", "<tr>"]
        for entry in row_data:
            html.append("<th>{0}</th>".format(entry))
        html.append("</tr>")
        html.append("</thead>")
        return html


if __name__ == '__main__':
    style = '<style type="text/css"> ' \
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

    from src.cript.keys.cond import *
    from src.cript.keys.prop import *
    from src.cript.keys.data import *
    from src.cript.keys.material import *
    from src.cript.keys.process import *

    _dict = [
        [cond_keys, "condition_keys"],
        [prop_keys_rxn, "property_keys_reaction"],
        [prop_keys_poly, "property_keys_polymers"],
        [prop_keys_mat, "property_keys_materials"],
        [keys_methods, "method_keys"],
        [data_keys, "data_keys"],
        [keywords_material_p | keywords_material, "material_keys"],
        [Qty_keys | Rel_Qty_keys, "quantity_keys"],
        [Ingr_keys, "ingredient_keys"],
        [Process_keys, "process_keys"],
    ]

    for _ddict in _dict:
        html = DictTable(_ddict[0]).generate_html(title=_ddict[1].replace("_", " "), table_style=style)
        save_html(html, f"{_ddict[1]}.html")


    # _dict = keywords_material
    # a = DictTable(_dict).generate_html(title="test", table_style=style)
    # save_html(a, "test.html")


    print("done")
