color_prompt = """Answer extremely simple questions about the colors of objects on a surface. 
Always determine a single, unambiguous answer. Do not give multiple possibilities.
Always finish your response in the format: "So the answer is x", where x is the answer you believe is correct.

Question: On the nightstand, there is a red pencil, a purple mug, a burgundy keychain, a fuchsia teddy bear, a black plate, and a blue stress ball. What color is the stress ball?
Answer: Let's think step by step.
According to this question, the color of the stress ball is blue. So the answer is blue.

Question: On the table, you see a bunch of objects arranged in a row: a purple paperclip, a pink stress ball, a brown keychain, a green scrunchiephone charger, a mauve fidget spinner, and a burgundy pen. What is the color of the object directly to the right of the stress ball?
Answer: Let's think step by step.
According to this question, the objects are arranged in a row, from left to right, as follows: (1) a purple paperclip, (2) a pink stress ball, (3) a brown keychain, (4) a green scrunchiephone charger, (5) a mauve fidget spinner, (6) a burgundy pen.
The stress ball is the second object on the list, namely (2). The object that is to the right of the stress ball corresponds to (3), which is a brown keychain.
The color of the keychain is brown. So the answer is brown.

Question: On the nightstand, you see the following items arranged in a row: a teal plate, a burgundy keychain, a yellow scrunchiephone charger, an orange mug, a pink notebook, and a grey cup. How many non-orange items do you see to the left of the teal item?
Answer: Let's think step by step.
According to this question, the objects are arranged in a row, from left to right, as follows: (1) a teal plate, (2) a burgundy keychain, (3) a yellow scrunchiephone charger, (4) an orange mug, (5) a pink notebook, (6) a grey cup.
The teal plate is the first item, namely (1). There is no item to the left of the teal item.
The number of non-orange items to the left of the teal item is 0. So the answer is 0.
"""

color_prompt_op = """Choose one answer from the given options for the provided question. If the correct answer is not listed, select the option that is closest or most appropriate. Always finish your response in the format: \"The answer is x\", where x is the answer you believe is correct.

Question: On the nightstand, there is a red pencil, a purple mug, a burgundy keychain, a fuchsia teddy bear, a black plate, and a blue stress ball. What color is the stress ball?
Options: 
(A) blue
(B) purple
(C) black
Answer: Let's think step by step. According to this question, the color of the stress ball is blue. \"The answer is blue\".

Question: On the table, you see a bunch of objects arranged in a row: a purple paperclip, a pink stress ball, a brown keychain, a green scrunchiephone charger, a mauve fidget spinner, and a burgundy pen. What is the color of the object directly to the right of the stress ball?
Options: 
(A) pink
(B) brown
(C) mauve
(D) green
Answer: Let's think step by step. According to this question, the objects are arranged in a row, from left to right, as follows: (1) a purple paperclip, (2) a pink stress ball, (3) a brown keychain, (4) a green scrunchiephone charger, (5) a mauve fidget spinner, (6) a burgundy pen.
The stress ball is the second object on the list, namely (2). The object that is to the right of the stress ball corresponds to (3), which is a brown keychain. The color of the keychain is brown. \"The answer is brown\".

Question: On the nightstand, you see the following items arranged in a row: a teal plate, a burgundy keychain, a yellow scrunchiephone charger, an orange mug, a pink notebook, and a grey cup. How many non-orange items do you see to the left of the teal item?
Options: 
(A) 0
(B) 1
(C) 5
Answer: Let's think step by step. According to this question, the objects are arranged in a row, from left to right, as follows: (1) a teal plate, (2) a burgundy keychain, (3) a yellow scrunchiephone charger, (4) an orange mug, (5) a pink notebook, (6) a grey cup. The teal plate is the first item, namely (1). There is no item to the left of the teal item. The number of non-orange items to the left of the teal item is 0. \"The answer is 0\".
"""


def build_option_prompt(example, n_option=4):
    prompt = color_prompt_op + "\n\n"

    question = example['question']

    prompt += f"Question: {question}" + "\n"
    
    prompt += "Options: " + "\n"
    opt = ""
    cand_ans = example['sc_pred']
    cand_ans = [(str(x[0]), x[1]) for x in cand_ans.items()]
    cand_ans = sorted(cand_ans, key=lambda x: x[1], reverse=True)
    for idx, ans in enumerate(cand_ans[:n_option]):
        opt += f"({chr(idx+65)}) {ans[0]}\n"
    prompt += opt
    
    prompt += "Answer: "
    cand_ans = {cand[0]:cand[1] for cand in cand_ans}
    
    return prompt, cand_ans