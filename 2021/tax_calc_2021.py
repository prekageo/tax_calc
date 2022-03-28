#!/usr/bin/env python3

import math
import re
from decimal import Decimal as D


dollar_rounding = False

y2020_f1040_11 = D(0)
y2020_f1040_24 = D(0)
children = 1
children_under_6 = 0
letter_6419 = D(0)
W2_1 = D(120000)  # Wages, tips, other comp.
W2_2 = D(0)  # Federal income tax withheld
W2_5 = D(0)  # Medicare wages and tips
W2_6 = D(0)  # Medicare tax withheld
f1099_INT_1 = []
f1099_DIV_1a = []
f1099_DIV_1b = []
f1099_DIV_5 = []
f1099_DIV_2a = []
f1099_DIV_7 = []
f1099_b_cost_reported_1d = []
f1099_b_cost_reported_1e = []
f1099_b_cost_reported_1g = []
f1099_b_cost_not_reported_1d = []
f1099_b_cost_not_reported_1e = []
f1099_b_cost_not_reported_1g = []
f1099_b_not_reported_1d = []
f1099_b_not_reported_1e = []
f1099_b_not_reported_1g = []
f1099_INT_1.append(D(0))  # Interest Income

f1099_DIV_1a.append(D(1))  # Total Ordinary Dividends
f1099_DIV_1b.append(D(1))  # Qualified Dividends
f1099_DIV_2a.append(D(1))  # Total Capital Gain Distributions
f1099_DIV_5.append(D(0))  # Section 199A Dividends
f1099_DIV_7.append(D(0))  # Foreign Tax Paid
f1099_b_cost_reported_1d.append(D(1))  # Total Proceeds (Short-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS)
f1099_b_cost_reported_1e.append(D(0))  # Total Cost Basis (Short-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS)
f1099_b_cost_reported_1g.append(D(0))  # Wash Sale Loss Disallowed (Short-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS)
f1099_b_cost_not_reported_1d.append(D(0))  # Total Proceeds (Short-term transactions reported on Form(s) 1099-B showing basis wasn’t reported to the IRS)
f1099_b_cost_not_reported_1e.append(D(0))  # Total Cost Basis (Short-term transactions reported on Form(s) 1099-B showing basis wasn’t reported to the IRS)
f1099_b_cost_not_reported_1g.append(D(0))  # Wash Sale Loss Disallowed (Short-term transactions reported on Form(s) 1099-B showing basis wasn’t reported to the IRS)

f1099_b_not_reported_1d.append(D(0))  # Total Proceeds
f1099_b_not_reported_1e.append(D(0))  # Total Cost Basis
f1099_b_not_reported_1g.append(D(0))  # Wash Sale Loss Disallowed

def sortfunc(kv):
    k = kv[0]
    parts = k.split('_')
    ret = []
    for p in parts:
        m = re.match(r'(?P<num>[0-9]*)(?P<str>.*)', p)
        if len(m.group('num')) > 0:
            ret.extend(['', int(m.group('num'))])
        ret.append(m.group('str'))
    return ret


def print_vars(variables):
    for x, y in sorted(variables, key=sortfunc):
        if isinstance(y, D):
            if dollar_rounding:
                print(f'{x:20} {y:10.0f}')
            else:
                print(f'{x:20} {y:10.2f}')
        elif isinstance(y, int):
            print(f'{x:20} {y:7d}')
        elif callable(y) or x in ('__loader__'):
            pass
        else:
            print(x, y)


def tax(v):
    if   0      <= v < 19900 : ret = (v - 0     ) * D('0.10')
    elif 19900  <= v < 81050 : ret = (v - 19900 ) * D('0.12') + 1990
    elif 81050  <= v < 172750: ret = (v - 81050 ) * D('0.22') + 9328
    elif 172750 <= v < 329850: ret = (v - 172750) * D('0.24') + 29502
    elif 329850 <= v < 418850: ret = (v - 329850) * D('0.32') + 67206
    elif 418850 <= v < 628300: ret = (v - 418850) * D('0.35') + 95686
    elif 628300 <= v         : ret = (v - 628300) * D('0.37') + D('168993.50')

    return ret


def roundup(x, multiple=1000):
    value = x
    value = D(math.ceil(value / multiple)) * multiple
    return value


# Form 8949 Sales and Other Dispositions of Capital Assets (Box A)
f8949_a_1a = ''  # Description of property
f8949_a_1b = ''  # Date acquired
f8949_a_1c = ''  # Date sold or disposed of
f8949_a_1d = sum(f1099_b_cost_reported_1d)  # Proceeds (sales price) (see instructions)
f8949_a_1e = sum(f1099_b_cost_reported_1e)  # Cost or other basis. See the Note below and see Column (e) in the separate instructions
f8949_a_1g = sum(f1099_b_cost_reported_1g)  # Amount of adjustment
f8949_a_1h = f8949_a_1d - f8949_a_1e + sum(f1099_b_cost_reported_1g)
f8949_a_2d = f8949_a_1d
f8949_a_2e = f8949_a_1e
f8949_a_2g = f8949_a_1g
f8949_a_2h = f8949_a_1h

