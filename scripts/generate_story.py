import random
import os

def load(file):
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip()]

characters = load("stories/characters.txt")
lessons = load("stories/lessons.txt")
actions = load("stories/actions.txt")
endings = load("stories/endings.txt")

character = random.choice(characters)
lesson = random.choice(lessons)
action = random.choice(actions)
ending = random.choice(endings)

story = f"""
Once upon a time, there was a happy {character}.

One day, the {character} {action}.
During this time, the {character} learned about {lesson}.

{ending}
"""

os.makedirs("output", exist_ok=True)

with open("output/story.txt", "w") as f:
    f.write(story.strip())

print("✅ Story generated successfully")
print(story)
