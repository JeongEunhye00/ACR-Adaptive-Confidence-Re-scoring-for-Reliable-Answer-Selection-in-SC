gsm8k_prompt = """Answer the provided question. Always finish your response in the format: "The answer is x", where x is the numeric answer you believe is correct.

Question: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?
Answer: There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. The answer is 6.

Question: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?
Answer: There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5. The answer is 5.

Question: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?
Answer: Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. The answer is 39.

Question: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?
Answer: Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8. The answer is 8.

Question: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?
Answer: Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9. The answer is 9.

Question: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?
Answer: There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. 9 + 20 is 29. The answer is 29.

Question: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?
Answer: Michael started with 58 golf balls. After losing 23 on tuesday, he had 58 - 23 = 35. After losing 2 more, he had 35 - 2 = 33 golf balls. The answer is 33.

Question: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?
Answer: Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8. The answer is 8.
"""


gsm8k_prompt_op = """Choose one answer from the given options for the provided question. 
If the correct answer is not listed, select the option that is closest or most appropriate. 
Always finish your response in the format: "The answer is (n) x", where n is the option number and x is the option content.

Question: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?
Options: 
(1) 36
(2) 5
(3) 6
Answer: There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. The answer is (3) 6.

Question: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?
Options: 
(1) 5
(2) 1
Answer: There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5. The answer is (1) 5.

Question: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?
Options: 
(1) 39
(2) 77
(3) 7
Answer: Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. The answer is (1) 39.

Question: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?
Options: 
(1) 32
(2) 8
Answer: Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8. The answer is (2) 8.

Question: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?
Options: 
(1) 9
(2) -1
(3) 7
Answer: Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9. The answer is (1) 9.

Question: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?
Options: 
(1) 20
(2) 45
(3) 29
Answer: There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. 9 + 20 is 29. The answer is (3) 29.

Question: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?
Options: 
(1) 33
(2) 35
(3) 81
Answer: Michael started with 58 golf balls. After losing 23 on tuesday, he had 58 - 23 = 35. After losing 2 more, he had 35 - 2 = 33 golf balls. The answer is (1) 33.

Question: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?
Options: 
(1) 15
(2) 20
(3) 6
(4) 8
Answer: Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8. The answer is (4) 8.
"""


gsm8k_prompt_sv = """Answer the provided question.
Always finish your response with the phrase: "So the answer is x", where x is either "True" or "False".

Question: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today? I think the answer is 6. Is it correct (True or False)?
Answer: There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. So the answer is True.

Question: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot? I think the answer is 1. Is it correct (True or False)?
Answer: There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5. So the answer is False.

Question: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total? I think the answer is 74. Is it correct (True or False)?
Answer: Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. So the answer is False.

Question: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny? I think the answer is 8. Is it correct (True or False)?
Answer: Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8. So the answer is True.

Question: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now? I think the answer is 10. Is it correct (True or False)?
Answer: Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9. So the answer is False.

Question: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room? I think the answer is 29. Is it correct (True or False)?
Answer: There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. 9 + 20 is 29. So the answer is True.

Question: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday? I think the answer is 33. Is it correct (True or False)?
Answer: Michael started with 58 golf balls. After losing 23 on tuesday, he had 58 - 23 = 35. After losing 2 more, he had 35 - 2 = 33 golf balls. So the answer is True.

Question: Olivia has $23. She bought five bagels for $3 each. How much money does she have left? I think the answer is 20. Is it correct (True or False)?
Answer: Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8. So the answer is False.
"""

import random
random.seed(42)

def build_option_prompt(example, n_option=4):
    prompt = gsm8k_prompt_op + "\n\n"

    question = example['question']

    prompt += f"Question: {question}" + "\n"
    
    prompt += "Options: " + "\n"
    opt = ""
    cand_ans = example['sc_pred']
    cand_ans = [(str(x[0]), x[1]) for x in cand_ans.items()]
    # random.shuffle(cand_ans)
    # cand_ans = sorted(cand_ans, key=lambda x: x[1], reverse=True)
    for idx, ans in enumerate(cand_ans[:n_option]):
        if int(float(ans[0])) == float(ans[0]):
            opt += f"({idx+1}) {int(float(ans[0]))}\n"
        else:
            opt += f"({idx+1}) {ans[0]}\n"
    prompt += opt
    
    prompt += "Answer: "
    cand_ans = {cand[0]:cand[1] for cand in cand_ans}
    
    return prompt, cand_ans