if dollar_rounding:
    f8949_a_2d = round(f8949_a_2d)
    f8949_a_2e = round(f8949_a_2e)
    f8949_a_2g = round(f8949_a_2g)
    f8949_a_2h = round(f8949_a_2h)

# Form 8949 Sales and Other Dispositions of Capital Assets (Box B)
f8949_b_1a = ''  # Description of property
f8949_b_1b = ''  # Date acquired
f8949_b_1c = ''  # Date sold or disposed of
f8949_b_1d = sum(f1099_b_cost_not_reported_1d)  # Proceeds (sales price) (see instructions)
f8949_b_1e = sum(f1099_b_cost_not_reported_1e)  # Cost or other basis. See the Note below and see Column (e) in the separate instructions
f8949_b_1g = sum(f1099_b_cost_not_reported_1g)  # Amount of adjustment
f8949_b_1h = f8949_b_1d - f8949_b_1e + sum(f1099_b_cost_not_reported_1g)
f8949_b_2d = f8949_b_1d
f8949_b_2e = f8949_b_1e
f8949_b_2g = f8949_b_1g
f8949_b_2h = f8949_b_1h

if dollar_rounding:
    f8949_b_2d = round(f8949_b_2d)
    f8949_b_2e = round(f8949_b_2e)
    f8949_b_2g = round(f8949_b_2g)
    f8949_b_2h = round(f8949_b_2h)

# Form 8949 Sales and Other Dispositions of Capital Assets (Box C)
f8949_c_1a = ''  # Description of property
f8949_c_1b = ''  # Date acquired
f8949_c_1c = ''  # Date sold or disposed of
f8949_c_1d = sum(f1099_b_not_reported_1d)  # Proceeds (sales price) (see instructions)
f8949_c_1e = sum(f1099_b_not_reported_1e)  # Cost or other basis. See the Note below and see Column (e) in the separate instructions
f8949_c_1g = sum(f1099_b_not_reported_1g)  # Amount of adjustment
f8949_c_1h = f8949_c_1d - f8949_c_1e + sum(f1099_b_not_reported_1g)
f8949_c_2d = f8949_c_1d
f8949_c_2e = f8949_c_1e
f8949_c_2g = f8949_c_1g
f8949_c_2h = f8949_c_1h

if dollar_rounding:
    f8949_c_2d = round(f8949_c_2d)
    f8949_c_2e = round(f8949_c_2e)
    f8949_c_2g = round(f8949_c_2g)
    f8949_c_2h = round(f8949_c_2h)

# Form 1040 SCHEDULE D Capital Gains and Losses
schedule_d_1b_d = f8949_a_2d
schedule_d_1b_e = f8949_a_2e
schedule_d_1b_g = f8949_a_2g
schedule_d_1b_h = f8949_a_2h
schedule_d_2_d = f8949_b_2d
schedule_d_2_e = f8949_b_2e
schedule_d_2_g = f8949_b_2g
schedule_d_2_h = f8949_b_2h
schedule_d_3_d = f8949_c_2d
schedule_d_3_e = f8949_c_2e
schedule_d_3_g = f8949_c_2g
schedule_d_3_h = f8949_c_2h
schedule_d_7 = schedule_d_1b_h + schedule_d_2_h + schedule_d_3_h  # Net short-term capital gain or (loss). Combine lines 1a through 6 in column (h).
schedule_d_13 = sum(f1099_DIV_2a)  # Capital gain distributions
if dollar_rounding:
    schedule_d_13 = round(schedule_d_13)
schedule_d_15 = schedule_d_13  # Net long-term capital gain or (loss). Combine lines 8a through 14 in column (h).
schedule_d_16 = schedule_d_7 + schedule_d_15  # Combine lines 7 and 15
schedule_d_18 = D(0)
schedule_d_19 = D(0)
if schedule_d_16 > 0:
    schedule_d_17 = 'Yes' if schedule_d_15 > 0 and schedule_d_16 > 0 else 'No'
    assert schedule_d_17 == 'Yes'
    schedule_d_20 = 'Yes' if schedule_d_18 == 0 and schedule_d_19 == 0 else 'No'
    # 28% Rate Gain Worksheet might be needed for You reported in Part II of Form 8949 a section 1202 exclusion from the eligible gain on QSB stock
    f1040_7 = schedule_d_16  # Capital gain or (loss)
else:
    assert False
    schedule_d_21 = max(-3000, schedule_d_16)
    schedule_d_20 = 'Yes' if f1040_3a > 0 else 'No'
    f1040_7 = schedule_d_21  # Capital gain or (loss)

