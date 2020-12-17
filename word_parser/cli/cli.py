import click

from word_parser.parser import Parser


@click.command()
@click.option(
    "--input-file",
    "-i",
    help="The full path to the source file to parse",
    required=True,
)
@click.option(
    "--rules-file",
    "-r",
    help="The full path to the file with words to exclude",
    required=True,
)
@click.option(
    "--number-of-results",
    "-n",
    help="The number of words to return. Defaults to 20",
    default=20,
)
@click.option(
    "--use-collections-counter",
    "-c",
    is_flag=True,
    default=False,
    help="Use the Counter class from the collections module instead of custom method",
)
def parse_file(input_file, rules_file, number_of_results, use_collections_counter):
    parser = Parser(input_file=input_file, rules_file=rules_file)
    parser.parse_file()
    if not use_collections_counter:
        top_words = parser.get_top_words(number_of_results)
    else:
        print("INFO: Using collections counter")
        top_words = parser.final_words.most_common(number_of_results)
    print(f'| {"Word":<12} | Occurrences |')
    print(f'|{"-".join(["" for _ in range(15)])}|{"-".join(["" for _ in range(14)])}|')
    for row in top_words:
        print(f"| { row[0]:<12} | {row[1]:>11} |")
