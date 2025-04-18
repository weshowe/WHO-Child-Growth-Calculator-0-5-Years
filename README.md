# WHO-Child-Growth-Calculator-0-5-Years
Uses WHO data ([reference](https://www.cdc.gov/growthcharts/who-data-files.htm](https://www.who.int/tools/child-growth-standards/standards/head-circumference-for-age))) to calculate percentiles for length by age, weight by age, head circumference by age, and length by weight based on the child's age and gender. Works on babies/kids up to 5 years old.

## Installing:
Clone the repo to a folder of your choice and install dependencies by executing "pip install pandas" in the command line.

The program has a command line version (child.py) and a GUI version (child_gui.py). The GUI was vibecoded because I don't like making UIs.

## How to use:

### GUI

Execute the following command and fill out the desired fields in the window. Percentile results will be displayed in the "Results" tab.

    python child_gui.py

### Command Line

Execute child.py with the desired command line arguments to get percentiles for the measurements that you have. For example, to get a percentile for all measurements for a boy that's 3 months and 2 days old, you might type:
    
    python child.py --weight 5.5 --length 50 --head 30.3 --months 3 --days 2 --gender boy

Age of the child is specified using the --years, --months and --days arguments. You only need to specify at least one, ie: --months 4 if your baby is 4 months old.

Gender of the child is specified using the --gender argument (boy or girl)

The --weight argument followed by weight in kilograms is used to get the weight by age percentile.

The --length and --head arguments followed by the measurement in centimeters are used to get the length by age percentile and head circumference by age percentile, respectively.

If --length and --weight are passed, the length by weight percentile will be calculated.

If you would like to use Imperial measurements (pounds and/or inches), you can add the --pounds and/or --inches flags and the program will convert them. For example:

    python child.py --weight 12.11 --length 19.68 --head 11.92 --months 3 --days 2 --gender boy --pounds --inches

## Additional Notes
This program is intended for informational purposes only. I am not a doctor nor am I affiliated with the WHO, and the program's output should not be interpreted as medical advice.
