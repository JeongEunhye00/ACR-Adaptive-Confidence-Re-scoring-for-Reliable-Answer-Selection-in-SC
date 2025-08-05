import json
import numpy as np
import argparse
from collections import Counter

def main():
    parser = argparse.ArgumentParser(description="Evaluate the generated responses.")
    parser.add_argument("--dataset_name", type=str, default="gsm8k", help="dataset name")
    parser.add_argument("--model_name", type=str, default="gemini-1.5-flash-8b", help="The model used to generate response.")
    parser.add_argument("--output_dir", type=str, default="output/gsm8k", help="generation output save dir")
    parser.add_argument("--eval_dir", type=str, default="output/gsm8k", help="generation output save dir")
    parser.add_argument("--sv", action='store_true')
    parser.add_argument("--sc_gen", type=int, default=20, help="# of reasoning paths in SC")
    parser.add_argument("--so_gen", type=int, default=5, help="# of reasoning paths in SO")
    parser.add_argument("--scoring_func", type=int, default=0, help="0: Sum, 1: Product, 2: Fobar, 3:SC-Boost")

    args = parser.parse_args()

    eval_file = f'output/{args.dataset_name}/{args.model_name}/evaluation/eval_op_sc_5_test_random.json'
    print(eval_file)
    final_acc = 0
    f_acc = []

    fin_cor, fin_incor = 0,0
    fin_delta = 0
    eps = 1e-8
    alpha = 0.5
    beta = 1 - alpha
    scx_acro = []

    with open(eval_file, 'r') as f:
        results = json.load(f)
        results = results[1:]

    sc_o, sc_x, op_o, op_x = 0,0,0,0
    gold_in_sc_pred = 0

    for data in results:
        gold = data['gold_answer']
        sc_pred = data['sc_pred']
        op_pred = data['op_pred']
        sc_answer = data['sc_answer']
        op_answer = data['op_answer']

        if gold == sc_answer:
                sc_o += 1     
        else:
            sc_x += 1
            if str(gold) in sc_pred:
                gold_in_sc_pred += 1
        
        if gold == op_answer:
            op_o += 1
        else:
            op_x += 1
    
    print("***** SC evaluation results *****")
    print(f"accuracy: {sc_o/(sc_o+sc_x)*100:.2f} %")
    print(f"correct: {sc_o}, incorrect: {sc_x}, gold in sc_pred(incor): {gold_in_sc_pred}")

    print("***** OP evaluation results *****")
    print(f"accuracy: {op_o/(op_o+op_x)*100:.2f} %")
    print(f"correct: {op_o}, incorrect: {op_x}")

    if args.sv:
        if args.model_name == 'gemini-1.5-flash-8b':
            sv_eval_file = f'output/{args.dataset_name}/{args.model_name}/generation/sv_sc_5_test.json'
        else:
            sv_eval_file = f'output/{args.dataset_name}/{args.model_name}/generation/sv_sc_5_test_all.json'
        sv_o, sv_x = 0,0
        fo_o, fo_x = 0,0
        eps = 1e-8
        alpha = 0.5
        beta = 1 - alpha
        with open(sv_eval_file, 'r') as f:
            results = json.load(f)
            results = results[1:]

        for data in results:
            gold = data['gold_answer']
            sv_ans = data['sv_answer']
            if gold == sv_ans:
                sv_o += 1
            else:
                sv_x += 1
            
            fw = data['sc_pred']
            if len(fw) > 1:
                bw = data["sv_scores"]
                if sum(bw.values()) != 0:
                    fw = {k: v/sum(fw.values()) for k,v in fw.items()}
                    bw = {k: v/(eps + sum(bw.values())) for k,v in bw.items()}
                    fobar = {}
                    for cand_ans in list(fw.keys())[:4]:
                        fobar[cand_ans] = ((fw[cand_ans])**alpha) * ((bw[cand_ans])**beta)
                    data['fobar_scores'] = fobar
                    fo_ans = float(max(fobar, key=fobar.get))
                else:
                    fo_ans = data['sc_answer']
            else:
                fo_ans = data['sc_answer']
            data['fobar_answer'] = fo_ans
            if gold == fo_ans:
                fo_o += 1
            else:
                fo_x += 1
    
        print("***** SV evaluation results *****")
        print(f"accuracy: {sv_o/(sv_o+sv_x)*100:.2f} %")
        print(f"correct: {sv_o}, incorrect: {sv_x}")

        print("***** FOBAR evaluation results *****")
        print(f"accuracy: {fo_o/(fo_o+fo_x)*100:.2f} %")
        print(f"correct: {fo_o}, incorrect: {fo_x}")


    for delta in list(np.arange(0, 1.05, 0.05)):
        sc_o, sc_x, op_o, op_x = 0,0,0,0
        oo, ox, xo, xx = 0,0,0,0
        f_data = 0
        with open(eval_file, 'r') as f:
            results = json.load(f)
            results = results[1:]
        cand_cnt = []
        for data in results:
            gold = data['gold_answer']
            sc_pred = data['sc_pred']
            op_pred = data['op_pred']
            sc_answer = data['sc_answer']
            op_answer = data['op_answer']
            
            if sc_pred:
                data['sc_pred'] = {k:v/args.sc_gen for k, v in sc_pred.items()}
            else:
                data['sc_pred'] = {"None": 1.0}

            if op_pred:
                data['op_pred'] = {k:v/args.so_gen for k, v in op_pred.items()}
            else:
                data['op_pred'] = {sc_answer: 1.0}

            final_pred = data['sc_pred'].copy()

            if len(data['sc_pred']) > 1:
                cand_cnt.append(len(data['sc_pred']))
                stds = np.std(list(data['sc_pred'].values()))
                if stds <= delta:
                    f_data += 1
                    final_pred = data['op_pred'].copy()
                    for op in data['op_pred']:
                        if op in data['sc_pred']:
                            if args.scoring_func == 0:
                                final_pred[op] = data['sc_pred'][op] + data['op_pred'][op] 
                            elif args.scoring_func == 1:
                                final_pred[op] = data['sc_pred'][op] * data['op_pred'][op]
                            elif args.scoring_func == 2:
                                final_pred[op] = (data['sc_pred'][op]**alpha) * (data['op_pred'][op]**beta)
                            elif args.scoring_func == 3:
                                final_pred[op] = data['sc_pred'][op] + data['sc_pred'][op] * data['op_pred'][op]
                else:
                    final_pred = data['sc_pred']
            
            final_answer = [k for k,v in final_pred.items() if max(final_pred.values()) == v]
            final_answer = float(final_answer[0]) if final_answer[0] != "None" else final_answer[0]
            data['final_pred'] = final_pred
            data['final_ans'] = final_answer

            if final_answer == gold:
                if gold == sc_answer:
                    oo += 1
                else:
                    xo += 1
                    data['delta'] = delta
                    scx_acro.append(data)
            else:
                if gold == sc_answer:
                    ox += 1
                else:
                    xx += 1
            
        f_acc.append((oo+xo)/(oo+ox+xo+xx)*100)
        if final_acc < (oo+xo)/(oo+ox+xo+xx)*100:
            final_acc = (oo+xo)/(oo+ox+xo+xx)*100
            fin_cor = oo+xo
            fin_incor = ox+xx
            fin_acc = final_acc
            fin_delta = delta
            
            with open(f'output/{args.dataset_name}/{args.model_name}/evaluation/ACR_res.json', 'w') as f:
                json.dump(results, f, indent=4)

    print(f"***** ACR evaluation results - delta : {fin_delta}*****")
    print(f"accuracy: {fin_cor/(fin_cor+fin_incor)*100:.2f} %")
    print(f"correct: {fin_cor}, incorrect: {fin_incor}")

    print(f_acc)

if __name__ == "__main__":
    main()