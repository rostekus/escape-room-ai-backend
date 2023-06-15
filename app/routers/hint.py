import io
import uuid
from os.path import join

import openai
import soundfile as sf
from fastapi import APIRouter

from app.models.hint import ChatResponse
from app.utils.serializers.audio_serializers import AudioGoogleSerializer
from app.utils.tools.generate_link import generate_download_signed_url_v4
from app.utils.tts.google_tts import Text2SpeachGoogleApiModel

router = APIRouter()


riddle_places = {
    1: "Bedroom",
    2: "Kitchen",
    3: "Bedroom -> Kitchen",
    4: "Bedroom",
    5: "Kitchen -> Bedroom",
    6: "Bedroom –-> Kitchen",
    7: "Kitchen –->Bedroom",
    8: "Bedroom",
}

riddle_hints = {
    (
        1,
        1,
    ): "Lately it has been really cold outside, make sure that you are ready to go out… After that make sure to light up a place that usually gives the light by itself.",
    (
        1,
        2,
    ): "Search through the clothes, there may be something interesting hidden inside of them. Use it to look inside of the chimney for clues.",
    (
        1,
        3,
    ): "There is a flashlight hidden inside of one of the pockets of the coat. It needs a battery, but this can be found on the bedside table. Using that, will help you to look inside of the chimney to finish the riddle.",
    (
        2,
        1,
    ): "Oh my gosh, this place is so dirty… maybe you should tidy it up a little bit?",
    (
        2,
        2,
    ): "Look for a proper place for all of this cutlery. Maybe cleaning it up will unlock something?",
    (
        2,
        3,
    ): "Put all of the cutlery in a proper drawer. This should unlock the next drawer underneath, revealing the clue.",
    (
        3,
        1,
    ): "You should have 5 letters. If you have less, maybe search the room one more time or ask your mates from the other room for clues?",
    (
        3,
        2,
    ): "Letters can be found on different herb packs scattered around the house. One was found by your teammates in the bedroom and two were supposed to be found by you. Put the letters in the correct order and fill the bottle with proper liquid.",
    (
        3,
        3,
    ): "Those letters should spell a word that represents liquid found in a human body. There is only 1 bottle on the table with the color the same as this liquid. Fill the empty bottle with this liquid to find the solution.",
    (
        4,
        1,
    ): "In a room, not far ahead,\nDreams arise on a cozy bed.\nBeneath the stars and past the shores,\nAre tales told through whispered roars.\n\nBy the bed, a map laid wide,\nTo distant lands, our dreams collide.\nEach drawn line and sketched out cape,\nIs an invitation to escape.\n\nIn the drawer, tucked away neat,\nAre memories where our journeys meet.\nEach memento and cherished lore,\nSpeak of places we did explore.\n\nPast the map, beyond the doors,\nLie the realms that one adores.\nYet no matter how far you tread,\nRemember the comfort of your own bed.",
    (
        4,
        2,
    ): "Look for 4 hidden buttons in the room. 2 of them are fairly in the open and the rest are more hidden. To get to them you need more than just clues from this room.",
    (
        4,
        3,
    ): "One button is next to the wooden doors. The second one is on the leg of the bed. The next one is hidden in the drawer that can be opened with the key found in the kitchen. Last is in a safe behind the world map. Open it with a code found earlier. You cannot press all the buttons at the same time right now.",
    (
        5,
        1,
    ): "Perhaps there's a connection between the colors and items in the room. The numbers you're seeking might be related to them.",
    (
        5,
        2,
    ): "It seems like you've missed something in the bedroom and kitchen. Try looking at unusual places in the kitchen. Even the kettle could hold a surprise. Once you have all the numbers, try relating them to specific pages in the books.",
    (
        5,
        3,
    ): "Noticed the recipe names on the chalkboard yet? They're not just for cooking. Once you have found the corresponding recipes in the books, rip off the cards from the chalkboard. These will reveal numbers that will help you in your quest to press the right wooden buttons and solve the puzzle.",
    (
        6,
        1,
    ): "The items you found in the box might look random, but they aren't. There's a connection between the hunting rifle, the laser pointer, and the 1929 newspaper article. Consider the year and the event described in the article. Is there any way you could redo the events mentioned in the article?",
    (
        6,
        2,
    ): "Have you noticed that the rifle is too big to move around the rooms? This is intentional. You need to find a way to reflect the laser beam into the bedroom. Look around, is there something reflective that you might use?",
    (
        6,
        3,
    ): "You're on the right track with the mirror! Use it to reflect the laser beam onto the correct location on the map, corresponding to the event from 1929. When you hear a click, you'll know you've done it correctly and the wooden door should open.",
    (
        7,
        1,
    ): "Do you remember the red buttons found before? The answer lies in the collective effort of all players in the bedroom.",
    (
        7,
        2,
    ): "The buttons from the previous riddle all need to be pressed simultaneously. Listen closely for any sounds that might follow. Surprised by the sudden fall of objects? Pay close attention to where they land.",
    (
        7,
        3,
    ): "Pressing all the buttons simultaneously will lead to a startling event - the unexpected opening of the steel doors. You're free to leave, but if you're curious about the true story behind this place, then keep in mind that the chimney isn't just for warmth, it holds another piece of the puzzle. You can try to stay and unravel the mysteries held in the newly discovered camera and documents.",
    (
        8,
        1,
    ): "Noticed anything odd about the video recording on the camera? Pay attention to the details, they are definitely the key! And remember about the lamp.",
    (
        8,
        2,
    ): "Try moving the objects to match the positions in the video. Suddenly in the dark? There's a small lamp in the kitchen that might prove useful now. Don't be fooled if it doesn't seem to produce visible light, it might be illuminating something else.",
    (
        8,
        3,
    ): "Now it's time for the UV lamp to shine, literally. Check the walls for any hidden writings and look around for marked herbs and bottles. These are the ingredients for a mysterious potion. Hurry up! Make the potion, record the process and try to get out before time runs out.",
}


