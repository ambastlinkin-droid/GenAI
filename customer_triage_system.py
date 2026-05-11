import os
from dotenv import load_dotenv
import openai
import pandas as pd
import io

load_dotenv()  # loads from .env file
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

csv_data = """review_id,review_text
1,"This is the best coffee maker I've ever owned! It brews the perfect cup every single time. 5 stars!"
2,"The product is great, but the shipping box was completely crushed and it arrived two days late."
3,"I ordered the blue headphones but received the green ones. How can I start an exchange?"
4,"The t-shirt material feels cheap and it shrank after one wash. Very disappointed and would not recommend."
5,"It's okay. Does the job, I guess. Nothing special."
6,"Wow! The setup was a breeze and the user interface is so intuitive. However, the battery life is much shorter than advertised."
"""

df = pd.read_csv(io.StringIO(csv_data))
print("Data loaded successfully!")

#Ground truth data
ground_truth_data = [
    {"review_id":1, "ground_truth":{
        "overal_sentiment": "Positive",
        "aspects":[
            {"aspect_name":"product_quality", "sentiment":"Positive",
             "summary":"Customer calls it the best coffee maker they've owned."}
        ]}},
    {"review_id": 2, "ground_truth": {
        "overall_sentiment": "Mixed",
        "aspects": [
            {"aspect_name": "product_quality",    "sentiment": "Positive", "summary": "The product itself is great."},
            {"aspect_name": "delivery_condition", "sentiment": "Negative", "summary": "The shipping box was crushed."},
            {"aspect_name": "delivery_speed",     "sentiment": "Negative", "summary": "Arrived two days late."}
        ]}},

    {"review_id":3, "ground_truth":{
        "overall_sentiment":"Negative",
        "aspects":[
            {"aspect_name":"product_quality","sentiment":"Negative","summary":"Received the wrong color (green instead of blue)."},
            {"aspect_name": "customer_service", "sentiment": "Neutral",  "summary": "Customer is asking about the exchange process."}
        ]}},
    
    {"review_id": 4, "ground_truth": {
        "overall_sentiment": "Negative",
        "aspects": [
            {"aspect_name": "product_quality", "sentiment": "Negative",
             "summary": "Material feels cheap and the t-shirt shrank after one wash."}
        ]}},

    {"review_id": 5, "ground_truth": {
        "overall_sentiment": "Neutral",
        "aspects": [
            {"aspect_name": "product_quality", "sentiment": "Neutral",
             "summary": "Customer finds the product acceptable but unremarkable."}
        ]}},

    {"review_id": 6, "ground_truth": {
        "overall_sentiment": "Mixed",
        "aspects": [
            {"aspect_name": "app_experience",  "sentiment": "Positive", "summary": "Setup was easy and the UI is intuitive."},
            {"aspect_name": "product_quality", "sentiment": "Negative", "summary": "Battery life is much shorter than advertised."}
        ]}}

]

#----------------------------MERGING STARTS-------------------------------------#
get_df = pd.DataFrame(ground_truth_data) #converting GT to dataframe
df = df.merge(get_df,on="review_id") #merging csv + ground_truth
print("Ground truth merged with the csv data based on review id")
#----------------------------MERGING ENDS---------------------------------------#
#Part: 1
zero_shot_prompt = """
You are a customer feedback analyst for ShopSphere, an e-commerece platform.

Analyze the following customer review and extract:

1. overall_sentiment -> must be one of: Positive, Negative, Neutral, Mixed
2. A short summary of what the customer is saying (1-2 sentences max)

Review:
{review_text}

Respond in this exact JSON format:
{{
        "overall_sentiment": "...",
        "summary": "...",
        
}}
"""

#Part: 2
few_shot_prompting = """
You are a customer feedback analyst for ShopSphere, an e-commerce platform.

Your job is to analyze a customer review and extract structured feedback in JSON format.

Each JSON Output MUST contain:
- Overall_sentiment -> one of: Positive, Negative, Neutral, Mixed
-> summary  1-2 sentences summary of whole review
-> aspects  list of specific aspects mentioned, each with:
    -aspects_name -> one of: product_quality, packaging, delivery_speed,
    delivery_condition, returns refunds, customer_service,
    price_value, app_experience

    - sentiment -> Positive, Negative, or Neutral
    - summary   -> one sentence about that specific aspect

Here are some examples:

EXAMPLE 1:

Review: "Absolutely love this blender! it's powerful, quiet, and easy to clean. ",

Output:

{{
    "overall_sentiment": "Positive",
    "summary": "The customer is very happy with the blender praising its power, noise level, and ease of cleaning.",
    "aspects":[
    {{
        "aspect_name":"Product Quality",
        "sentiment": "Positive",
        "summary":"Customer find the blender powerful, quiet, and easy to clean."
    }}
]
}}


────────────────────────────────────────────────
Example 2:
Review: "The jacket looks great but the zipper broke after just 1 week. Also took 10 days to arrive."

Output:

{{

"overall_sentiment": "Mixed",
"summary": "The customer likes the jacket's appearance but is disappointed by a broken zipper and slow delivery.",
"aspects":[
    {{
        "aspect_name":"product_quality",
        "sentiment":"Negative",
        "summary": "The zipper broke only after one week of use"
    }},
    {{
        "aspect_name":"delivery speed",
        "sentiment": "Negative",
        "summary": "The order took 10 days to arrive."
    
    }},
    {{
        "aspect_name":"price_value",
        "sentiment":"positive"
        "summary":"Customer appreciates the visual appearance of the jacket".
    }}
]

}}

────────────────────────────────────────────────
EXAMPLE 3:

Review: "I was charged twice for the same order. Customer support help me fix it quickly though."

Output:

{{
    "overall_sentiment": "Mixed",
    "summary": "The customer faced a billing issue but appreciated the quick resolution by customer support.",
    "aspects":[
        {{
            "aspect_name":"price_value",
            "sentiment":"Negative",
            "summary":"Customer was incorrectly charged twice for the same order."
        }},
        {{
            "aspect_name":"customer_service",
            "sentiment":"Positive",
            "summary":"Support team resolved the billing issue quickly."
        }}
    ]
}}

────────────────────────────────────────────────
Now analyze this review

Review: {review_text}

Respond with JSON only - no extra text, no code blocks.

"""
#Part: 3

