import google.generativeai as genai
from tqdm import tqdm
import json
import os
import argparse
from prompt import build_option_prompt


def select_option(example, llm, llm_config_op, debug=False, n_option=4):
    prompt, cand_ans = build_option_prompt(example, n_option)
    
    responses = llm.generate_content(prompt, generation_config=llm_config_op)
    responses = responses.text

    if debug:
        print(prompt)
        print(responses)
    
    return responses, cand_ans


def Self_consistency_Option_results(dataset, output_path, cnt, n_selection, n_option, llm, llm_config, cfg=None):
    if cnt != 0:
        with open(output_path) as f:
            results = json.load(f)
    else:
        results = [cfg]
    
    for data in dataset:
        print(f"***** data id {data['id']} *****")
        tmp = data
        tmp['responses'] = []
        sc_pred = data['sc_pred'].copy()

        if len(sc_pred) > 1:
            for i in tqdm(range(n_selection)):
                attempt = 0
                retries = 5
                while attempt < retries:
                    try:
                        res, cand_ans = select_option(data, llm, llm_config, debug=False, n_option=n_option)
                        break
                    except Exception as e:
                        attempt += 1
                        print(f"attempt - {attempt}")
                        print(f"Error - {e}")
                        import time
                        time.sleep(1)
                
                tmp['responses'].append(res)
                if i == 0:
                    tmp['sc_pred'] = cand_ans

        results.append(tmp)
        cnt += 1
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=4)


model_versions = {"gemini-1.5-flash-8b": "models/gemini-1.5-flash-8b"}


def main():
    parser = argparse.ArgumentParser(description="Run the novel solution generation program.")
    parser.add_argument("--seed", type=int, default=42, help="randoom seed setting")
    parser.add_argument("--dataset_name", type=str, default="gsm8k", help="dataset name")
    
    parser.add_argument("--model_name", type=str, default="gemini-1.5-flash-8b", help="The model used to generate response.")
    parser.add_argument("--n_selection", type=int, default=5, help="Number of generation samples for each problem")
    parser.add_argument("--n_option", type=int, default=4, help="Number of top-k options for each problem")
    
    parser.add_argument("--do_sample", type=bool, default=True, help="do sample")
    parser.add_argument("--temperature", type=float, default=0.5, help="LLM temperature setting")
    parser.add_argument("--top_p", type=float, default=1.0, help="LLM top_p setting")
    parser.add_argument("--top_k", type=int, default=50, help="LLM top_p setting")
    parser.add_argument("--max_new_tokens", type=int, default=350, help="maximum new generation tokens")

    parser.add_argument("--log_dir", type=str, default="logs", help="logging log dir")
    parser.add_argument("--log_level", type=str, default="INFO", help="logging log level")

    parser.add_argument("--cache_dir", type=str, default="cache", help="model cache dir")
    parser.add_argument("--data_path", type=str, default="output/gsm8k/gemini-1.5-flash-8b/evaluation/eval_sc_20_test.json", help="dataset path")
    parser.add_argument("--output_dir", type=str, default="output/gsm8k", help="generation output save dir")

    args = parser.parse_args()

    output_dir = os.path.join(args.output_dir, args.model_name, 'generation')
    os.makedirs(output_dir, exist_ok=True)

    model = model_versions[args.model_name]
    temp = args.temperature
    n_sel = args.n_selection
    max_new_tokens = args.max_new_tokens
    n_option = args.n_option

    cfg = {'model': model,
           'temperature': temp,
           'max_output_token': max_new_tokens,
           'n_selection': n_sel}
    
    with open(args.data_path, 'r') as f:
        dataset = json.load(f)
        dataset = dataset[1:]
    
    output_path = os.path.join(output_dir, f'op_sc_{n_sel}_test.json')


    GOOGLE_API_KEY = "API_KEY"
    genai.configure(api_key=GOOGLE_API_KEY)
    
    llm = genai.GenerativeModel(model_name=model)
    llm_config = genai.types.GenerationConfig(
            candidate_count=1,
            max_output_tokens=max_new_tokens,
            temperature=temp,
        )
    cnt = 0
    Self_consistency_Option_results(dataset, output_path, cnt, n_sel, n_option, llm, llm_config, cfg)


if __name__ == "__main__":
    main()