def get_prev_hints(riddle_id, hint_id):
    prev_hints = ""
    for i in range(1, hint_id):
        prev_hints += f"{i} : "
        prev_hints += f"{riddle_hints[riddle_id,i]}\n"

    return prev_hints


text_to_speech = Text2SpeachGoogleApiModel()
text_to_speech.load()


def generate_prompt(riddle_place, prev_hint, hint):
    return """You play role in escape room game. You are in locked the saperate room but
you have book with hints how to get out. Your role is to help your team to get out of the room but you do that unwillingly.

Background Story:
Your arrival to the town has created a real flurry, every one of the locals wanted to see you.
Some with impression, some with hopes of their fears disappearing once and for all. 
You have decided to stay in a small motel by the main road.
After unpacking all of your stuff, you decided to go to sleep, since the next day was supposed to be exhausting: looking for clues, speaking with witnesses etc.
Only if you would have known. 
Next day miraculously all of you woke up in a strange place. 
It was a small wooden hut consisting of 2 rooms, between which you were split in half.

Place where team shoul be: {}

Given hints: {}

Hint to be given :{}
""".format(
        riddle_place.capitalize(), prev_hint.capitalize(), hint.capitalize()
    )


import os


@router.get("/api/v1/hint/{riddle_id}/{hint_id}")
async def read_user_item(hint_id: int, riddle_id: int) -> ChatResponse:
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    # print((get_prev_hints(riddle_id,hint_id)))
    # print(riddle_hints[(riddle_id, hint_id)])
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": generate_prompt(
                    riddle_places[riddle_id],
                    get_prev_hints(riddle_id, hint_id),
                    riddle_hints[(riddle_id, hint_id)],
                ),
            },
            {
                "role": "user",
                "content": " Write your hint, add a little bit of mistery and fun.",
            },
        ],
    )

    hint_text = response["choices"][0]["message"]["content"]
    audio_buffer = text_to_speech.process(hint_text, {}, {})
    audio, audio_sample_rate = sf.read(io.BytesIO(audio_buffer))
    serializer = AudioGoogleSerializer(audio, audio_sample_rate, "wav", "/tmp")
    audio_filename = join("audio", str(uuid.uuid4()))
    with serializer:
        serializer.serialize(
            "audio-escape-room",
            audio_filename,
        )
    url = generate_download_signed_url_v4("audio-escape-room", audio_filename + ".wav")

    return ChatResponse(
        audioUrl=url, text=hint_text, aiText=hint_text
    )
