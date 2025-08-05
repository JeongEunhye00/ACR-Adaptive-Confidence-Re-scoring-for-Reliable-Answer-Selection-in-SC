tabmwp_prompt = """Read the following table and then answer the provided question. Always finish your response in the format: "The answer is x", where x is the answer you believe is correct.

Table: Number of streets | Number of traffic cones
1 | 5
2 | 10
3 | 15
4 | ?
Question: Each street has 5 traffic cones. How many traffic cones are on 4 streets?
Answer: Count by fives. Use the chart: there are 20 traffic cones on 4 streets. The answer is 20.

Table: Number of vans | Number of empty seats
1 | 2
2 | 4
3 | 6
4 | ?
Question: Each van has 2 empty seats. How many empty seats are in 4 vans?
Answer: Count by twos. Use the chart: there are 8 empty seats in 4 vans. The answer is 8.

Table: Type | Number of respondents
White chocolate | 870
Milk chocolate | 280
Dark chocolate | 140
Question: A survey was conducted to learn people's chocolate preferences. What fraction of the respondents preferred white chocolate? Simplify your answer.
Answer: Find how many respondents preferred white chocolate.
870
Find how many people responded in total.
870 + 280 + 140 = 1,290
Divide 870 by1,290.
\frac{870}{1,290}
Reduce the fraction.
\frac{870}{1,290} → \frac{29}{43}
\frac{29}{43} of respondents preferred white chocolate. The answer is 29/43.

Table: chestnuts | $12/pound
peanuts | $6/pound
pine nuts | $5/pound
macadamia nuts | $12/pound
Brazil nuts | $9/pound
pistachios | $12/pound
Question: How much would it cost to buy 4/5 of a pound of peanuts?
Answer: Find the cost of the peanuts. Multiply the price per pound by the number of pounds.
$6 × \frac{4}{5} = $6 × 0.8 = $4.80
It would cost $4.80. The answer is 4.80.
"""


tabmwp_prompt_op = """Read the following table and then must select one option from the given options for the provided question. If the correct answer is not listed, select the option that is closest or most appropriate. Always finish your response in the format: \"The answer is x\", where x is the answer you believe is correct.

Table: Number of streets | Number of traffic cones
1 | 5
2 | 10
3 | 15
4 | ?
Question: Each street has 5 traffic cones. How many traffic cones are on 4 streets?
Options: 
(1) 20
(2) 19
(3) 24
Answer: Count by fives. Use the chart: there are 20 traffic cones on 4 streets. \"The answer is 20\".

Table: Number of vans | Number of empty seats
1 | 2
2 | 4
3 | 6
4 | ?
Question: Each van has 2 empty seats. How many empty seats are in 4 vans?
Options: 
(1) 8
(2) 10
Answer: Count by twos. Use the chart: there are 8 empty seats in 4 vans. \"The answer is 8\".

Table: [Title] Chocolate preferences
Type | Number of respondents
White chocolate | 870
Milk chocolate | 280
Dark chocolate | 140
Question: A survey was conducted to learn people's chocolate preferences. What fraction of the respondents preferred white chocolate? Simplify your answer.
Options: 
(1) 29/43
(2) 870/1290
Answer: Find how many respondents preferred white chocolate: 870. Find how many people responded in total: 870 + 280 + 140 = 1290. Divide 870 by 1290 = 870 /1290 is 29/43. \"The answer is 29/43\".

Table: chestnuts | $12/pound
peanuts | $6/pound
pine nuts | $5/pound
macadamia nuts | $12/pound
Brazil nuts | $9/pound
pistachios | $12/pound
Question: How much would it cost to buy 4/5 of a pound of peanuts?
Options: 
(1) 4.80
(2) 5.00
(3) 3.80
Answer: Find the cost of the peanuts. Multiply the price per pound by the number of pounds: 6 * 4/5 = 6 * 0.8 = 4.80. It would cost $4.80. \"The answer is 4.80\".
"""

