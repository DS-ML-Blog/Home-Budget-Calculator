import os
import sys

from classes import MyWorkbook
from functions.part_funcs.create_all_plots import create_all_plots
from functions.part_funcs.create_pptx_presentation \
    import create_pptx_presentation
from functions.part_funcs.create_xlsx_report import create_xlsx_report


start_month = int(sys.argv[1])
start_year = int(sys.argv[2])
end_month = int(sys.argv[3])
end_year = int(sys.argv[4])

# Preparing the analysis
if (start_year > end_year) or \
   (start_year == end_year and start_month > end_month):
    print("Podany zakres dat jest błędny")
    sys.exit()
else:
    # generating list of sheetnames for a given range
    list_of_sheetnames = []
    n_of_months = 12*(end_year-start_year) + end_month-start_month + 1
    month = start_month
    year = start_year
    for i in range(n_of_months):
        name_of_sheet = ("0"+str(month) if month <= 9 else str(month)) \
                        + "." + str(year)
        list_of_sheetnames.append(name_of_sheet)

        month += 1
        if month > 12:
            month -= 12
            year += 1

folder_path_file = open("path.txt", "r")
folder_path = folder_path_file.read()
folder_path_file.close()

file_path = folder_path + "/total/total.xlsx"
part_label = str(start_month) + ".20" + str(start_year) + "-" \
             + str(end_month) + ".20" + str(end_year)

myWorkbook = MyWorkbook(file_path, list_of_sheetnames)

start_label = [int(list_of_sheetnames[0][:2]), int(list_of_sheetnames[0][-2:])]

results_dir = folder_path + "/!Raporty/total_partial/" + part_label \
              + " - wyniki/"
if not os.path.exists(results_dir):
    os.mkdir(results_dir)
    os.mkdir(results_dir + "/plots")


# Actual analysis
spendings_list, incomes_list \
    = create_all_plots(myWorkbook, part_label, results_dir, start_label,
                       n_of_months)

create_pptx_presentation(part_label, results_dir)

create_xlsx_report(results_dir, part_label, myWorkbook, start_label,
                   n_of_months)
