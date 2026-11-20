from hypothesis import given, strategies as st
from processor import (
    lookup_drink_code,
    calculate_average_shot_cost,
    parse_order_modifiers
)


# Test 1: Drink code lookup
@given(st.text() | st.none())
def test_lookup_drink_code_no_crash(s):
    try:
        result = lookup_drink_code(s)

        # If accepted, result must be a valid menu price
        assert result in (3.00, 3.50, 4.00, 4.50, 5.00)

    except ValueError:
        # Invalid input is safely rejected
        pass
    except Exception as e:
        assert False, f"Unexpected crash: {e}"


# Test 2: Average shot cost
@given(st.text() | st.none())
def test_calculate_average_shot_cost_safe(s):
    try:
        result = calculate_average_shot_cost(s)

        assert isinstance(result, float)
        assert result >= 0

    except ValueError:
        # Invalid prices are safely rejected
        pass
    except Exception as e:
        assert False, f"Unexpected crash: {e}"


# Test 3: Order modifier parsing
@given(st.text() | st.none())
def test_parse_order_modifiers_safe(s):
    try:
        result = parse_order_modifiers(s)

        assert isinstance(result, dict)

        for key, value in result.items():
            assert key.strip() != ""
            assert value.strip() != ""

    except ValueError:
        # Malformed modifiers are safely rejected
        pass
    except Exception as e:
        assert False, f"Unexpected crash: {e}"
