import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from services.topicGenerationService import get_openai_response
from services.generateAudioService import generate_audio
from services.imageDownloadService import fetch_and_save_first_image
from moviepy.editor import AudioFileClip, concatenate_audioclips,VideoFileClip,CompositeVideoClip,TextClip,ImageClip
import asyncio

# Load environment variables
load_dotenv()



def read_prompt_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


# Example usage
if __name__ == "__main__":
    topic = "What is React JS "
    prompt = read_prompt_from_file("prompt.txt")
    # result = get_openai_response(prompt, topic)
    result = {
    "scene1": {
        "person1": {"text": "What are Design Patterns?", "imageSearchQuery": None},
        "person2": {
            "text": "Design patterns are standard solutions to common problems in software design. They are like templates which can be directly used to solve a particular problem.",
            "imageSearchQuery": "Design Patterns in software engineering",
        },
    },
    "scene2": {
        "person1": {
            "text": "How many types of Design Patterns are there?",
            "imageSearchQuery": None,
        },
        "person2": {
            "text": "There are three types of Design Patterns: Creational, Structural, and Behavioral patterns.",
            "imageSearchQuery": "Types of Design Patterns",
        },
    },
    "scene3": {
        "person1": {
            "text": "Can you explain Creational Design Patterns?",
            "imageSearchQuery": None,
        },
        "person2": {
            "text": "Creational patterns deal with object creation mechanisms. They provide a way to create objects in a flexible manner.",
            "imageSearchQuery": "Creational Design Patterns",
        },
    },
    "scene4": {
        "person1": {
            "text": "How about Structural Design Patterns?",
            "imageSearchQuery": None,
        },
        "person2": {
            "text": "Structural patterns explain how to assemble objects and classes into larger structures, while keeping the structures flexible and efficient.",
            "imageSearchQuery": "Structural Design Patterns",
        },
    },
    "scene5": {
        "person1": {
            "text": "What are Behavioral Design Patterns?",
            "imageSearchQuery": None,
        },
        "person2": {
            "text": "Behavioral patterns deal with algorithms and the assignment of responsibilities between objects.",
            "imageSearchQuery": "Behavioral Design Patterns",
        },
    },
    "scene6": {
        "person1": {
            "text": "Why are Design Patterns important?",
            "imageSearchQuery": None,
        },
        "person2": {
            "text": "Design Patterns promote reusability, improve code readability and efficiency. They provide solutions to common programming issues.",
            "imageSearchQuery": "Importance of Design Patterns",
        },
    },
}

    # print(result)

    BASE_VIDEO_FILE = "base_video.mp4"
    baseVideoFile = VideoFileClip(BASE_VIDEO_FILE)
    text_clips = []
    image_clips = []


    time_elapsed = 0 

    def addTextClips (text , startTime , duration):
        text_clip = TextClip(
            text,
             color = "#97e84a",
             fontsize = 65,
              method = 'caption',
            size = (baseVideoFile.size[0] * 0.8,None),
            font = "Poppins-Bold-Italic",
                stroke_color = "black",
                stroke_width = 3

        )
        text_clip = text_clip.set_start(startTime).set_duration(duration)
        text_clip = text_clip.set_pos('center')
        text_clip = text_clip.margin(top=700 , bottom=20 , left =20 , right=20,opacity=0)
        text_clips.append(text_clip)
    






    for index, (key, value) in enumerate(result.items()):
        scene_name = f"scene_{index}" 


         
        audioPath__person1 = f"audio/{scene_name}_person1.mp3"
        audioPath__person2 = f"audio/{scene_name}_person2.mp3"

       


        image_path =  f"images/{scene_name}.jpg"

        
        # asyncio.run(fetch_and_save_first_image(value.get("person2").get("imageSearchQuery") , image_path)) 



        asyncio.run(generate_audio(value.get("person1").get("text") , audioPath__person1 , "male"))
        asyncio.run(generate_audio(value.get("person2").get("text") , audioPath__person2 , "female"))

        person1_audio_duration = AudioFileClip(audioPath__person1).duration 
        person2_audio_duration = AudioFileClip(audioPath__person2).duration

        audio1_text_startTime = time_elapsed 
        audio2_text_startTime = audio1_text_startTime + person1_audio_duration

        image_start_time = audio2_text_startTime
        image_duration  = person2_audio_duration

        image = (ImageClip(image_path)
         .resize(newsize=(900, 550))            # Set exact width and height
         .set_position(("center", 100))       # Set position
         .set_start(image_start_time)           # Start at 5 seconds
         .set_duration(image_duration))  

        image_clips.append(image)

        addTextClips(value.get("person1").get("text") , audio1_text_startTime , person1_audio_duration)
        addTextClips(value.get("person2").get("text") , audio2_text_startTime , person2_audio_duration)


        time_elapsed = time_elapsed + person1_audio_duration + person2_audio_duration 


    

    

    AUDIO_BASE_PATH = "audio"
    audio_files = sorted([
        os.path.join(AUDIO_BASE_PATH, file)
        for file in os.listdir(AUDIO_BASE_PATH)
        if file.lower().endswith((".mp3")) 
    ])

    FINAL_AUDIO_PATH = "FINAL_AUDIO.mp3"

    # Load all audio clips
    audio_clips = [AudioFileClip(file) for file in audio_files]
    # Concatenate clips
    final_clip = concatenate_audioclips(audio_clips)

    # Export final audio
    final_clip.write_audiofile(FINAL_AUDIO_PATH)






    # writing all text in video 
    final_audio_file = AudioFileClip(FINAL_AUDIO_PATH)
    baseVideoFile = baseVideoFile.set_duration(final_audio_file.duration)
    baseVideoFile = baseVideoFile.set_audio(final_audio_file)
    baseVideoFile = CompositeVideoClip([baseVideoFile ,   *text_clips , *image_clips])
    baseVideoFile.write_videofile("FINAL_OUTPUT.mp4", codec='libx264', audio_codec='aac')

