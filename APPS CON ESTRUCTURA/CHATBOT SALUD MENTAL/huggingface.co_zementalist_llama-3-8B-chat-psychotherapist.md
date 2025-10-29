# zementalist/llama-3-8B-chat-psychotherapist · Hugging Face

**URL:** https://huggingface.co/zementalist/llama-3-8B-chat-psychotherapist

---

Hugging Face
Models
Datasets
Spaces
Docs
Pricing
Log In
Sign Up
zementalist
/
llama-3-8B-chat-psychotherapist 
like
29
Text Generation
PEFT
Safetensors
mpingale/mental-health-chat-dataset
Amod/mental_health_counseling_conversations
heliosbrahma/mental_health_chatbot_dataset
llama
SFT
PEFT
Mental Health
Psychotherapy
Fine-tuning
Text Generation
Chatbot
conversational
4-bit precision
bitsandbytes
License:
mit
Model card
Files
xet
Community
1
Use this model
Model Card for Model ID

A fine-tuned Llama-3-8B-instruct trained to provide initial support and guidance in mental health by leveraging the power of large language models (LLMs). It's a fine-tuned version of the LLaMA 3 model specifically trained on mental health counseling conversations.

Model Details

Llama-3-8B-chat-psychotherapist

Provides active listening: The model is trained to follow conversation flows and respond attentively to user expressions. Offers empathetic support: The model's responses are designed to be supportive and understanding, fostering a safe space for users to share their concerns. Guides users towards self-reflection: The model can ask open-ended questions and prompt users to explore their thoughts and feelings. Offers resources and information: Depending on the conversation, the model can provide users with relevant mental health resources and information. Important to Note:

This model is intended for initial support and guidance, not a replacement for professional mental health care. It's crucial to emphasize that users should seek professional help if needed. The model is still under development, and its responses may require human oversight for accuracy and safety.

Further Considerations: You can specify the type of mental health conversations the model is trained on (e.g., anxiety, depression, general well-being). Briefly mention the dataset used for fine-tuning to showcase the model's training grounds. If applicable, mention any limitations of the model, such as inability to diagnose or provide specific treatment plans.

How to Get Started with the Model

Use the code below to get started with the model.

Read model
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM

model_id = "zementalist/llama-3-8B-chat-psychotherapist"
config = PeftConfig.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path)
model = PeftModel.from_pretrained(model, model_id)

Inference

question = "I feel like I don't exist and my body is not my own, I'm sombody else observing me, what causes these ideas?"

messages = [
    {"role": "system", "content": "Answer the following inquiry:"},
    {"role": "user", "content": question}
]

input_ids = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)


terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = model.generate(
    input_ids,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.01
)
response = outputs[0][input_ids.shape[-1]:]
output = tokenizer.decode(response, skip_special_tokens=True)


print(output)

Training Details
Training Data
Amod/mental_health_counseling_conversations
mpingale/mental-health-chat-dataset
heliosbrahma/mental_health_chatbot_dataset
Training Hyperparameters
epochs: 2
learning rate: 6e-5
learning rate scheduler type: constant
Warmup ratio: 0.03
optimizer: paged_adamw_32bit
weight_decay: 0.001
fp16: True
Evaluation
Step	Training Loss
100	2.637700
200	2.350900
300	2.234500
400	2.230800
500	2.194900
600	2.041100
700	2.033800
800	1.988600
900	1.898900
1000	1.823600
1100	1.943700
1200	1.789900
1300	1.840700
1400	1.760900
1500	1.718400
1600	1.725600
1700	1.717600
1800	1.628200
1900	1.693300
2000	1.535600
2100	1.630100
2200	1.592300
2300	1.628400
2400	1.462500
2500	1.504500
2600	1.517500
2700	1.375100
2800	1.452800
2900	1.527200
3000	1.418600
3100	1.437700
3200	1.247900
3300	1.134900
3400	1.283800
3500	1.378600
3600	1.114600
3700	1.300900
3800	1.225700
3900	1.190000
4000	1.260200
4100	1.053300
4200	1.173000
4300	1.275900
4400	1.079800
4500	1.121100
4600	1.043100
4700	1.121000
4800	1.087200
4900	1.102400
5000	1.126100
5100	1.182200
5200	1.156500
5300	0.979700
5400	1.145300
5500	1.018100
5600	1.070500
5700	0.954900
5800	1.074200
5900	1.022800
6000	1.037700
6100	0.913400
6200	0.929500
Inference example
Question: I feel like I don't exist and my body is not my own, like if I'm sombody else observin me, what could be this disorder?
Answer: You're describing a phenomenon called depersonalization. It's a common symptom of anxiety disorders, post-traumatic stress disorder (PTSD), and other mental health conditions.
Depersonalization can make you feel like you're observing yourself from the outside, like you're watching a movie or reading a book about yourself. You might also feel like you're not in control of your body or that you're just a puppet.
This feeling can be very distressing and can make you wonder if you're even alive. It's a very disorienting and unsettling experience.
If you're experiencing depersonalization, it's important to seek help from a mental health professional. They can help you identify the underlying causes of your feelings and develop coping strategies to manage them.

Question: I'm always confused when making decisions, I cannot choose one option, I must have only one option so I can make a decision, what are the causes of being indecisive?
Answer: Indecisiveness is a common phenomenon that many people experience. It's not a mental health condition, but it can be frustrating and time-consuming. Here are some possible causes of indecisiveness:
Fear of making the wrong decision: Sometimes, people are afraid of making the wrong choice, which can lead to indecisiveness. This fear can be due to various factors such as fear of failure, fear of rejection, or fear of the unknown.
Lack of clear goals: When people don't have clear goals, they can be indecisive. This is because they don't know what they want, which can lead to confusion and indecisiveness.
Overthinking: Overthinking can be a major cause of indecisiveness. When people overthink, they can get caught up in their thoughts and be unable to make a decision.
Lack of self-confidence: People who lack self-confidence can be indecisive. This is because they don't believe in themselves and are afraid of making the wrong decision.
Avoidance: Avoiding a decision can be a cause of indecisiveness. When people avoid making a decision, they can be indecisive because they don't know
Developed by: [Zeyad Khalid]
Downloads last month
85
Safetensors
Model size
4.65B params
Tensor type
F32
·
U8

Chat template

Files info

Inference Providers
NEW
Text Generation
This model isn't deployed by any Inference Provider.
🙋
Ask for provider support
Model tree for
zementalist/llama-3-8B-chat-psychotherapist
Merges
5 models
Datasets used to train
zementalist/llama-3-8B-chat-psychotherapist
Amod/mental_health_counseling_conversations
Viewer
•
Updated Aug 8
•
3.51k
•
3.51k
•
430
heliosbrahma/mental_health_chatbot_dataset
Viewer
•
Updated Feb 29, 2024
•
172
•
958
•
89
mpingale/mental-health-chat-dataset
Viewer
•
Updated Nov 5, 2023
•
2.78k
•
78
•
19
Spaces using
zementalist/llama-3-8B-chat-psychotherapist
3
😻
EktaSharma7/zementalist-llama-3-8B-chat-psychotherapist
💬
rsvordz/zementalist-llama-3-8B-chat-psychotherapist
💬
Mob27/zementalist-llama-3-8B-chat-psychotherapist
System theme
TOS
Privacy
About
Jobs
Models
Datasets
Spaces
Pricing
Docs