# Form 8959 Additional Medicare Tax
f8959_1 = W2_5  # Medicare wages and tips
f8959_2 = D(0)  # Unreported tips from Form 4137, line 6
f8959_3 = D(0)  # Wages from Form 8919, line 6
f8959_4 = f8959_1 + f8959_2 + f8959_3  # Add lines 1 through 3
f8959_5 = D('250000')  # Enter the following amount for your filing status:
f8959_6 = max(0, f8959_4 - f8959_5)  # Subtract line 5 from line 4. If zero or less, enter -0-
f8959_7 = f8959_6 * D('0.009')  # Additional Medicare Tax on Medicare wages. Multiply line 6 by 0.9% (0.009).
f8959_18 = f8959_7  # Add lines 7, 13, and 17. Also include this amount on Schedule 2 (Form 1040 ), line 11
f8959_19 = W2_6  # Medicare tax withheld from Form W-2, box 6.
if dollar_rounding:
    f8959_19 = round(f8959_19)
f8959_20 = f8959_1  # Medicare tax withheld from Form W-2, box 6.
f8959_21 = f8959_20 * D('1.45') / 100  # Multiply line 20 by 1.45% (0.0145). This is your regular Medicare tax withholding on Medicare wages
if dollar_rounding:
    f8959_21 = round(f8959_21)
f8959_22 = f8959_19 - f8959_21  # Subtract line 21 from line 19. If zero or less, enter -0-. This is your Additional Medicare Tax withholding on Medicare wages
f8959_23 = D(0)  # Additional Medicare Tax withholding on railroad retirement (RRTA) compensation from Form W-2, box 14
f8959_24 = f8959_22  # Total Additional Medicare Tax withholding. Add lines 22 and 23. Also include this amount with federal income tax withholding on Form 1040, 1040-SR, or 1040-NR, line 25c

# Form 1040 Schedule 3 Additional Credits and Payments
schedule_3_1 = sum(f1099_DIV_7)
if schedule_3_1 > 0:
    schedule_3_1 = sum(f1099_DIV_7)  # Foreign tax credit. Attach Form 1116 if required
    # Credit for child and dependent care expenses from Form 2441, line 11. Attach Form 2441
    if schedule_3_1 >= 600:
        print('submit 1116')
    schedule_3_8 = schedule_3_1  # Add lines 1 through 5 and 7. Enter here and on Form 1040, 1040-SR, or 1040-NR, line 20
    if dollar_rounding:
        schedule_3_8 = round(schedule_3_8)
else:
    schedule_3_8 = 0

# Form 1040
f1040_1 = W2_1  # Wages, salaries, tips, etc.
f1040_2b = sum(f1099_INT_1)  # Taxable interest
if f1040_2b > 1500:
    print('attach schedule b')
f1040_3a = sum(f1099_DIV_1b)  # Qualified dividends
f1040_3b = sum(f1099_DIV_1a)  # Ordinary dividends,
if f1040_3b > 1500:
    print('attach schedule b')
f1040_9 = f1040_1 + f1040_2b + f1040_3b + f1040_7  # Total Income
f1040_11 = f1040_9  # Adjusted Gross Income,
if f1040_11 > 250000:
    print('attach form 8960')
f1040_12a = D('25100')  # Standard deduction
f1040_12c = f1040_12a  # Add lines 12a and 12b

if f1040_11 - f1040_12c < 329800:
    # Form 8995 Qualified Business Income Deduction Simplified Computation
    # Use this form if your taxable income, before your qualified business income deduction, is at or below $164,900 ($164,925 if married filing separately; $329,800 if married filing jointly), and you aren’t a patron of an agricultural or horticultural cooperative.
    f8995_5 = D(0)
    f8995_7 = D(0)
    f8995_6 = sum(f1099_DIV_5)
    f8995_8 = max(0, f8995_6 + f8995_7)
    f8995_9 = f8995_8 * D('0.20')
    f8995_10 = f8995_5 + f8995_9
    f8995_11 = f1040_11 - f1040_12c
    f8995_12 = f1040_3a + min(schedule_d_15, schedule_d_16)
    f8995_13 = max(0, f8995_11 - f8995_12)
    f8995_14 = f8995_13 * D('0.20')
    f8995_15 = min(f8995_10, f8995_14)
