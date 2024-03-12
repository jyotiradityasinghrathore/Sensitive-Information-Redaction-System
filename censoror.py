import sys
import os
import argparse
import glob

from assignment1.main import *

from warnings import filterwarnings
filterwarnings("ignore")

# The main function orchestrates the censoring process by reading raw data files,
# applying censoring functions based on user arguments, outputting censored data, and generating statistics.
def main(args):
    # Gather a list of raw data files using glob
    Raw_Data_Files = []
    for Global_Input in args.input:
        Raw_Data_Files += glob.glob(Global_Input)

    final_stats = ""
    # Process each raw data file
    for raw_file in Raw_Data_Files:
        print(" In Process", raw_file, "==>")
        data = ""
        try:
            # Attempt to read the raw data file
            with open(raw_file, 'r') as f:
                data = f.read()
        except:
            # Handle the case where the file cannot be read
            print(f"{raw_file} file not able to read file\n")
            continue
        
        # Initialize dictionaries to store censor counts and lists
        censor_counts = {}
        censor_list = {}

        # Apply date censoring if specified
        if args.dates:
            data, List_Dates = DatesCensor(data)
            censor_counts["dates_count"] = len(List_Dates)
            censor_list["List_Dates"] = List_Dates   

        # Apply phone censoring if specified
        if args.phones:
            data, list_phones = PhoneCensor(data)
            censor_counts["phones_count"] = len(list_phones)
            censor_list["list_phones"] = list_phones

        # Apply address censoring if specified
        if args.address:
            data, List_Address = AddressCensor(data)
            censor_counts["address_count"] = len(List_Address)
            censor_list["List_Address"] = List_Address

        # Apply name censoring if specified
        if args.names:
            data, names_list = Snorkel_Censor_Name(data)
            censor_counts["names_count"] = len(names_list)
            censor_list["names_list"] = names_list

        # Output the censored data to stdout, stderr, or file
        if args.output == 'stdout' or args.output == 'stderr':
            if args.output == 'stdout':
                sys.stdout.write(data)
                sys.stdout.write('\n')
            
            if args.output == 'stderr':
                sys.stderr.write(data)
                sys.stderr.write('\n')
        else:
            Censored_File_Write(raw_file, args.output, data)

        # Generate statistics on censoring and append to final_stats
        stats = Stats_Censor(args, censor_counts, censor_list)
        final_stats += f"- Censored data from {raw_file} file, statistics below from the file -\n" + stats + "\n\n"

        # Output statistics to stdout, stderr, or file
        if args.stats == 'stdout':
            sys.stdout.write("\n- Censored Data from file, statistics below from the file -\n")
            sys.stdout.write(final_stats)
            sys.stdout.write('\n')
        
        if args.stats == 'stderr':
            sys.stdout.write("\n- Censored Data from file, statistics below from the file -\n")
            sys.stderr.write(final_stats)
            sys.stderr.write('\n')
        else:
            Stats_File_Write(args.stats, final_stats)

        # Reset final_stats for the next iteration
        final_stats = ""        


# Writes the censored text to a file in the specified output directory,
# creating the directory if it doesn't exist.
def Censored_File_Write(input_file, output_dir, censored_text):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, os.path.basename(input_file) + ".censored")
    with open(output_file, 'w') as f:
        f.write(censored_text)   


# Writes the statistics of censoring to a file, including the counts and lists of censored items.
def Stats_File_Write(raw_file, stats):
    raw_file_path = os.path.join(os.getcwd(), raw_file)

    with open(raw_file_path, 'w') as f:
        f.write(stats)

    print(f"Stats to {raw_file_path}")
    print("\n")

# Generates statistics based on the censoring counts and lists, 
# and returns them as a formatted string for display or writing to a file.
def Stats_Censor(args, censor_counts, censor_list):
    List_Stats = []
    
    if vars(args)['names']:
        List_Stats.append(f"Total {censor_counts['names_count']} names got censored.")
        List_Stats.append(f"\tCensored names are {censor_list['names_list']} ")

    if vars(args)['dates']:
        List_Stats.append(f"Total {censor_counts['dates_count']} dates got censored.")
        List_Stats.append(f"\tCensored dates are {censor_list['List_Dates']} ")

    if vars(args)['phones']:
        List_Stats.append(f"Total {censor_counts['phones_count']} phone numbers got censored.")
        List_Stats.append(f"\tCensored phone numbers are {censor_list['list_phones']} ")

    if vars(args)['address']:
        List_Stats.append(f"Total {censor_counts['address_count']} address/es got censored.")
        List_Stats.append(f"\tCensored addressess are {censor_list['List_Address']} ")

    return "\n".join(List_Stats)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required = True, type = str, action = "append", help='input file is from argument')
    parser.add_argument('--names', action = "store_true", help='names censored using snorkel')
    parser.add_argument('--dates', action = "store_true", help='dates censored from the input files')
    parser.add_argument('--phones', action = "store_true", help='phone numbers censored from the input files')
    parser.add_argument('--address', action = "store_true", help='All Address censored from the input files')
    parser.add_argument('--output',required = True, help='the printing format specified')
    parser.add_argument('--stats', required = True, help='the printing format specified')

    args = parser.parse_args()
    
    main(args)