cot_prompt = """

You are a customer feedback analyst for ShopSphere, an e-commerece platorm.

Before giving your final JSON output, think through the review step-by-step.

Follow these reasoning steps:

STEP 1: Read the review carefully
        what is the customer mainly thinking about?

STEP 2: Identify every distinct aspects mentioned.
        Only use these aspects names:
        Product_quality, packaging, delivery_speed, delivery_condition,
        returns_refunds, customer_service, price_value, app_experience

STEP 3: For each aspects you identified:
        - Is customer happy, unhappy, or neutral about it?
        - What exactly did they say about it?

STEP 4: Look at the review as a whole.
        - If ALL aspects are Positive: overall_sentiment = Positive
        - if ALL aspects are Negative: overall_sentiment = Negative
        - if ALL aspects are Mixed:    overall_sentiment = Mixed
        - if no strong feeling either way: overall_sentiment = Neutral

STEP 5: Now produce the final JSON output

────────────────────────────────────────────────
EXAMPLE - watch how the thinking leads to the output:

Review: "The shoes look amazing but they gave me blisters
         Delivery was super fast though! Also I had to call
         Support three times before anyone helped me."

THINKING:

- Step 1: Customer talks about the shoe appearance, comfort, delivery, and support.
- Step 2: Aspects-> product_quality,delivery_speed,customer_service
- Step 3: 
       product_quality -> Negative (looks good but caused blisters)
       delivery_speed -> Positive (Super fast)
       customer_service -> Negative (had to call 3 times)
- Step 4: Mix of positive and Negative -> overall_sentiment = Mixed


Output Format:

{{
"overall_sentiment":"Mixed",
"summary": "Customer likes the shoe appearance and fast delivery but is unhappy with comfort and poor customer support.",
"aspects":[
    {{
        "aspect_name":"product_quality",
        "sentiment":"Negative",
        "summary": "Shoes look good but caused blisters when worn."
    }},
    {{
        "aspect_name":"delivery_speed",
        "sentiment":"Positive",
        "summary":"Delivery was very fast."
    }},
    {{
        "aspect_name":"customer_service",
        "sentiment":"Negative",
        "summary":"Customer had to call support three times before getting help."
    }}
]

}}

───────────────────────────────────────────────
Now analyze this review using the same thinking steps:

Review: {review_text}

First write your THINKING steps, then output the final JSON.
Wrap the JSON in <json> and </json> tags like this:

<json>
{{
    ...
}}
</json>
"""


#Zero shot
def analyze_review_zero_shot(review_text):
     prompt = zero_shot_prompt.format(review_text=review_text)
     response = client.chat.completions.create(
         model = "gpt-4o-mini",
         temperature=0.4,
         messages=[
             {"role":"user","content":prompt}
         ]
     )
     return response.choices[0].message.content
#Few Shot
def analyze_few_shot(review_text):
    prompt = few_shot_prompting.format(review_text=review_text)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        messages=[

            {"role":"user","content":prompt}
        ]
    )
    return response.choices[0].message.content

#CoT - Chain of thought.
def analyze_review_cot(review_text):
    prompt = cot_prompt.format(review_text=review_text)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    raw = response.choices[0].message.content
    try:
        json_part = raw.split("<json>")[1].split("</json>")[0].strip()
        return json_part
    except:
        return raw #if the tags are missing

#Self-Consistency!



for index, row in df.iterrows():
    print(f"\n--- Review #{row['review_id']} ---")
    
    #What the model said
    #print("Model Said!")
    zero_shot = analyze_review_zero_shot(row['review_text'])
    few_shot  = analyze_few_shot(row['review_text'])
    cot       = analyze_review_cot(row['review_text'])
    
    # What the correct answer is
    print("Correct Answer!")
    #my csv data was updated with the ground truth earlier now it has ground_truth also in it.
    print(f"Ground Truth : {row['ground_truth']}")
    
    # Side by side comparison
    print(f"Zero Shot    : {zero_shot}")
    print(f"Few Shot     : {few_shot}")
    print(f"CoT          : {cot}")