import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from os import path
import pandas as pd
from math import log, erf, sqrt

# Import functions from child.py
from child import calc_percentile, calc_value, calc_value_wh

class ChildGrowthGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Child Growth Percentile Calculator (0-5 years)")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create the main input frame
        self.input_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.input_frame, text="Input Data")
        
        # Create the results frame
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        
        # Set up the input frame
        self.setup_input_frame()
        
        # Set up the results frame
        self.setup_results_frame()
        
        # Calculate path for chart files
        try:
            self.script_path = str(Path(path.dirname(__file__)).resolve())
        except NameError:
            self.script_path = str(Path(path.dirname(sys.argv[0])).resolve())
    
    def setup_input_frame(self):
        # Gender selection
        ttk.Label(self.input_frame, text="Gender:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.gender_var = tk.StringVar(value="boy")
        gender_frame = ttk.Frame(self.input_frame)
        gender_frame.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        ttk.Radiobutton(gender_frame, text="Boy", variable=self.gender_var, value="boy").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Girl", variable=self.gender_var, value="girl").pack(side=tk.LEFT, padx=5)
        
        # Age inputs
        age_frame = ttk.LabelFrame(self.input_frame, text="Age")
        age_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ttk.Label(age_frame, text="Years:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.years_var = tk.IntVar(value=0)
        ttk.Spinbox(age_frame, from_=0, to=5, textvariable=self.years_var, width=5).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        ttk.Label(age_frame, text="Months:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.months_var = tk.IntVar(value=0)
        ttk.Spinbox(age_frame, from_=0, to=11, textvariable=self.months_var, width=5).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        ttk.Label(age_frame, text="Days:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.days_var = tk.IntVar(value=0)
        ttk.Spinbox(age_frame, from_=0, to=30, textvariable=self.days_var, width=5).grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Measurement inputs
        measurements_frame = ttk.LabelFrame(self.input_frame, text="Measurements")
        measurements_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # Weight input
        ttk.Label(measurements_frame, text="Weight:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.weight_var = tk.DoubleVar(value=0)
        ttk.Entry(measurements_frame, textvariable=self.weight_var, width=10).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.weight_unit_var = tk.StringVar(value="kg")
        weight_unit_frame = ttk.Frame(measurements_frame)
        weight_unit_frame.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(weight_unit_frame, text="kg", variable=self.weight_unit_var, value="kg").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(weight_unit_frame, text="lb", variable=self.weight_unit_var, value="lb").pack(side=tk.LEFT, padx=5)
        
        # Length input
        ttk.Label(measurements_frame, text="Length/Height:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.length_var = tk.DoubleVar(value=0)
        ttk.Entry(measurements_frame, textvariable=self.length_var, width=10).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.length_unit_var = tk.StringVar(value="cm")
        length_unit_frame = ttk.Frame(measurements_frame)
        length_unit_frame.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(length_unit_frame, text="cm", variable=self.length_unit_var, value="cm").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(length_unit_frame, text="in", variable=self.length_unit_var, value="in").pack(side=tk.LEFT, padx=5)
        
        # Head circumference input
        ttk.Label(measurements_frame, text="Head Circumference:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.head_var = tk.DoubleVar(value=0)
        ttk.Entry(measurements_frame, textvariable=self.head_var, width=10).grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.head_unit_var = tk.StringVar(value="cm")
        head_unit_frame = ttk.Frame(measurements_frame)
        head_unit_frame.grid(row=2, column=2, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(head_unit_frame, text="cm", variable=self.head_unit_var, value="cm").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(head_unit_frame, text="in", variable=self.head_unit_var, value="in").pack(side=tk.LEFT, padx=5)
        
        # Calculate button
        calculate_button = ttk.Button(self.input_frame, text="Calculate Percentiles", command=self.calculate_percentiles)
        calculate_button.grid(row=3, column=0, columnspan=2, pady=20)
    
    def setup_results_frame(self):
        # Text widget to display results
        self.results_text = tk.Text(self.results_frame, wrap=tk.WORD, width=80, height=20)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.results_frame, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Make the text read-only
        self.results_text.config(state=tk.DISABLED)
    
    def calculate_percentiles(self):
        try:
            # Get input values
            gender = self.gender_var.get()
            years = self.years_var.get()
            months = self.months_var.get()
            days = self.days_var.get()
            
            # Handle overflows like in the original program
            if days > 30:
                months += int(days / 30)
                days = days % 30
            
            if months > 12:
                years += int(months / 12)
                months = months % 12
            
            # Calculate total days
            total_days = days + (months * 30.4375) + (years * 12 * 30.4375)
            total_days = int(total_days)
            
            # Cap at 1856 days as per WHO guidelines
            if total_days > 1856:
                messagebox.showwarning("Age Warning", "WHO chart is limited to 1856 days (approximately 5 years). Calculation will be performed for an age of 1856 days.")
                total_days = 1856
            
            # Get measurement values
            weight = self.weight_var.get() if self.weight_var.get() > 0 else None
            length = self.length_var.get() if self.length_var.get() > 0 else None
            head = self.head_var.get() if self.head_var.get() > 0 else None
            
            # Check units
            is_imperial_weight = self.weight_unit_var.get() == "lb"
            is_imperial_length = self.length_unit_var.get() == "in" or self.head_unit_var.get() == "in"
            
            # Clear previous results
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            
            results = []
            
            # Add age information
            results.append(f"Input age: {years} Years, {months} Months, {days} Days = {total_days} Days (adjusted calculation based on WHO instructions)")
            results.append("")
            
            # Calculate weight percentile
            if weight is not None and weight > 0:
                weight_chart = None
                
                if gender == "girl":
                    weight_chart = pd.read_excel(f"{self.script_path}/charts/wfa-girls-zscore-expanded-tables.xlsx")
                else:
                    weight_chart = pd.read_excel(f"{self.script_path}/charts/wfa-boys-zscore-expanded-tables.xlsx")
                
                weight_chart = weight_chart.set_index(['Day'])
                
                # Calculate and store result as string
                weight_percentile = calc_percentile(total_days, weight * (0.45359237 if is_imperial_weight else 1), weight_chart)
                unit_text = "pounds" if is_imperial_weight else "kilograms"
                results.append(f"For weight of {weight} {unit_text}, the percentile for age by weight is: {weight_percentile:.2f}")
                results.append("")
            
            # Calculate length percentile
            if length is not None and length > 0:
                length_chart = None
                
                if gender == "girl":
                    length_chart = pd.read_excel(f"{self.script_path}/charts/lhfa-girls-zscore-expanded-tables.xlsx")
                else:
                    length_chart = pd.read_excel(f"{self.script_path}/charts/lhfa-boys-zscore-expanded-tables.xlsx")
                
                length_chart = length_chart.set_index(['Day'])
                
                # Calculate and store result
                length_percentile = calc_percentile(total_days, length * (2.54 if is_imperial_length else 1), length_chart)
                unit_text = "inches" if is_imperial_length else "centimeters"
                results.append(f"For length of {length} {unit_text}, the percentile for age by length is: {length_percentile:.2f}")
                results.append("")
            
            # Calculate head circumference percentile
            if head is not None and head > 0:
                head_chart = None
                
                if gender == "girl":
                    head_chart = pd.read_excel(f"{self.script_path}/charts/hcfa-girls-zscore-expanded-tables.xlsx")
                else:
                    head_chart = pd.read_excel(f"{self.script_path}/charts/hcfa-boys-zscore-expanded-tables.xlsx")
                
                head_chart = head_chart.set_index(['Day'])
                
                # Calculate and store result
                head_percentile = calc_percentile(total_days, head * (2.54 if is_imperial_length else 1), head_chart)
                unit_text = "inches" if is_imperial_length else "centimeters"
                results.append(f"For head circumference of {head} {unit_text}, the percentile for age by head circumference is: {head_percentile:.2f}")
                results.append("")
            
            # Calculate weight for length percentile if both are provided
            if weight is not None and length is not None and weight > 0 and length > 0:
                wl_chart = None
                
                conv_weight = weight * (0.45359237 if is_imperial_weight else 1)
                conv_length = length * (2.54 if is_imperial_length else 1)
                
                if gender == "girl":
                    if total_days > 730:
                        wl_chart = pd.read_excel(f"{self.script_path}/charts/tab_wfh_girls_p_2_5.xlsx")
                        wl_chart = wl_chart.set_index(['Height'])
                    else:
                        wl_chart = pd.read_excel(f"{self.script_path}/charts/tab_wfl_girls_p_0_2.xlsx")
                        wl_chart = wl_chart.set_index(['Length'])
                else:
                    if total_days > 730:
                        wl_chart = pd.read_excel(f"{self.script_path}/charts/tab_wfh_boys_p_2_5.xlsx")
                        wl_chart = wl_chart.set_index(['Height'])
                    else:
                        wl_chart = pd.read_excel(f"{self.script_path}/charts/tab_wfl_boys_p_0_2.xlsx")
                        wl_chart = wl_chart.set_index(['Length'])
                
                # Round height to nearest 0.5 for indexing purposes
                height_index = round(2 * conv_length) / 2
                
                # Calculate and store result
                try:
                    wfl_percentile = calc_percentile(height_index, conv_weight, wl_chart)
                    weight_unit = "pounds" if is_imperial_weight else "kilograms"
                    length_unit = "inches" if is_imperial_length else "centimeters"
                    results.append(f"For a weight of {weight} {weight_unit} and a height of {length} {length_unit}, the percentile for height by weight is: {wfl_percentile:.2f}")
                except KeyError:
                    results.append(f"Unable to calculate weight-for-length percentile: height value {height_index} cm not found in chart.")
            
            # Display all results
            self.results_text.insert(tk.END, "\n".join(results))
            self.results_text.config(state=tk.DISABLED)
            
            # Switch to results tab
            self.notebook.select(1)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during calculation: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChildGrowthGUI(root)
    root.mainloop() 