else:
    # Form 8995-A Qualified Business Income Deduction
    # Use this form if your taxable income, before your qualified business income deduction, is above $164,900 ($164,925 if married filing separately; $329,800 if married filing jointly), or you’re a patron of an agricultural or horticultural cooperative.
    f8995_a_16 = 0  # Total qualified business income component. Add all amounts reported on line 15
    f8995_a_27 = f8995_a_16  # Total qualified business income component from all qualified trades, businesses, or aggregations. Enter the amount from line 16
    f8995_a_28 = sum(f1099_DIV_5)  # Qualified REIT dividends and publicly traded partnership (PTP) income or (loss). See instructions
    f8995_a_29 = 0  # Qualified REIT dividends and PTP (loss) carryforward from prior years
    f8995_a_30 = max(0, f8995_a_28 + f8995_a_29)  # Total qualified REIT dividends and PTP income. Combine lines 28 and 29. If less than zero, enter -0-
    f8995_a_31 = f8995_a_30 * D('0.20')  # REIT and PTP component. Multiply line 30 by 20% (0.20)
    f8995_a_32 = f8995_a_27 + f8995_a_31  # Qualified business income deduction before the income limitation. Add lines 27 and 31
    f8995_a_33 = f1040_11 - f1040_12c  # Taxable income before qualified business income deduction
    f8995_a_34 = f1040_3a + max(0, min(schedule_d_15, schedule_d_16))  # Net capital gain. See instructions
    f8995_a_35 = max(0, f8995_a_33 - f8995_a_34)  # Subtract line 34 from line 33. If zero or less, enter -0-
    f8995_a_36 = f8995_a_35 * D('0.20')  # Income limitation. Multiply line 35 by 20% (0.20)
    f8995_a_37 = min(f8995_a_32, f8995_a_36)  # Qualified business income deduction before the domestic production activities deduction (DPAD) under section 199A(g). Enter the smaller of line 32 or line 36
    f8995_a_38 = 0  # DPAD under section 199A(g) allocated from an agricultural or horticultural cooperative. Don’t enter more than line 33 minus line 37
    f8995_a_39 = f8995_a_37 + f8995_a_38  # Total qualified business income deduction. Add lines 37 and 38
    if dollar_rounding:
        f8995_a_39 = round(f8995_a_39)

# Form 1040
if f1040_11 - f1040_12c < 329800:
    f1040_13 = f8995_15  # Qualified business income deduction from Form 8995 or Form 8995-A
else:
    f1040_13 = f8995_a_39  # Qualified business income deduction from Form 8995 or Form 8995-A
f1040_14 = f1040_12c + f1040_13  # Add lines 12c and 13
f1040_15 = max(0, f1040_11 - f1040_14)  # Taxable income

# Form 8960 Net Investment Income Tax — Individuals, Estates, and Trusts
f8960_1 = f1040_2b  # Taxable interest (see instructions
f8960_2 = f1040_3b  # Ordinary dividends (see instructions
f8960_5a = f1040_7  # Net gain or loss from disposition of property (see instructions)
f8960_5d = f8960_5a  # Combine lines 5a through 5c
f8960_8 = f8960_2 + f8960_1 + f8960_5d  # Total investment income. Combine lines 1, 2, 3, 4c, 5d, 6, and 7
f8960_12 = f8960_8  # Net investment income. Subtract Part II, line 11, from Part I, line 8. Individuals, complete lines 13–17.
f8960_13 = f1040_11  # Modified adjusted gross income (see instructions)
f8960_14 = D('250000')  # Threshold based on filing status (see instructions)
f8960_15 = max(0, f8960_13 - f8960_14)  # Subtract line 14 from line 13. If zero or less, enter -0-
f8960_16 = min(f8960_12, f8960_15)  # Enter the smaller of line 12 or line 15
f8960_17 = f8960_16 * D('3.8') / 100  # Net investment income tax for individuals. Multiply line 16 by 3.8% (0.038). Enter here and include on your tax return (see instructions)

