import argparse
import glob
import sys
import os

from assignment1.main import *

from warnings import filterwarnings
filterwarnings("ignore")


def main(args):
    # Getting list of input files
    raw_files = []
    for inp_glob in args.input:
        raw_files += glob.glob(inp_glob)

    # censoring each file
    final_stats = ""
    for raw_file in raw_files:
        print("Processing", raw_file, "==>")
        data = ""
        try:
            with open(raw_file, 'r') as f:
                data = f.read()
        except:
            print(f"{raw_file} file that is given can't be read, and so it can't be censored\n")
            continue
        
        #To count censored ones
        censor_counts = {}
        #To collect censored quantities
        censor_list = {}
        

        if args.address:
            data,address_list = censor_address(data)
            censor_counts["address_count"] = len(address_list)
            censor_list["address_list"] = address_list

        if args.names:
            data, names_list = censor_names_snorkel(data)
            censor_counts["names_count"] = len(names_list)
            censor_list["names_list"] = names_list

        # if args.names_without_snorkel:
        #     data, names_list = censor_names(data)
        #     censor_counts["names_count"] = len(names_list)
        #     censor_list["names_list"] = names_list

        if args.dates:
            data,dates_list = censor_dates(data)
            censor_counts["dates_count"] = len(dates_list)
            censor_list["dates_list"] = dates_list

        if args.phones:
            data,phones_list = censor_phones(data)
            censor_counts["phones_count"] = len(phones_list)
            censor_list["phones_list"] = phones_list
        
        if args.output == 'stdout' or args.output == 'stderr':
            if args.output == 'stdout':
                sys.stdout.write(data)
                sys.stdout.write('\n')
            
            if args.output == 'stderr':
                sys.stderr.write(data)
                sys.stderr.write('\n')
        else:
            write_censored_file(raw_file, args.output, data)
        

        stats=censor_stats(args, censor_counts, censor_list)
        final_stats += f"------Data is censored from {raw_file} file, below is the statistics of the censorions made in file------\n" + stats + "\n\n"

        if args.stats == 'stdout':
            sys.stdout.write("\n-----------Data is censored from file, below is the statistics of the censorions made in file---------------\n")
            sys.stdout.write(final_stats)
            sys.stdout.write('\n')
        
        if args.stats == 'stderr':
            sys.stdout.write("\n-----------Data is censored from file, below is the statistics of the censorions made in file---------------\n")
            sys.stderr.write(final_stats)
            sys.stderr.write('\n')
        else:
            write_to_files_stats(args.stats, final_stats)

        final_stats = ""        

def write_censored_file(input_file, output_dir, censored_text):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, os.path.basename(input_file) + ".censored")
    with open(output_file, 'w') as f:
        f.write(censored_text)   


def write_to_files_stats(raw_file, stats):
    raw_file_path = os.path.join(os.getcwd(), raw_file)

    with open(raw_file_path, 'w') as f:
        f.write(stats)

    print(f"Stats to {raw_file_path}")
    print("\n")

def censor_stats(args, censor_counts, censor_list):
    stats_list = []
    

    # if vars(args)['names_without_snorkel']:
    #     stats_list.append(f"In total {censor_counts['names_count']} names got censored.")
    #     stats_list.append(f"\tThe names that got censored are {censor_list['names_list']} ")
    
    if vars(args)['names']:
        stats_list.append(f"In total {censor_counts['names_count']} names got censored.")
        stats_list.append(f"\tThe names that got censored are {censor_list['names_list']} ")

    if vars(args)['dates']:
        stats_list.append(f"In total {censor_counts['dates_count']} dates got censored.")
        stats_list.append(f"\tThe dates that got censored are {censor_list['dates_list']} ")

    if vars(args)['phones']:
        stats_list.append(f"In total {censor_counts['phones_count']} phone numbers got censored.")
        stats_list.append(f"\tThe phones that got censored are {censor_list['phones_list']} ")

    if vars(args)['address']:
        stats_list.append(f"In total {censor_counts['address_count']} address/es got censored.")
        stats_list.append(f"\tThe address/es that got censored are {censor_list['address_list']} ")

    
    return "\n".join(stats_list)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required = True, type = str, action = "append", help='input file is taken through this argument')
    # parser.add_argument('--names_without_snorkel', action = "store_true", help='names from the input file gets censored')
    parser.add_argument('--names', action = "store_true", help='names from the input file gets censored using snorkel')
    parser.add_argument('--dates', action = "store_true", help='dates from the input files get censored')
    parser.add_argument('--phones', action = "store_true", help='phone numbers from the input files get censored')
    parser.add_argument('--address', action = "store_true", help='addresses in the input files get censored')
    parser.add_argument('--output',required = True, help='the printing format of input file output  is specified')
    parser.add_argument('--stats', required = True, help='the printing format of input file summary is specified')

    args = parser.parse_args()
    
    
    main(args)