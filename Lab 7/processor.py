import math


def lookup_drink_code(code_string):
    if not isinstance(code_string, str):
        raise ValueError("Drink code must be a string")

    code_prefix = code_string.strip().upper()[:3]

    menu_prices = {
        "LAT": 4.50,
        "CAP": 4.00,
        "ESP": 3.00,
        "AME": 3.50,
        "MOC": 5.00
    }

    if code_prefix not in menu_prices:
        raise ValueError("Unknown drink code")

    return menu_prices[code_prefix]


def calculate_average_shot_cost(pricing_csv):
    if not isinstance(pricing_csv, str) or not pricing_csv.strip():
        raise ValueError("Pricing CSV must be a non-empty string")

    try:
        prices = [float(p.strip()) for p in pricing_csv.split(',')]
    except (ValueError, TypeError):
        raise ValueError("All shot prices must be valid numbers")

    if not prices:
        raise ValueError("At least one price is required")

    if any(not math.isfinite(price) or price < 0 for price in prices):
        raise ValueError("Prices must be finite and non-negative")

    return sum(prices) / len(prices)


def parse_order_modifiers(order_spec):
    if not isinstance(order_spec, str) or not order_spec.strip():
        raise ValueError("Order specification must be a non-empty string")

    modifier_dict = {}

    for item in order_spec.split(';'):
        if not item.strip():
            raise ValueError("Empty modifier is not allowed")

        if item.count(':') != 1:
            raise ValueError("Each modifier must contain exactly one colon")

        key, value = item.split(':')
        key = key.strip()
        value = value.strip()

        if not key or not value:
            raise ValueError("Modifier key and value cannot be empty")

        if key in modifier_dict:
            raise ValueError("Duplicate modifier key")

        modifier_dict[key] = value

    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    try:
        price = lookup_drink_code(drink_input)
        print("Base Price: $", price)
    except ValueError as e:
        print("Invalid drink code:", e)
        return

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    try:
        avg_price = calculate_average_shot_cost(shots_input)
        print("Average Shot Price: $", avg_price)
    except ValueError as e:
        print("Invalid shot prices:", e)
        return

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    try:
        mods = parse_order_modifiers(spec_input)
        print("Parsed Modifiers:", mods)
    except ValueError as e:
        print("Invalid order modifiers:", e)


if __name__ == "__main__":
    main()