# Worksheet Qualified Dividends and Capital Gain Tax Worksheet
QDCGTW_1 = f1040_15  # income Enter the amount from Form 1040 or 1040-SR, line 15. However, if you are filing Form 2555 (relating to foreign earned income), enter the amount from line 3 of the Foreign Earned Income Tax Worksheet
QDCGTW_2 = f1040_3a  # qual.div. Enter the amount from Form 1040 or 1040-SR, line 3a
QDCGTW_3 = max(0, min(schedule_d_15, schedule_d_16))  # max(0, long.term.gain + min(0,short.term.gain))==cap.gain. Enter the smaller of line 15 or 16 of Schedule D. If either line 15 or 16 is blank or a loss, enter -0-.
QDCGTW_4 = QDCGTW_3 + QDCGTW_2  # qual.div.+cap.gain. Add lines 2 and 3
QDCGTW_5 = max(0, QDCGTW_1 - QDCGTW_4)  # income-qual.div.-cap.gain. Subtract line 4 from line 1. If zero or less, enter -0-
QDCGTW_6 = D('80800')
QDCGTW_7 = min(QDCGTW_6, QDCGTW_1)  # 80k Enter the smaller of line 1 or line 6
QDCGTW_8 = min(QDCGTW_5, QDCGTW_7)  # 80k Enter the smaller of line 5 or line 7
QDCGTW_9 = QDCGTW_7 - QDCGTW_8  # 0 Subtract line 8 from line 7. This amount is taxed at 0%
QDCGTW_10 = min(QDCGTW_4, QDCGTW_1)  # qual.div.+cap.gain. Enter the smaller of line 1 or line 4
QDCGTW_11 = QDCGTW_9  # 0 Enter the amount from line 9
QDCGTW_12 = QDCGTW_10 - QDCGTW_11  # qual.div.+cap.gain. Subtract line 11 from line 10
QDCGTW_13 = D('501600')
QDCGTW_14 = min(QDCGTW_13, QDCGTW_1)  # income Enter the smaller of line 1 or line 13
QDCGTW_15 = QDCGTW_5 + QDCGTW_9  # income-qual.div.-cap.gain. Add lines 5 and 9
QDCGTW_16 = max(0, QDCGTW_14 - QDCGTW_15)  # qual.div.+cap.gain. Subtract line 15 from line 14. If zero or less, enter -0-
QDCGTW_17 = min(QDCGTW_12, QDCGTW_16)  # qual.div.+cap.gain. Enter the smaller of line 12 or line 16
QDCGTW_18 = QDCGTW_17 * D('0.15')  # Multiply line 17 by 15% (0.15)
QDCGTW_19 = QDCGTW_9 + QDCGTW_17  # Add lines 9 and 17
QDCGTW_20 = QDCGTW_10 - QDCGTW_19  # Subtract line 19 from line 10
QDCGTW_21 = QDCGTW_20 * D('0.20')  # Multiply line 20 by 20% (0.20)
QDCGTW_22 = tax(QDCGTW_5)  # Figure the tax on the amount on line 5
QDCGTW_23 = QDCGTW_18 + QDCGTW_21 + QDCGTW_22  # Add lines 18, 21, and 22
QDCGTW_24 = tax(QDCGTW_1)  # Figure the tax on the amount on line 1
QDCGTW_25 = min(QDCGTW_23, QDCGTW_24)  # Tax on all taxable income. Enter the smaller of line 23 or 24

# Form 1040
f1040_16 = round(QDCGTW_25, 2)  # Tax
if dollar_rounding:
    f1040_16 = round(f1040_16)

# Form 1040 (SCHEDULE 2) Additional Taxes
schedule_2_2 = 0  # Excess advance premium tax credit repayment. Attach Form 8962

# Worksheet To See if You Should Fill in Form 6251—Schedule 2, Line 1
worksheet_6251_3 = f1040_11 - f1040_13  # subtract Form 1040 or 1040-SR, line 13, or Form 1040-NR, line 13a, from Form 1040, 1040-SR, or 1040-NR, line 11
worksheet_6251_4 = 0  # Enter any tax refund from Schedule 1, lines 1 and 8z
worksheet_6251_5 = worksheet_6251_3 - worksheet_6251_4  # Subtract line 4 from line 3
worksheet_6251_6 = D(114600)  # Enter the amount shown below for your filing status
worksheet_6251_7 = worksheet_6251_5 - worksheet_6251_6  # Subtract line 6 from line 5
assert worksheet_6251_7 > 0
worksheet_6251_8 = D(1047200)  # Enter the amount shown below for your filing status.
assert worksheet_6251_5 <= worksheet_6251_8
worksheet_6251_9 = 0  # Is the amount on line 5 more than the amount on line 8? Enter -0-.
worksheet_6251_10 = min(worksheet_6251_6, worksheet_6251_9 * D('0.25'))  # Multiply line 9 by 25% (0.25) and enter the smaller of the result or line 6
worksheet_6251_11 = worksheet_6251_7 + worksheet_6251_10  # Add lines 7 and 10
if worksheet_6251_11 > D(199900):  # Is the amount on line 11 more than $199,900
    print('fill in form 6251')

# Form 6251 Alternative Minimum Tax—Individuals
assert f1040_15 > 0
f6251_1 = f1040_15  # Enter the amount from Form 1040 or 1040-SR, line 15, if more than zero. If Form 1040 or 1040-SR, line 15, is zero, subtract lines 12 and 13 of Form 1040 or 1040-SR from line 11 of Form 1040 or 1040-SR and enter the result here. (If less than zero, enter as a negative amount.)
f6251_2a = f1040_12a  # If filing Schedule A (Form 1040), enter the taxes from Schedule A, line 7; otherwise, enter the amount from Form 1040 or 1040-SR, line 12a
f6251_4 = f6251_1 + f6251_2a  # Alternative minimum taxable income. Combine lines 1 through 3. (If married filing separately and line 4 is more than $752,800, see instructions.
assert f6251_4 < D('1047200')
f6251_5 = D('114600')
f6251_6 = f6251_4 - f6251_5  # Subtract line 5 from line 4.
assert f6251_6 > 0
assert f1040_3a > 0

