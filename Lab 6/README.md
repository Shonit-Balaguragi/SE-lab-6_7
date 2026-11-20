# Lab 6 — Code and Branch Coverage

Install and run from this directory:

```bash
python -m pip install pytest coverage
python -m coverage erase
python -m coverage run --source=coffee_shop_order -m pytest -q CodeCoverageTest_coffee_shop_order.py
python -m coverage report -m
python -m coverage erase
python -m coverage run --branch --source=coffee_shop_order -m pytest -q BranchCoverageTest_coffee_shop_order.py
python -m coverage report -m
```

Capture terminal screenshots after running each report. The two separate test modules match the deliverables requested in the Lab 6 handout.
