def auto_cap(key, _frame, _roi):

    import capture

    switcher = {
        0: capture('Anjali', _frame, _roi),
        1: capture('Dhyana', _frame, _roi),
        2: capture('Gyan', _frame, _roi),
        3: capture('Mushti', _frame, _roi),
        4: capture('Vayu', _frame, _roi),
        5: capture('Misc', _frame, _roi)

    }

    return switcher.get(key, 'auto_cap error statement here')