# Form 6251 Alternative Minimum Tax—Individuals (Part III)
f6251_12 = f6251_6  # Enter the amount from Form 6251, line 6.
f6251_13 = QDCGTW_4  # Enter the amount from line 4 of the Qualified Dividends and Capital Gain Tax Worksheet in the Instructions for Form 1040
f6251_14 = schedule_d_19  # Enter the amount from Schedule D (Form 1040), line 19 (as refigured for the AMT, if necessary).
f6251_15 = f6251_13  # If you did not complete a Schedule D Tax Worksheet for the regular tax or the AMT, enter the amount from line 13.
f6251_16 = min(f6251_12, f6251_15)  # Enter the smaller of line 12 or line 15
f6251_17 = f6251_12 - f6251_16  # Subtract line 16 from line 12
if f6251_17 <= 199900:
    f6251_18 = f6251_17 * D('0.26')  # If line 17 is $199,900 or less ($99,950 or less if married filing separately), multiply line 17 by 26% (0.26).
else:
    f6251_18 = f6251_17 * D('0.28') - 3998  # Otherwise, multiply line 17 by 28% (0.28) and subtract $3,998 ($1,999 if married filing separately) from the result
f6251_19 = D('80800')
f6251_20 = QDCGTW_5  # Enter the amount from line 5 of the Qualified Dividends and Capital Gain Tax Worksheet
f6251_21 = max(0, f6251_19 - f6251_20)  # Subtract line 20 from line 19. If zero or less, enter -0-
f6251_22 = min(f6251_12, f6251_13)  # Enter the smaller of line 12 or line 13
f6251_23 = min(f6251_21, f6251_22)  # Enter the smaller of line 21 or line 22. This amount is taxed at 0%
f6251_24 = f6251_22 - f6251_23  # Subtract line 23 from line 22
f6251_25 = D('501600')
f6251_26 = f6251_21  # Enter the amount from line 21
f6251_27 = QDCGTW_5  # Enter the amount from line 5 of the Qualified Dividends and Capital Gain Tax Worksheet
f6251_28 = f6251_26 + f6251_27  # Add line 26 and line 27
f6251_29 = max(0, f6251_25 - f6251_28)  # Subtract line 28 from line 25. If zero or less, enter -0-
f6251_30 = min(f6251_24, f6251_29)  # Enter the smaller of line 24 or line 29
f6251_31 = f6251_30 * D('0.15')  # Multiply line 30 by 15% (0.15)
f6251_32 = f6251_23 + f6251_30  # Add lines 23 and 30
assert f6251_32 != f6251_12
f6251_33 = f6251_22 - f6251_32  # Subtract line 32 from line 22
f6251_34 = f6251_33 * D('0.2')  # Multiply line 33 by 20% (0.20)
assert f6251_14 == 0
f6251_37 = 0
f6251_38 = f6251_18 + f6251_31 + f6251_34 + f6251_37  # Add lines 18, 31, 34, and 37
if f6251_12 <= 199900:
    f6251_39 = f6251_12 * D('0.26')  # If line 12 is $199,900 or less ($99,950 or less if married filing separately), multiply line 12 by 26% (0.26).
else:
    f6251_39 = f6251_12 * D('0.28') - 3998  # Otherwise, multiply line 12 by 28% (0.28) and subtract $3,998 ($1,999 if married filing separately) from the result
f6251_40 = min(f6251_38, f6251_39)  # Enter the smaller of line 38 or line 39 here and on line 7.
f6251_7 = f6251_40  # complete Part III on the back and enter the amount from line 40 here.
f6251_10 = f1040_16 + schedule_2_2 - schedule_3_1  # Add Form 1040 or 1040-SR, line 16 (minus any tax from Form 4972), and Schedule 2 (Form 1040), line 2. Subtract from the result Schedule 3 (Form 1040), line 1 and any negative amount reported on Form 8978, line 14 (treated as a positive number). If zero or less, enter -0-.
assert f6251_10 > f6251_7  # otherwise line 8 must be calculated
f6251_8 = 0  # Alternative minimum tax foreign tax credit
f6251_9 = f6251_7 - f6251_8  # Tentative minimum tax. Subtract line 8 from line 7
f6251_11 = max(0, f6251_9 - f6251_10)  # Subtract line 10 from line 9. If zero or less, enter -0-. Enter here and on Schedule 2 (Form 1040), line 1
if f6251_7 > f6251_10:
    print('attach form 6251')

# Form 1040 (SCHEDULE 2) Additional Taxes
schedule_2_1 = f6251_11  # Alternative minimum tax. Attach Form 6251
schedule_2_3 = schedule_2_1 + schedule_2_2  # Add lines 1 and 2. Enter here and on Form 1040, 1040-SR, or 1040-NR, line 17
schedule_2_11 = round(f8959_18, 2)  # Additional Medicare Tax. Attach Form 8959
schedule_2_12 = round(f8960_17, 2)  # Net investment income tax. Attach Form 8960
schedule_2_21 = schedule_2_11 + schedule_2_12  # Add lines 4, 7 through 16, 18, and 19. These are your total other taxes. Enter here and on Form 1040 or 1040-SR, line 23, or Form 1040-NR, line 23b
if dollar_rounding:
    schedule_2_21 = round(schedule_2_21)

