# US Federal Tax calculator

This is a Python script for calculating the US Federal Tax for tax year 2021. It prints the value of every field for all the supported tax forms.

It supports the following tax forms:
* Form 1040 (U.S. Individual Income Tax Return)
* Form 2210 (Underpayment of Estimated Tax by Individuals, Estates, and Trusts)
* Form 6251 (Alternative Minimum Tax—Individuals)
* Form 8949 (Sales and Other Dispositions of Capital Assets)
* Form 8959 (Additional Medicare Tax)
* Form 8960 (Net Investment Income Tax — Individuals, Estates, and Trusts)
* Form 8995 (Qualified Business Income Deduction Simplified Computation)
* Form 8995-A (Qualified Business Income Deduction)
* Schedule 2 (Form 1040) (Additional Taxes)
* Schedule 3 (Form 1040) (Additional Credits and Payments)
* Schedule 8812 (Form 1040) (Credits for Qualifying Children and Other Dependents)
* Schedule D (Form 1040) (Capital Gains and Losses)

Disclaimer:
* Not all code paths have been tested. I have tried to mark them with `assert False`.
* Please be aware that many constants assume that you are filing as "married filing jointly".
* Double check the results. I am not a tax expert. Please review the Limitation of Liability of the license.

## Instructions

Modify the script to input your information and execute it. The output looks like this:
```
f1040_1               120000.00
f1040_2b                   0.00
f1040_3a                   1.00
f1040_3b                   1.00
f1040_7                    2.00
f1040_9               120003.00
f1040_11              120003.00
f1040_12a              25100.00
f1040_12c              25100.00
f1040_13                   0.00
f1040_14               25100.00
f1040_15               94903.00
f1040_16               12375.52
f1040_17                   0
f1040_18               12375.52
f1040_19                   0
f1040_20                   0
f1040_21                   0
f1040_22               12375.52
f1040_23                   0.00
f1040_24               12375.52
f1040_25a                  0.00
f1040_25c                  0.00
f1040_25d                  0.00
f1040_27a                  0.00
f1040_28                3000.00
f1040_29                   0.00
f1040_31                   0.00
f1040_32                3000.00
f1040_33                3000.00
f1040_37                9375.52
f1040_38                   0.00
...
info: adjusted gross income             120003.00
info: Taxable income                     94903.00

info: federal tax                        12375.52
info: net investment tax                     0.00
info: social security tax                    0.00
info: medicare tax                           0.00
info: child tax credit                   -3000.00
info: total tax                           9375.52

info: withheld federal tax                   0.00
info: withheld social security tax           0.00
info: withheld medicare tax                  0.00
info: advance child tax credit payment       0.00
info: payed already                          0.00

info: amount you owe now                  9375.52
```
