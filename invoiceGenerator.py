"""
====================================================================
 JIRA: SVC-1950 — Fix Invoice PDF Generation Alignment
====================================================================
 P1 | Points: 2 | Labels: client, python

 Invoice PDF has misaligned columns. Currency formatting wrong
 (1000 shows as 1000 instead of 1,000.00). Tax calculation rounds
 per line item instead of on total.

 ACCEPTANCE CRITERIA:
 - [ ] Currency formatted with commas and 2 decimal places
 - [ ] Tax calculated on subtotal (not sum of per-line tax)
 - [ ] Line items aligned in columns
====================================================================
"""

class InvoiceGenerator:
    def __init__(self, tax_rate=0.1):
        self.tax_rate = tax_rate
        self.line_items = []

    def add_item(self, description, quantity, unit_price):
        self.line_items.append({
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'total': quantity * unit_price,
        })

    def calculate_subtotal(self):
        return sum(item['total'] for item in self.line_items)

    def calculate_tax(self):
        # Example: 3 items at $10.03 → per-item tax rounds differently than total tax
        total_tax = 0
        for item in self.line_items:
            total_tax += round(item['total'] * self.tax_rate, 2)
        return total_tax
        # Should be: round(self.calculate_subtotal() * self.tax_rate, 2)

    def format_currency(self, amount):
        return f"${amount}"
        # Should be: f"${amount:,.2f}"

    def generate(self):
        lines = ["INVOICE", "=" * 60]
        for item in self.line_items:
            lines.append(
                f"{item['description']} x{item['quantity']} @ {self.format_currency(item['unit_price'])} = {self.format_currency(item['total'])}"
            )

        subtotal = self.calculate_subtotal()
        tax = self.calculate_tax()
        lines.append(f"\nSubtotal: {self.format_currency(subtotal)}")
        lines.append(f"Tax ({self.tax_rate * 100}%): {self.format_currency(tax)}")
        lines.append(f"Total: {self.format_currency(subtotal + tax)}")

        return '\n'.join(lines)


# Tests
if __name__ == '__main__':
    inv = InvoiceGenerator(tax_rate=0.1)
    inv.add_item("Widget A", 3, 10.03)
    inv.add_item("Widget B", 2, 1000.50)

    assert inv.format_currency(1000.5) == "$1,000.50", \
        f"FAIL: Got {inv.format_currency(1000.5)}"
    print(inv.generate())
