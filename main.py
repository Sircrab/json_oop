import sys
import json
import parse_classes as parser


def main():
    if(len(sys.argv) < 2):
        print("Please pass input JSON file as argument")
        sys.exit()
    else:
        with open(sys.argv[0], encoding='utf-8-sig') as json_file:
            data = json.load(json_file)
            parser.parse(data)


if __name__ == "__main__":
    main()
