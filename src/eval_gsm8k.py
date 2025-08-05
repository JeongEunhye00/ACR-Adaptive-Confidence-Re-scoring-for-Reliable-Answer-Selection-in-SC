import re
import json
from collections import Counter
import argparse
import os


def extract_prediction(output):
    output = re.sub(r"\$?\\frac\{([\d\.\,\-]+)\}\{([\d\.\,]+)\}\$?", r"\1/\2", output)
    output = re.sub(r"(?<![APap]\.[Mm])\.$", "", output)
    output = re.sub(r"(?<![APap][mM])$", "", output)
    output = re.sub(r"(?<=\d)[\=](?=[\-\$\d])", " = ", output)
    output = re.sub(r"\u2212", "-", output)
    output = output.replace("**", '')

    patterns = [
    r'[Tt]he answer is.*?(\d[\d,\.]*)',
    r' = ([\d\$\.\,\/\:]+)',
    r'\\boxed\{([\-\d\$\.\,\/\:]+)\}',
    r'boxed\{([\-\d\$\.\,\/\:]+)\}',
    r'\\\(([\-\d\$\.\,\/\:]+)\\\)',
    r'\b(?:be|is|are|was|were)\b\s+([\-\d\$\.\,\/\:]{0,}[\d]+)',
    r' ([\d\$\.\,\/\:]+ [APap]\.[Mm]\.)',
    r' ([\d\$\.\,\/\:]+ [APap][Mm]\.)',
    r'([\-\d\$\.\,\/\:]{0,}[\d]+)',
]

    for p in patterns:
        pattern = re.compile(p)
        res = pattern.findall(output)
        if len(res) > 0:
            # print(res)
            prediction = res[-1].strip()
            prediction = re.sub('\.+$', ".", prediction)
            prediction = re.sub(r"\.{2,}", ".", prediction)
           
            if prediction.endswith(","):
                prediction = prediction[-1]
            if prediction.endswith(".") and ".M." not in prediction:
                prediction = prediction[:-1]

            match = re.match(r"(\d{1,2}):\d{2} ?[AaPp]\.?[Mm]\.?", prediction)
            if match:
                return match.group(1) 
            return prediction

    return output


def normalize_answer(text):

    text = re.sub("^[\$]", "", text)
    text = re.sub("[\,\.\,\/]$", "", text)
    

    result = re.match("^[-+]?[\d,./]+$", text)

    if result is not None:
        # is number?
        text = text.replace(",", "")
        text = text.replace("$", "")
        result = re.match("[-+]?\d+$", text)

        if result is not None:
            number = int(text)
        elif "/" in text:
            nums = text.split("/")
            number = float(nums[0]) / float(nums[1])
        else:
            number = float(text)
        number = str(number)
        number = re.sub(r"\.[0]+$", "", number)

        return number, True
    else:
        return text, False


def majority_voting(pred, gold):
    cand_ans = []
    none_cnt = 0
    sc_answer = 'None'
    
    for res in pred:
        res = extract_prediction(res)
        res, isnum = normalize_answer(res)
        if isnum:
            cand_ans.append(res)
        else:
            none_cnt += 1
    
    if len(cand_ans) > 0:
        cand_ans = sorted(cand_ans, key=lambda x: x)
        cand_ans = Counter(cand_ans)
        cand_ans = [(x[0], x[1]) for x in cand_ans.items()]
        cand_ans = sorted(cand_ans, key=lambda x: (-1*x[1], float(x[0])))
    
        sc_answer = float(cand_ans[0][0])

        cand_ans = {float(k):v for k,v in cand_ans[:4]}
        
    return cand_ans, sc_answer, sc_answer==gold


def main():
    parser = argparse.ArgumentParser(description="Evaluate the generated responses.")
    parser.add_argument("--dataset_name", type=str, default="gsm8k", help="dataset name")
    parser.add_argument("--model_name", type=str, default="gemini-1.5-flash-8b", help="The model used to generate response.")
    parser.add_argument("--n_generation", type=int, default=20, help="Number of generation samples for each problem")
    parser.add_argument("--output_dir", type=str, default="output/gsm8k", help="generation output save dir")

    args = parser.parse_args()

    data_path = os.path.join(args.output_dir, f'{args.model_name}/generation/sc_{args.n_generation}_test.json')
    with open(data_path, 'r') as f:
        dataset = json.load(f)
    
    cor = 0
    ans_in_pred = 0
    results = [dataset[0]]
    incor_results = [dataset[0]]
    dataset = dataset[1:]

    for idx, data in enumerate(dataset):
        gold = float(data['gold_answer'])
        cand_ans, sc_ans, iscorrect = majority_voting(data['responses'][:], gold)

        tmp = {"id": idx,
            "question": data['question'],
            "gold_answer": gold,
            "sc_answer": sc_ans,
            "sc_pred": cand_ans}
        results.append(tmp)
        if iscorrect:
            cor += 1
        else:
            incor_results.append(tmp)
            if gold in cand_ans:
                ans_in_pred += 1
    
    save_dir = os.path.join(args.output_dir, args.model_name, 'evaluation')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f'eval_sc_{args.n_generation}_test.json')
    
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=4)

    if args.n_generation == 1:
        print("***** GD evaluation results *****")
    else:
        print("***** SC evaluation results *****")
    print(f"accuracy: {cor/(len(dataset))*100:.2f} %")
    print(f"correct: {cor}, incorrect: {len(dataset)-cor}, gold in sc_pred(incor): {ans_in_pred}")

if __name__ == "__main__":
    main()