def pytest_collection_modifyitems(config, items):
    """
        This function is called by pytest after collecting all tests.
        It is used to order the tests in the following order:
            1. Unit tests
            2. Integration tests
    """
    ordered_items = []
    unit_tests = []
    integration_tests = []

    for item in items:
        if "test/unit" in item.fspath.strpath:
            unit_tests.append(item)
        elif "test/integration" in item.fspath.strpath:
            integration_tests.append(item)
        else:
            ordered_items.append(item)

    ordered_items.extend(unit_tests)
    ordered_items.extend(integration_tests)

    # Update items list with ordered tests
    items[:] = ordered_items
