# WHO-Baby-Growth-Calculator-0-24-Months-
Uses WHO data ([reference](https://www.cdc.gov/growthcharts/who-data-files.htm)) to calculate percentiles for length, weight, and head circumference based on baby's age.

## Installing:
Clone the repo to a folder of your choice and install dependencies by executing "pip install pandas scipy" in the command line.

## How to use:
Execute baby.py with the desired command line arguments to get percentiles for the measurements that you have. For example, to get a percentile for all 3 measurements, you might type:
    
    baby.py --weight 5.5 --length 50 --head 30.3 --months 3 --days 2 --gender boy

Age of the baby is specified using the --months and --days arguments.

Gender of the baby is specified using the --gender argument (boy or girl)

The --weight argument followed by weight in kilograms is used to get the weight percentile.

The --length and --head arguments followed by the measurement in centimeters are used to get the length percentile and head circumference percentile, respectively.

If you would like to use Imperial measurements (pounds and/or inches), you can add the --pounds and/or --inches flags and the program will convert them. For example:

    baby.py --weight 12.11 --length 19.68 --head 11.92 --months 3 --days 2 --gender boy --pounds --inches

## Additional Notes

Since the WHO growth data is only by month, this program uses linear interpolation for ages that are not exact months. For example, if your baby is 2 months and 15 days old (2.5 months) and has a weight percentile that would be 65 at month 2 and 55 at month 3, the program will calculate the percentile for 2.5 months as 60.

This program is intended for informational purposes only. I am not a doctor nor am I affiliated with the WHO, and the program's output should not be interpreted as medical advice.
