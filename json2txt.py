import argparse
import json
from os import path, walk


def get_txt(json_dir, recursive):
    start_of_text_token = '<|startoftext|>'
    end_of_text_token = '<|endoftext|>'
    text_separator = end_of_text_token + start_of_text_token

    article_text_list = []

    for dirpath, _, filenames in walk(json_dir):
        for filename in filenames:
            with open(path.join(dirpath, filename), encoding='utf8') as input_file:
                for article_json in input_file.readlines():
                    article = json.loads(article_json)
                    article_text_list.append(article['text'])

        if not(recursive):
            break

    return start_of_text_token + text_separator.join(article_text_list) + end_of_text_token


if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description='Converts WikiExtractor output JSON files to GPT-2 finetuning input text files.')

    parser.add_argument('json_dir', type=str,
                        help='the directory where the JSON files are located')

    parser.add_argument('-r', '--recursive', dest='recursive', action='store_true', default=False,
                        help='whether the JSON file search should be recursive')

    parser.add_argument('-o', '--output', dest='output', type=str, required=True,
                        help='the output file to write')

    args = parser.parse_args()

    # Convert to text and write
    # TODO: To be able to handle very large collections, we should not process everything at once
    output_txt = get_txt(args.json_dir, args.recursive)
    wrote_first_line = False

    with open(args.output, 'w', encoding='utf8') as output_file:
        for line in output_txt.splitlines():  # Split to prevent MemoryErrors when writing
            if wrote_first_line:
                output_file.write('\n')

            output_file.write(line)
            wrote_first_line = True
