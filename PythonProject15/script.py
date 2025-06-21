import argparse
import csv
from statistics import mean
from tabulate import tabulate

def main():
    parser = argparse.ArgumentParser(description='Обработка CSV с фильтрацией, агрегацией и сортировкой')
    parser.add_argument('--file', required=True, help='Путь к CSV файлу')
    parser.add_argument('--where', help='Условие для фильтрации, например: "price>100" или "brand=apple"')
    parser.add_argument('--aggregate', help='Агрегация, например: "rating=avg" или "price=min"')
    parser.add_argument('--order', help='Колонка для сортировки')
    parser.add_argument('--desc', action='store_true', help='Обратный порядок сортировки (desc)')
    args = parser.parse_args()

    with open(args.file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if args.where:
        condition = args.where.strip()
        if '=' in condition:
            col_name, value = condition.split('=', 1)
            op = '='
        elif '>' in condition:
            col_name, value = condition.split('>', 1)
            op = '>'
        elif '<' in condition:
            col_name, value = condition.split('<', 1)
            op = '<'
        else:
            raise ValueError('Некорректное условие фильтрации')
        col_name = col_name.strip()
        value = value.strip()

        def filter_func(row):
            cell = row[col_name]
            try:
                cell_num = float(cell)
                value_num = float(value)
                if op == '=':
                    return cell_num == value_num
                elif op == '>':
                    return cell_num > value_num
                elif op == '<':
                    return cell_num < value_num
            except ValueError:
                if op == '=':
                    return cell == value
                else:
                    return False
        rows = list(filter(filter_func, rows))

    if args.aggregate:
        col_name, agg_func = args.aggregate.split('=')
        col_name = col_name.strip()
        agg_func = agg_func.strip()

        values = []
        for row in rows:
            try:
                values.append(float(row[col_name]))
            except ValueError:
                pass

        if not values:
            print("Нет числовых данных для агрегации")
            return

        if agg_func == 'avg':
            result = mean(values)
        elif agg_func == 'min':
            result = min(values)
        elif agg_func == 'max':
            result = max(values)
        else:
            raise ValueError('Неизвестная функция агрегации')

        print(tabulate([[result]], headers=[f'{col_name} {agg_func}'], tablefmt='grid'))
        return

    if args.order:
        order_col = args.order
        reverse = args.desc
        if rows and order_col in rows[0]:
            try:
                rows.sort(key=lambda x: float(x[order_col]), reverse=reverse)
            except ValueError:
                rows.sort(key=lambda x: x[order_col], reverse=reverse)
        else:
            print(f"Колонки '{order_col}' нет в данных или данных нет.")
            return
    if rows:
        print(tabulate(rows, headers='keys', tablefmt='grid'))
    else:
        print("Нет данных для отображения")


if __name__ == '__main__':
    main()