# Form 1040 U.S. Individual Income Tax Return
f1040_17 = schedule_2_3  # Amount from Schedule 2, line 3
f1040_18 = f1040_16 + f1040_17  # Add lines 16 and 17

# SCHEDULE 8812 (Form 1040) Credits for Qualifying Children and Other Dependents
f8812_1 = f1040_11  # Enter the amount from line 11 of your Form 1040, 1040-SR, or 1040-NR
f8812_3 = f8812_1  # Add lines 1 and 2d
f8812_4a = children  # Number of qualifying children under age 18 with the required social security number
f8812_4b = children_under_6  # Number of children included on line 4a who were under age 6 at the end of 2021
f8812_4c = f8812_4a - f8812_4b  # Subtract line 4b from line 4a
if f8812_4a > 0:
    line_5_worksheet_1 = f8812_4b * D(3600)  # Multiply Schedule 8812, line 4b, by $3,600
    line_5_worksheet_2 = f8812_4c * D(3000)  # Multiply Schedule 8812, line 4c, by $3,000
    line_5_worksheet_3 = line_5_worksheet_1 + line_5_worksheet_2  # Add line 1 and line 2
    line_5_worksheet_4 = f8812_4a * D(2000)  # Multiply Schedule 8812, line 4a, by $2,000
    line_5_worksheet_5 = line_5_worksheet_3 - line_5_worksheet_4  # Subtract line 4 from line 3
    line_5_worksheet_6 = D(12500)  # Enter the amount shown below for your filing status
    line_5_worksheet_7 = min(line_5_worksheet_5, line_5_worksheet_6)  # Enter the smaller of line 5 or line 6
    line_5_worksheet_8 = D(150000)  # Enter the amount shown below for your filing status
    line_5_worksheet_9 = roundup(max(0, f8812_3 - line_5_worksheet_8))  # Subtract line 8 from Schedule 8812, line 3
    line_5_worksheet_10 = line_5_worksheet_9 * D('0.05')  # Multiply line 9 by 5% (0.05)
    line_5_worksheet_11 = min(line_5_worksheet_7, line_5_worksheet_10)  # Enter the smaller of line 7 or line 10
    line_5_worksheet_12 = line_5_worksheet_3 - line_5_worksheet_11  # Subtract line 11 from line 3. Enter on Schedule 8812, line 5

    f8812_5 = line_5_worksheet_12
else:
    f8812_5 = 0
f8812_7 = 0  # Multiply line 6 by $500
f8812_8 = f8812_7 + f8812_5  # Add lines 5 and 7
f8812_9 = D(400000)  # Enter the amount shown below for your filing status.
f8812_10 = roundup(max(0, f8812_3 - f8812_9))  # Subtract line 9 from line 3.
f8812_11 = f8812_10 * D('0.05')  # Multiply line 10 by 5% (0.05)
f8812_12 = max(0, f8812_8 - f8812_11)  # Subtract line 11 from line 8. If zero or less, enter -0-
f8812_13 = 'A'  # Check here if you (or your spouse if married filing jointly) had a principal place of abode in the United States for more than half of 2021
f8812_14a = min(f8812_7, f8812_12)  # Enter the smaller of line 7 or line 12
f8812_14b = f8812_12 - f8812_14a  # Subtract line 14a from line 12
if f8812_14a == 0:
    f8812_14c = 0  # If line 14a is zero, enter -0-;
else:
    assert False
    # f8812_14c = credit_limit_worksheet_a # enter the amount from the Credit Limit Worksheet A
f8812_14d = min(f8812_14a, f8812_14c)  # Enter the smaller of line 14a or line 14c
f8812_14e = f8812_14b + f8812_14d  # Add lines 14b and 14d
f8812_14f = letter_6419  # Enter the aggregate amount of advance child tax credit payments you (and your spouse if filing jointly) received for 2021.
f8812_14g = f8812_14e - f8812_14f  # Subtract line 14f from line 14e. If zero or less, enter -0- on lines 14g through 14i and go to Part III
assert f8812_14g > 0
f8812_14h = min(f8812_14d, f8812_14g)  # Enter the smaller of line 14d or line 14g. This is your credit for other dependents. Enter this amount on line 19 of your Form 1040, 1040-SR, or 1040-NR
f8812_14i = f8812_14g - f8812_14h  # Subtract line 14h from line 14g. This is your refundable child tax credit. Enter this amount on line 28 of your Form 1040, 1040-SR, or 1040-NR

