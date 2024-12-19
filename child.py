import pandas as pd
import math
from scipy.stats import norm
import argparse
from pathlib import Path
import os
import sys

# Calculation taken from CDC website instructions for L S and M values (apply to WHO as well)
def calc_percentile(age, val, chart):
    
    chart_row = chart.loc[age]
    z_score = 0

    if chart_row["L"] == 0:
        z_score = math.log(val/chart_row["M"]) / chart_row["S"]

    else:
        z_score = (((val/chart_row["M"]) ** chart_row["L"]) - 1) / (chart_row["L"] * chart_row["S"])

    return norm.cdf(z_score) *100

# Get percentile.
def calc_value(age, val, chart, unit, isImperial = False):

    # Determine what unit of measurement we're using.
    conv_measurement = val
    unMeasurement = None

    if unit == "weight":

        if isImperial:
            unMeasurement = "pounds"
            conv_measurement *= 0.45359237
        else:
            unMeasurement = "kilograms"
    elif (unit == "length") or unit == "head circumference":
        if isImperial:
            unMeasurement = "inches"
            conv_measurement *= 2.54
        else:
            unMeasurement = "centimeters"
    else:
        print(f"Error: No logic present for unit type {unit}")
        return
    
    # Get percentile
    resultant = calc_percentile(age, conv_measurement, chart)

    print(f"For {unit} of {val} {unMeasurement}, the percentile: {resultant}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pounds", help="Use weight measurement of pounds", action="store_true")
    parser.add_argument("-i", "--inches", help="Use length measurement of inches", action="store_true")
    parser.add_argument("-c", "--head", type=float, help="the length of the baby's head circumference")
    parser.add_argument("-l", "--length", type=float, help="the length of the baby")
    parser.add_argument("-w", "--weight", type=float, help="the weight of the baby")
    parser.add_argument("-m", "--months", type=int, help="How many months old the baby is.")
    parser.add_argument("-y", "--years", type=int, help="How many months old the baby is.")
    parser.add_argument("-d", "--days", type=int, help="How many days old the baby is in addition to the month (ie: if the baby is 5 months 2 days old, this is 2 and the month is 5)")
    parser.add_argument("-g", "--gender", type=str, help="The baby's gender. Accepts 'boy' or 'girl'", required=True, action = "store")
    args = parser.parse_args()

    # Used to find script location with data files (makes invariant to script path as long as data files are in same folder)
    scriptPath = str(Path(os.path.dirname(sys.argv[0])).resolve())

    # sanity checks.
    isImperialWeight = args.pounds
    isImperialLength = args.inches

    if (args.gender is None) or ((args.gender != "boy") and (args.gender != "girl")):
        print(f"Error: gender argument must be 'boy' or 'girl', passed argument: {args.gender}")
        return
    
    if (args.days is None) and (args.months is None) and (args.years is None):
        print("Error: No age specified. You need to specify values for at least one of the following: --years, --months, --days")
        return
    
    if args.days is not None:

        if (args.days < 0):
            print(f"Error: days must be positive, passed value: {args.days}")
            return

        # Overflow handling
        if args.days > 30:

            if args.months is None:
                args.months = 0
            
            args.months += int(args.days / 30)
            args.days = args.days % 30

    else:
        args.days = 0
    
    if args.months is not None:

        if (args.months < 0):
            print(f"Error: months must be positive, passed value: {args.months}")
            return

        # Overflow handling
        if args.months > 12:

            if args.years is None:
                args.years = 0
            
            args.years += int(args.months / 12)
            args.months = args.months % 12

    else:
        args.months = 0

    if args.years is not None:

        if (args.years < 0):
            print(f"Error: years must be positive, passed value: {args.years}")
            return

    else:
        args.years = 0
    
    if args.head is not None:
        if args.head <= 0:
            print("Error: Head circumference must be greater than 0")
            return
    
    if args.length is not None:
        if args.length <= 0:
            print("Error: Length must be greater than 0")
            return
        
    if args.weight is not None:
        if args.weight <= 0:
            print("Error: Weight must be greater than 0")
            return
    
    print()

    # calculate age in days for the chart. Based on instructions here: https://cdn.who.int/media/docs/default-source/child-growth/child-growth-standards/indicators/instructions-en.pdf?sfvrsn=5cec8c61_23
    days = args.days + (args.months * 30.4375) + (args.years * 12 * 30.4375)
    days = int(days)
    print(f"Input age: {args.years} Years, {args.months} Months, {args.days} Days = {days} Days (adjusted calculation based on WHO instructions)")

    # chart is capped at 1856 days. If we we have overflow, print warning and cap at 1856.
    if days > 1856:
        print(f"Warning: WHO chart is limited to 1856 days (approximately 5 years), calculated age is {days} days. Performing calculation for an age of 1856 days.")
        days = 1856
    
    print()

    # weight calculation
    if args.weight is not None:
        weight_chart = None

        if args.gender == "girl":
            weight_chart = pd.read_excel(f"{scriptPath}/wfa-girls-zscore-expanded-tables.xlsx")
        else:
            weight_chart = pd.read_excel(f"{scriptPath}/wfa-boys-zscore-expanded-tables.xlsx")
           
        weight_chart = weight_chart.set_index(['Day'])

        calc_value(days, args.weight, weight_chart, "weight", isImperialWeight)  
        print()
    
    # length calculation
    if args.length is not None:
        length_chart = None

        if args.gender == "girl":
            length_chart = pd.read_excel(f"{scriptPath}/lhfa-girls-zscore-expanded-tables.xlsx")
        else:
            length_chart = pd.read_excel(f"{scriptPath}/lhfa-boys-zscore-expanded-tables.xlsx")
           
        length_chart = length_chart.set_index(['Day'])

        calc_value(days, args.length, length_chart, "length", isImperialLength)
        print()

    # head calculation
    if args.head is not None:
        head_chart = None

        if args.gender == "girl":
            head_chart = pd.read_excel(f"{scriptPath}/hcfa-girls-zscore-expanded-tables.xlsx")
        else:
            head_chart = pd.read_excel(f"{scriptPath}/hcfa-boys-zscore-expanded-tables.xlsx")
           
        head_chart = head_chart.set_index(['Day'])

        calc_value(days, args.head, head_chart, "head circumference", isImperialLength)
        print()


if __name__ == "__main__":
    main()


