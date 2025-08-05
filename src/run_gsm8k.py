import json
import google.generativeai as genai
from tqdm import tqdm
import random
import argparse
import logging
import os
from prompt import gsm8k_prompt as demo


def generate_answer(question, llm, llm_config=None, debug=False):
    prompt = demo + "\n\n"
    prompt += f"Question: {question}\n"
    prompt += "Answer: "

    responses = llm.generate_content(prompt, generation_config=llm_config)
    responses = responses.text

    if debug:
        print(prompt)
        print(responses)
    
    return responses


def Self_consistency_results(dataset, output_path, cnt, n_generation, llm_config, llm, cfg=None):
    dataset = dataset[cnt:]

    if cnt != 0:
        with open(output_path) as f:
            results = json.load(f)
    else:
        results = [cfg]
    
    for data in dataset:
        print(f"***** data {cnt} *****")
        tmp = {'id' : data['id'],
               'question': data['question'],
               'gold_answer' : data['answer'],
               'responses': []}
        for i in tqdm(range(n_generation)):
            attempt = 0
            retries = 5
            while attempt < retries:
                try:
                    res = generate_answer(data['question'], llm, llm_config)
                    break
                except Exception as e:
                    attempt += 1
                    print(f"attempt - {attempt}")
                    print(f"Error - {e}")
                    import time
                    time.sleep(1)
            tmp['responses'].append(res)
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
    parser.add_argument("--n_generation", type=int, default=20, help="Number of generation samples for each problem")
    
    parser.add_argument("--do_sample", type=bool, default=True, help="do sample")
    parser.add_argument("--temperature", type=float, default=0.7, help="LLM temperature setting")
    parser.add_argument("--top_p", type=float, default=1.0, help="LLM top_p setting")
    parser.add_argument("--top_k", type=int, default=50, help="LLM top_p setting")
    parser.add_argument("--max_new_tokens", type=int, default=350, help="maximum new generation tokens")

    parser.add_argument("--log_dir", type=str, default="logs", help="logging log dir")
    parser.add_argument("--log_level", type=str, default="INFO", help="logging log level")

    parser.add_argument("--cache_dir", type=str, default="cache", help="model cache dir")
    parser.add_argument("--data_path", type=str, default="dataset/gsm8k/test.json", help="dataset path")
    parser.add_argument("--output_dir", type=str, default="output/gsm8k", help="generation output save dir")

    args = parser.parse_args()

    output_dir = os.path.join(args.output_dir, args.model_name, 'generation')
    os.makedirs(output_dir, exist_ok=True)

    model = model_versions[args.model_name]
    temp = args.temperature
    n_gen = args.n_generation
    max_new_tokens = args.max_new_tokens

    cfg = {'model': model,
           'temperature': temp,
           'max_output_token': max_new_tokens,
           'n_generation': n_gen}
    
    with open(args.data_path, 'r') as f:
        dataset = json.load(f)
    
    output_path = os.path.join(output_dir, f'sc_{n_gen}_test.json')


    GOOGLE_API_KEY = "API_KEY"
    genai.configure(api_key=GOOGLE_API_KEY)

    llm = genai.GenerativeModel(model_name=model)
    llm_config = genai.types.GenerationConfig(
            candidate_count=1,
            max_output_tokens=max_new_tokens,
            temperature=temp,
        )
    cnt = 0
    Self_consistency_results(dataset, output_path, cnt, n_gen, llm_config, llm, cfg)


if __name__ == "__main__":
    main()