# Form 1040
f1040_19 = f8812_14h  # Nonrefundable child tax credit or credit for other dependents from Schedule 8812
f1040_20 = schedule_3_8  # Amount from Schedule 3, line 8
f1040_21 = f1040_19 + f1040_20  # Add lines 19 and 20
f1040_22 = f1040_18 - f1040_21  # Subtract line 21 from line 18. If zero or less, enter -0-
f1040_23 = schedule_2_21  # Other taxes, including self-employment tax, from Schedule 2, line 21
f1040_24 = f1040_23 + f1040_22  # Add lines 22 and 23. This is your total tax
f1040_25a = W2_2  # Federal income tax withheld from Forms W-2 and 1099
if dollar_rounding:
    f1040_25a = round(f1040_25a)
f1040_25c = f8959_24  # Federal income tax withheld from: Other forms (see instructions)
f1040_25d = f1040_25a + f1040_25c  # Add lines 25a through 25c
f1040_27a = D(0)  # Earned income credit (EIC)
f1040_29 = D(0)  # American opportunity credit from Form 8863, line 8
f1040_31 = D(0)  # Amount from Schedule 3, line 15
f1040_28 = f8812_14i  # Refundable child tax credit or additional child tax credit from Schedule 8812
f1040_32 = f1040_27a + f1040_28 + f1040_29 + f1040_31  # Add lines 27a and 28 through 31. These are your total other payments and refundable credits
f1040_33 = f1040_32 + f1040_25d  # Add lines 25d, 26, and 32. These are your total payments
f1040_37 = f1040_24 - f1040_33  # Amount you owe. Subtract line 33 from line 24.
f1040_38 = D(0)  # Estimated tax penalty

if f1040_2b > 1500 or f1040_3b > 1500:
    assert False

# Form 2210 Underpayment of Estimated Tax by Individuals, Estates, and Trusts
f2210_1 = f1040_22  # Enter your 2021 tax after credits from Form 1040, 1040-SR, or 1040-NR, line 22.
f2210_2 = schedule_2_11 + schedule_2_12  # Other taxes, including self-employment tax and, if applicable, Additional Medicare Tax and/or Net Investment Income Tax
# TODO: i am not sure about the following but 21_1040.xlsx sets it as such:
f2210_3 = -f1040_28  # Other payments and refundable credits
f2210_4 = f2210_1 + f2210_2 + f2210_3  # Current year tax. Combine lines 1, 2, and 3. If less than $1,000, stop; you don’t owe a penalty
if f2210_4 >= 1000:
    f2210_5 = f2210_4 * D('0.90')  # Multiply line 4 by 90% (0.90)
    f2210_6 = f1040_25d  # Withholding taxes. Don’t include estimated tax payments. See instructions
    f2210_7 = f2210_4 - f2210_6  # Subtract line 6 from line 4. If less than $1,000, stop; you don’t owe a penalty.
    if f2210_7 >= 1000:
        if y2020_f1040_11 > 150000:
            f2210_8 = y2020_f1040_24 * D('1.1')  # Maximum required annual payment based on prior year’s tax (see instructions)
        else:
            f2210_8 = y2020_f1040_24
        f2210_9 = min(f2210_5, f2210_8)  # Required annual payment. Enter the smaller of line 5 or line 8
        if f2210_9 > f2210_6:  # Is line 9 more than line 6?
            f2210_None = 'Yes'  # Yes. You may owe a penalty, but don’t file Form 2210 unless one or more boxes in Part II below applies
        else:
            f2210_None = 'No'  # No. You don’t owe a penalty. Don’t file Form 2210 unless box E below applies.

print_vars(dict(locals()).items())

social_security_tax = min(142800, W2_5) * D('0.062')
total_tax = f1040_16 + schedule_2_12 - sum(f1099_DIV_7) + social_security_tax + f8959_7 + f8959_21 - f8812_14e
payed_already = W2_2 + social_security_tax + W2_6 - letter_6419

if not dollar_rounding:
    assert abs(((total_tax - payed_already) - f1040_37)) <= 0.01
    assert abs((f1040_24 - (total_tax - social_security_tax + f8812_14e - f8959_21))) <= 0.01
    assert abs((f1040_33 - (payed_already + f8812_14e - f8959_21 - social_security_tax))) <= 0.01

print(f'info: adjusted gross income            {f1040_11:10.2f}')
print(f'info: Taxable income                   {f1040_15:10.2f}')
print()
print(f'info: federal tax                      {f1040_16:10.2f}')
print(f'info: net investment tax               {schedule_2_12:10.2f}')
print(f'info: social security tax              {social_security_tax:10.2f}')
print(f'info: medicare tax                     {f8959_7 + f8959_21:10.2f}')
print(f'info: child tax credit                 {-f8812_14e:10.2f}')
print(f'info: total tax                        {total_tax:10.2f}')
print()
print(f'info: withheld federal tax             {W2_2:10.2f}')
print(f'info: withheld social security tax     {social_security_tax:10.2f}')
print(f'info: withheld medicare tax            {W2_6:10.2f}')
print(f'info: advance child tax credit payment {-letter_6419:10.2f}')
print(f'info: payed already                    {payed_already:10.2f}')
print()
print(f'info: amount you owe now               {f1040_37:10.2f}')
