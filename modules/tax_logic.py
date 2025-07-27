def calculate_tax(income, filing_status='single'):
    income = float(income)

    # 2024 standard deductions
    standard_deductions = {
        'single': 14600,
        'married_joint': 29200,
        'married_separate': 14600,
        'head': 21900
    }

    deduction = standard_deductions.get(filing_status, 14600)
    taxable_income = max(0, income - deduction)

    # 2024 IRS tax brackets for 'single' (add others later if needed)
    brackets = [
        (0, 11600, 0.10),
        (11600, 47150, 0.12),
        (47150, 100525, 0.22),
        (100525, 191950, 0.24),
        (191950, 243725, 0.32),
        (243725, 609350, 0.35),
        (609350, float('inf'), 0.37)
    ]

    tax_due = 0
    for lower, upper, rate in brackets:
        if taxable_income > lower:
            taxed_amount = min(taxable_income, upper) - lower
            tax_due += taxed_amount * rate
        else:
            break

    return round(tax_due, 2), deduction, taxable_income
