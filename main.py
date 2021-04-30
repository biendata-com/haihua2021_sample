from argparse import ArgumentParser
import pandas as pd

def random_result(input_path, output_file):
    import random
    import json
    with open(input_path) as file:
        j = json.load(file)

    with open(output_file, 'w') as w:
        w.write('id,label\n')
        for i in j:
            for q in i['Questions']:
                w.write(q['Q_id'] + ',' + ['A','B','C','D'][random.randint(0,3)] + '\n')
                
    

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-input", type=str, required=True)
    parser.add_argument("-output", type=str, required=True)
    args = parser.parse_args()

    random_result(args.input, args.output)

    
