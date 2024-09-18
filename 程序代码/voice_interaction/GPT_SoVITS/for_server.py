import os
import soundfile as sf
from voice_interaction.tools.i18n.i18n import I18nAuto
from voice_interaction.GPT_SoVITS.inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav

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

        return output_wav_path  # Return the path of the generated audio file


def speak(target_file):
    # In this function, specify the paths
    GPT_model_path = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/GPT_SoVITS/models/gpt_weights.pth"
    SoVITS_model_path = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/GPT_SoVITS/models/sovits_weights.pth"
    ref_audio_path = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/datatest/test.wav"
    ref_text_path = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/datatest/test.txt"
    ref_language = "中文"  # Options: "中文", "英文", "日文"
    target_text_path = target_file
    target_language = "中文"  # Options: "中文", "英文", "日文", "中英混合", "日英混合", "多语种混合"
    output_path = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output"

    return synthesize(GPT_model_path, SoVITS_model_path, ref_audio_path, ref_text_path, ref_language, target_text_path,
                      target_language, output_path)
