import edge_tts

async def generate_audio(text,outputFilename , isMaleActor):
    # voiceActor = "en-IN-NeerjaNeural"
    voice = "en-IN-PrabhatNeural" if isMaleActor == "male" else "en-IN-NeerjaNeural"
    # Wrap in SSML with prosody for speech rate
    ssml = f"""
    <speak>
        <voice name="{voice}">
            <prosody rate="120%">{text}</prosody>
        </voice>
    </speak>
    """
    communicate = edge_tts.Communicate(text,voice)
    await communicate.save(outputFilename)





