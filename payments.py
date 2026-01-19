"""
def get_payment_message():
    return "Upgrade to PRO to unlock charts, reports & downloads"
"""
"""
UPI_ID = "9587269281@ybl"

def get_payment(plan):
    prices = {
        "MONTHLY": 499,
        "YEARLY": 4999
    }
    return UPI_ID, prices.get(plan, 0)
"""

# payments.py

UPI_ID = "9587269281@ybl"

def get_payment_message():
    return f"""
### 🔒 Upgrade Required

Your current plan does not allow this feature.

### 💳 Pricing
- Monthly Plan: ₹499
- Yearly Plan: ₹4999

### 📲 Pay via UPI
**{UPI_ID}**

After payment, contact admin to activate your plan.
"""
