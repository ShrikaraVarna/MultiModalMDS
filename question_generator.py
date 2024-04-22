# p1 = "The image shows a person engaging in what appears to be an environmental conservation activity, specifically planting young trees in a wetland or mangrove area. The individual is crouched down, with their hands in the mud, placing a sapling into the ground. There are wooden stakes next to each plant, likely used to support the young trees as they grow. The person is wearing a light blue t-shirt, dark shorts, and a black cap, and seems focused on the task at hand. The environment suggests a bright, sunny day with ample sunlight. This activity is often associated with reforestation or wetland restoration efforts."
# p2 = "This image depicts a person engaged in environmental restoration, specifically planting or tending to young trees in a wetland or mangrove area. It's a sunny day and the area looks tranquil, hinting at the restorative work being done. This person is making a positive impact on the ecosystem by participating in what appears to be a reforestation or conservation project, which is vital for maintaining biodiversity and combating climate change effects like coastal erosion."
# p3 = "In this image, we see an individual engaged in an outdoor activity that involves interaction with young plants and soil. The person is squatting by a small sapling, which is supported by a thin stake, and appears to be planting or tending to the sapling in a muddy environment, possibly a wetland or a marsh. The person is wearing a casual blue t-shirt, dark shorts, and blue slip-on shoes, suitable for outdoor work. A cap is worn backwards on the head, and the person seems focused on the task at hand. The background is blurred but seems to be filled with similar young plants, suggesting this could be part of a reforestation effort or an agricultural activity."
# p4 = "The image shows a person engaged in agricultural work. Specifically, they are crouched down and appear to be planting or tending to young plants in a field. The individual is wearing a short-sleeved, light blue shirt, dark shorts, and a black cap, and is working in an environment that looks like a wetland or muddy field with standing water. There are small plants staked with bamboo sticks in the background, suggesting this might be a form of cultivation like a nursery or a specialized crop that requires planting in wet soil, such as rice or mangrove saplings."
# p5 = "In the image, there is a person who is engaged in an agricultural activity. Specifically, they appear to be planting or tending to young plants in an outdoor setting. The individual is squatting near the ground, reaching out with both hands to either plant something in the soil or to care for a young plant that is already in place. There are several small stakes in the ground, which are often used to support young plants as they grow. The environment looks like a cultivated area with moist or muddy soil, suggesting that this might be a form of wetland agriculture or a location that requires irrigation. The person is dressed casually, wearing a T-shirt, shorts, and what seems to be a cap, indicating a warm climate or season."
transcript =  ["So I'm just erasing the clouds off the ocean.", "I probably saw it like a picture of a huge protest, but I would know if that was true or not.", "I just want to reset background.", "So this is not going to do it, so I'm going to use the pen tool.", "Right now, as you can see, the boat is pretty ginormous compared to the print, so we need to make this a bit smaller.", "That they even got another medical examiner due to the results.", "It kind of looks like it's in the water raging.", "In this you definitely want to use a soft brush."]
transcript_together = " ".join([str(item) for item in transcript])
key_frame_description = "This depicts a man merging two images on a canvas sheet. One of the images is that of a storm with dark clouds about to rain while the other image is that of a waterbody, mostly a sea."


frames_from_keytext_duration = "This depicts a man in glass presenting an image. The image presented is that of a storm in a sea with a bubble cloud for text."

import openai
from openai import OpenAI

# get the summary for the concatenated paragraphs
def summarize(paragrph: str):

  p = f"remove redundant information in the paragraph:{paragrph}"
  client = OpenAI(api_key="your key")
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": 'You are a helpful summmary assistant'},
                {"role": "user", "content": p}],
    temperature=0,
    max_tokens=1000
  )
  
  summ = response.choices[0].message.content
  return summ



# generate the question
from openai import OpenAI
def question_generator(question: str):

  p = f"Generate ten questions based on the following text:{question}"
  client = OpenAI(api_key="")
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": 'You are a helpful question generator'},
                {"role": "user", "content": p}],
    temperature=0,
    max_tokens=1000
  )
  
  print(response.choices[0].message.content)

question_generator(key_frame_description + transcript_together)