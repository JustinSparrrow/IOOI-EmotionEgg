import os
import soundfile as sf
import pyaudio
import wave

from .tools.i18n.i18n import I18nAuto
from .inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav

i18n = I18nAuto()

def synthesize(GPT_model_path, SoVITS_model_path, ref_audio_path, ref_text_path, ref_language, target_text_path,
               target_language, output_path):
    # Read reference text
    with open(ref_text_path, 'r', encoding='utf-8') as file:
        ref_text = file.read()

    # Read target text
    with open(target_text_path, 'r', encoding='utf-8') as file:
        target_text = file.read()

    # Change model weights
    change_gpt_weights(gpt_path=GPT_model_path)
    change_sovits_weights(sovits_path=SoVITS_model_path)

    # Synthesize audio
    synthesis_result = get_tts_wav(ref_wav_path=ref_audio_path,
                                   prompt_text=ref_text,
                                   prompt_language=i18n(ref_language),
                                   text=target_text,
                                   text_language=i18n(target_language), top_p=1, temperature=1)

    result_list = list(synthesis_result)

    if result_list:
        last_sampling_rate, last_audio_data = result_list[-1]
        output_wav_path = os.path.join(output_path, "output.wav")
        sf.write(output_wav_path, last_audio_data, last_sampling_rate)
        print(f"Audio saved to {output_wav_path}")

        # Play the generated audio
        play_audio(output_wav_path)


def play_audio(file_path):
    # Open the wave file
    wf = wave.open(file_path, 'rb')

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Open a stream to play the audio
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks and play it
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Close PyAudio
    p.terminate()

    # Close the wave file
    wf.close()


def speak(target_file):
    # 在这里直接指定路径参数
    GPT_model_path = "GPT_SoVITS/models/gpt_weights.pth"
    SoVITS_model_path = "GPT_SoVITS/models/sovits_weights.pth"
    ref_audio_path = "datatest/test.wav"
    ref_text_path = "datatest/test.txt"
    ref_language = "中文"  # 可选值为: "中文", "英文", "日文"
    target_text_path = target_file
    target_language = "中文"  # 可选值为: "中文", "英文", "日文", "中英混合", "日英混合", "多语种混合"
    output_path = "Voice_emotion/output"

    synthesize(GPT_model_path, SoVITS_model_path, ref_audio_path, ref_text_path, ref_language, target_text_path,
               target_language, output_path)