# CIS6930SP24-ASSIGNMENT1

## Author: Jyotiraditya

## Assignment Description:
This project aims to develop a system that automatically detects and censors sensitive entities such as names, dates, phone numbers, and addresses in documents. By leveraging data pipelines and natural language processing techniques, the system streamlines the redaction process, enhances efficiency, and ensures compliance with privacy regulations. Through a command-line interface, users can specify input files, select entities to be censored, and define output directories. Additionally, the system generates statistics on the redaction process, providing transparency and accountability.

## How to Install:
1. Clone the repository on your system:
    ```sh
    $ git clone https://github.com/jyotiradityasinghrathore/cis6930sp24-assignment1.git
    $ cd cis6930sp24-assignment1
    ```

2. Utilizing Pipenv, install prerequisites:
    ```sh
    $  pipenv install
    ```
3. Verify Installation:
    After the installation is complete, you can verify that
    pipenv, nltk, and spacy is installed correctly by running python:
    ```sh
    $ pipenv --version
    $ python
    $ import nltk
    $ import spacy
    ```   
## How to run
1. To run the program, use the following command:
    ```sh
    $ pipenv run python censoror.py --input '*.txt' \
                    --names --dates --phones --address\
                    --output 'files/' \
                    --stats stderr
    ```

## Code Structure
- cis6930sp24-assignment1/
    - COLLABORATORS
    - LICENSE
    - README.md
    - Pipfile
    - assignment1/
        - main.py
    - censoror.py
    - setup.cfg
    - setup.py
    - tests/
        - test_names.py
        - test_phones.py
        - test_address.py
        - test_dates

## Files

- `censoror.py`: The censoror.py script detects and censors sensitive information like names, dates, phone numbers, and addresses in plain text documents. It takes user-specified input files, processes them, and writes the censored content to new files. Additionally, it generates summary statistics of the censoring process. 

- `main.py`: The provided script main.py uses various natural language processing libraries such as NLTK, spaCy, and CommonRegex to censor names, dates, phone numbers, and addresses in text data. It tokenizes text, identifies named entities, and replaces them with a specified censor character. Additionally, it employs a snorkel labeling function to refine name censoring based on title occurrences before capitalized words.

## Function Descriptions

### `main(args)`
This is the main function that orchestrates the censorship process. It takes command-line arguments as input, including input file paths, censoring options, output format, and statistics printing format. It reads the input files, applies censorship based on the specified options, and writes the censored files to the output directory. Additionally, it generates statistics regarding the censorship process and prints or saves them based on the specified format.

### `write_to_files(raw_file, data)`
This function writes the censored text data to a file in the specified output directory. It creates the output directory if it doesn't exist and handles subfolders within the output directory.

### `Censored_File_Write(input_file, output_dir, censored_text)`
This function writes the censored text to a file in the specified output directory. It constructs the path for the output file, creates the output directory if it doesn't exist, and writes the censored text to the output file.

### `Stats_File_Write(raw_file, stats)`
This function writes the statistics of the censorship process to a file. It takes the file path and statistics as input, writes the statistics to the file, and prints a message indicating where the statistics are saved.

### `Stats_Censor(args, censor_counts, censor_list)`
This function generates statistics regarding the censorship process based on the specified censoring options. It formats the statistics as a string and returns them.

### `censor_names(data)`
This function censors names in the text data. It tokenizes the text, identifies named entities using NLTK's part-of-speech tagging and named entity recognition, and replaces the identified names with a censor character. It also excludes certain common titles from the list of censored names.

### `DatesCensor(data)`
This function censors dates in the text data. It uses spaCy to extract date entities and regular expressions to find date patterns in the text. It then replaces the identified dates with a censor character.

### `PhoneCensor(data)`
This function censors phone numbers in the text data. It uses CommonRegex to identify phone number patterns in the text and replaces them with a censor character.

### `AddressCensor(data)`
This function censors addresses in the text data. It uses pyap (Python Address Parser) to parse and identify address patterns in the text. It then replaces the identified addresses with a censor character.

### `refine_with_snorkel(sentences, extract_entities_fn, labeling_fn)`
This function refines the process of censoring names using a snorkel labeling function. It tokenizes the text into sentences, extracts named entities using a custom function (extract_entities), and applies a labeling function (lf_title_before_capitalized_word) to refine the list of identified names. Finally, it returns the refined list of names.


## Bugs/Assumptions
-  The code assumes that the output directory supplied by the --output parameter exists, or that it can be created if not. However, it does not check for permissions or handle directory construction errors.
-  The success of filtering names, dates, phone numbers, and addresses is dependent on the correctness of the underlying NLP and regex-based algorithms. Certain entities may not be accurately detected, and non-sensitive material may be suppressed incorrectly.
- The code does not address potential issues related to processing large input files or large volumes of input data. It may encounter performance issues or memory errors when dealing with excessively large files or datasets.


## Test Function Descriptions

#### test_address.py
The provided code tests the `AddressCensor` function from `assignment1.main` using `pytest`. Test cases, stored in `testdata`, contain input texts, expected outputs, and censorship counts.

The `@pytest.mark.parametrize` decorator parametrizes the `test_word` function with test data for iterative execution. Within the function, `AddressCensor` is invoked, and its output is compared to expected results using assertions.

This test suite ensures the accurate censorship of addresses and returns expected outputs and counts.

#### test_dates.py
This script tests the `DatesCensor` function from `main` using `pytest`. Test data in `testdata` includes input strings, expected outputs, and date counts.

Parametrizing `test_word` with `@pytest.mark.parametrize`, it enables repeated execution with diverse inputs. Within the function, `DatesCensor` is invoked, and assertions compare its output to expected results.

The unit test validates the `DatesCensor` function's behavior across varying inputs.

#### test_names.py
This code tests `Snorkel_Censor_Name` from `assignment1.main` using `pytest`. A single test case in `testdata` contains input, expected output, and censored name counts.

Parametrizing `test_word`, the function iterates over test data. Within it, `Snorkel_Censor_Name` is invoked, and assertions validate its output against expectations.

The unit test ensures the `Snorkel_Censor_Name` function's reliability under diverse scenarios.

#### test_phones.py
This script tests `PhoneCensor` from `main.py` using `pytest`. Test data in `testdata` comprises input strings, expected outputs, and phone number counts.

`test_word` is parametrized with `@pytest.mark.parametrize` for multiple executions. Inside, `PhoneCensor` is called, and assertions verify its output and count.

The unit test confirms the accuracy of `PhoneCensor` across various inputs.
