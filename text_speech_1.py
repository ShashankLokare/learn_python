import os
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

# Specify the output directory for the models
output_path = "model"

# Define the model name
model_name = "tts_models/en/vctk/vits"

# Initialize the model manager
model_manager = ModelManager()

# Download the model if not already present
if not os.path.exists(output_path):
    model_manager.download_model(model_name, output_path)

# Load the synthesizer with the pre-trained model
synthesizer = Synthesizer(
    tts_checkpoint=os.path.join(output_path, model_name, "model_file.pth"),
    tts_config_path=os.path.join(output_path, model_name, "config.json"),
    use_cuda=False
)

def synthesize_speech(text, emotion=None):
    """
    Synthesize speech from the input text with optional emotion.
    
    Parameters:
    - text (str): The input text to convert to speech.
    - emotion (str): The emotion to apply (if supported by the model).

    Returns:
    - audio (np.array): The generated audio waveform.
    """
    # Specify speaker and emotion if needed
    speaker = None  # Default speaker
    emotion = emotion if emotion else "neutral"  # Default to neutral if not specified

    # Generate audio
    audio = synthesizer.tts(text, speaker_name=speaker, style_wav=emotion)

    # Save the audio to a file
    synthesizer.save_wav(audio, "output.wav")
    print("Audio generated and saved as output.wav")

# Example usage
text_input = "Hello, how are you feeling today?"
emotion_input = "happy"  # Change this to 'angry', 'sad', 'surprised', etc.

synthesize_speech(text_input, emotion_input)