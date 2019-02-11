import sys
import json
import parse_classes as parser


def main():
    if(len(sys.argv) < 2):
        print("Please pass input JSON file as argument")
        sys.exit()
    else:
        with open(sys.argv[1], encoding='utf-8-sig') as json_file:
            data = json.load(json_file)
            print(data)
            res = parser.parse(data)
            output = open("output.json", "w")
            output.write(json.dumps(res, indent=2))
            output.close()



if __name__ == "__main__":
    main()
