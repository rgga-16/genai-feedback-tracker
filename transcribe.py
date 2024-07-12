"""
Code borrowed from: https://github.com/MahmoudAshraf97/whisper-diarization/blob/main/Whisper_Transcription_%2B_NeMo_Diarization.ipynb
"""

import os
import wget
from omegaconf import OmegaConf
import json
import shutil
from faster_whisper import WhisperModel
import whisperx
import torch
from pydub import AudioSegment
from nemo.collections.asr.models.msdd_models import NeuralDiarizer
from deepmultilingualpunctuation import PunctuationModel
import re
import logging
import nltk
from whisperx.alignment import DEFAULT_ALIGN_MODELS_HF, DEFAULT_ALIGN_MODELS_TORCH
from whisperx.utils import LANGUAGES, TO_LANGUAGE_CODE

punct_model_langs = [
    "en",
    "fr",
    "de",
    "es",
    "it",
    "nl",
    "pt",
    "bg",
    "pl",
    "cs",
    "sk",
    "sl",
]
wav2vec2_langs = list(DEFAULT_ALIGN_MODELS_TORCH.keys()) + list(
    DEFAULT_ALIGN_MODELS_HF.keys()
)

whisper_langs = sorted(LANGUAGES.keys()) + sorted(
    [k.title() for k in TO_LANGUAGE_CODE.keys()]
)


def create_config(output_dir):
    DOMAIN_TYPE = "telephonic"  # Can be meeting, telephonic, or general based on domain type of the audio file
    CONFIG_FILE_NAME = f"diar_infer_{DOMAIN_TYPE}.yaml"
    CONFIG_URL = f"https://raw.githubusercontent.com/NVIDIA/NeMo/main/examples/speaker_tasks/diarization/conf/inference/{CONFIG_FILE_NAME}"
    MODEL_CONFIG = os.path.join(output_dir, CONFIG_FILE_NAME)
    if not os.path.exists(MODEL_CONFIG):
        MODEL_CONFIG = wget.download(CONFIG_URL, output_dir)

    config = OmegaConf.load(MODEL_CONFIG)

    data_dir = os.path.join(output_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    meta = {
        "audio_filepath": os.path.join(output_dir, "mono_file.wav"),
        "offset": 0,
        "duration": None,
        "label": "infer",
        "text": "-",
        "rttm_filepath": None,
        "uem_filepath": None,
    }
    with open(os.path.join(data_dir, "input_manifest.json"), "w") as fp:
        json.dump(meta, fp)
        fp.write("\n")

    pretrained_vad = "vad_multilingual_marblenet"
    pretrained_speaker_model = "titanet_large"
    config.num_workers = 0  # Workaround for multiprocessing hanging with ipython issue
    config.diarizer.manifest_filepath = os.path.join(data_dir, "input_manifest.json")
    config.diarizer.out_dir = (
        output_dir  # Directory to store intermediate files and prediction outputs
    )

    config.diarizer.speaker_embeddings.model_path = pretrained_speaker_model
    config.diarizer.oracle_vad = (
        False  # compute VAD provided with model_path to vad config
    )
    config.diarizer.clustering.parameters.oracle_num_speakers = False

    # Here, we use our in-house pretrained NeMo VAD model
    config.diarizer.vad.model_path = pretrained_vad
    config.diarizer.vad.parameters.onset = 0.8
    config.diarizer.vad.parameters.offset = 0.6
    config.diarizer.vad.parameters.pad_offset = -0.05
    config.diarizer.msdd_model.model_path = (
        "diar_msdd_telephonic"  # Telephonic speaker diarization model
    )

    return config

def get_word_ts_anchor(s, e, option="start"):
    if option == "end":
        return e
    elif option == "mid":
        return (s + e) / 2
    return s

def get_words_speaker_mapping(wrd_ts, spk_ts, word_anchor_option="start"):
    s, e, sp = spk_ts[0]
    wrd_pos, turn_idx = 0, 0
    wrd_spk_mapping = []
    for wrd_dict in wrd_ts:
        ws, we, wrd = (
            int(wrd_dict["start"] * 1000),
            int(wrd_dict["end"] * 1000),
            wrd_dict["word"],
        )
        wrd_pos = get_word_ts_anchor(ws, we, word_anchor_option)
        while wrd_pos > float(e):
            turn_idx += 1
            turn_idx = min(turn_idx, len(spk_ts) - 1)
            s, e, sp = spk_ts[turn_idx]
            if turn_idx == len(spk_ts) - 1:
                e = get_word_ts_anchor(ws, we, option="end")
        wrd_spk_mapping.append(
            {"word": wrd, "start_time": ws, "end_time": we, "speaker": sp}
        )
    return wrd_spk_mapping

sentence_ending_punctuations = ".?!"

def get_first_word_idx_of_sentence(word_idx, word_list, speaker_list, max_words):
    is_word_sentence_end = (
        lambda x: x >= 0 and word_list[x][-1] in sentence_ending_punctuations
    )
    left_idx = word_idx
    while (
        left_idx > 0
        and word_idx - left_idx < max_words
        and speaker_list[left_idx - 1] == speaker_list[left_idx]
        and not is_word_sentence_end(left_idx - 1)
    ):
        left_idx -= 1

    return left_idx if left_idx == 0 or is_word_sentence_end(left_idx - 1) else -1

def get_last_word_idx_of_sentence(word_idx, word_list, max_words):
    is_word_sentence_end = (
        lambda x: x >= 0 and word_list[x][-1] in sentence_ending_punctuations
    )
    right_idx = word_idx
    while (
        right_idx < len(word_list)
        and right_idx - word_idx < max_words
        and not is_word_sentence_end(right_idx)
    ):
        right_idx += 1

    return (
        right_idx
        if right_idx == len(word_list) - 1 or is_word_sentence_end(right_idx)
        else -1
    )

def get_realigned_ws_mapping_with_punctuation(
    word_speaker_mapping, max_words_in_sentence=50
):
    is_word_sentence_end = (
        lambda x: x >= 0
        and word_speaker_mapping[x]["word"][-1] in sentence_ending_punctuations
    )
    wsp_len = len(word_speaker_mapping)

    words_list, speaker_list = [], []
    for k, line_dict in enumerate(word_speaker_mapping):
        word, speaker = line_dict["word"], line_dict["speaker"]
        words_list.append(word)
        speaker_list.append(speaker)

    k = 0
    while k < len(word_speaker_mapping):
        line_dict = word_speaker_mapping[k]
        if (
            k < wsp_len - 1
            and speaker_list[k] != speaker_list[k + 1]
            and not is_word_sentence_end(k)
        ):
            left_idx = get_first_word_idx_of_sentence(
                k, words_list, speaker_list, max_words_in_sentence
            )
            right_idx = (
                get_last_word_idx_of_sentence(
                    k, words_list, max_words_in_sentence - k + left_idx - 1
                )
                if left_idx > -1
                else -1
            )
            if min(left_idx, right_idx) == -1:
                k += 1
                continue

            spk_labels = speaker_list[left_idx : right_idx + 1]
            mod_speaker = max(set(spk_labels), key=spk_labels.count)
            if spk_labels.count(mod_speaker) < len(spk_labels) // 2:
                k += 1
                continue

            speaker_list[left_idx : right_idx + 1] = [mod_speaker] * (
                right_idx - left_idx + 1
            )
            k = right_idx

        k += 1

    k, realigned_list = 0, []
    while k < len(word_speaker_mapping):
        line_dict = word_speaker_mapping[k].copy()
        line_dict["speaker"] = speaker_list[k]
        realigned_list.append(line_dict)
        k += 1

    return realigned_list

def get_sentences_speaker_mapping(word_speaker_mapping, spk_ts):
    sentence_checker = nltk.tokenize.PunktSentenceTokenizer().text_contains_sentbreak
    s, e, spk = spk_ts[0]
    prev_spk = spk

    snts = []
    snt = {"speaker": f"Speaker {spk}", "start_time": s, "end_time": e, "text": ""}

    for wrd_dict in word_speaker_mapping:
        wrd, spk = wrd_dict["word"], wrd_dict["speaker"]
        s, e = wrd_dict["start_time"], wrd_dict["end_time"]
        if spk != prev_spk or sentence_checker(snt["text"] + " " + wrd):
            snts.append(snt)
            snt = {
                "speaker": f"Speaker {spk}",
                "start_time": s,
                "end_time": e,
                "text": "",
            }
        else:
            snt["end_time"] = e
        snt["text"] += wrd + " "
        prev_spk = spk

    snts.append(snt)
    return snts

def get_speaker_aware_transcript(sentences_speaker_mapping, f):
    previous_speaker = sentences_speaker_mapping[0]["speaker"]
    f.write(f"{previous_speaker}: ")

    for sentence_dict in sentences_speaker_mapping:
        speaker = sentence_dict["speaker"]
        sentence = sentence_dict["text"]

        # If this speaker doesn't match the previous one, start a new paragraph
        if speaker != previous_speaker:
            f.write(f"\n\n{speaker}: ")
            previous_speaker = speaker

        # No matter what, write the current sentence
        f.write(sentence + " ")

def format_timestamp(
    milliseconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
    assert milliseconds >= 0, "non-negative timestamp expected"

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return (
        f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    )

def write_srt(transcript, file):
    """
    Write a transcript to a file in SRT format.

    """
    for i, segment in enumerate(transcript, start=1):
        # write srt lines
        print(
            f"{i}\n"
            f"{format_timestamp(segment['start_time'], always_include_hours=True, decimal_marker=',')} --> "
            f"{format_timestamp(segment['end_time'], always_include_hours=True, decimal_marker=',')}\n"
            f"{segment['speaker']}: {segment['text'].strip().replace('-->', '->')}\n",
            file=file,
            flush=True,
        )

def find_numeral_symbol_tokens(tokenizer):
    numeral_symbol_tokens = [
        -1,
    ]
    for token, token_id in tokenizer.get_vocab().items():
        has_numeral_symbol = any(c in "0123456789%$£" for c in token)
        if has_numeral_symbol:
            numeral_symbol_tokens.append(token_id)
    return numeral_symbol_tokens

def _get_next_start_timestamp(word_timestamps, current_word_index, final_timestamp):
    # if current word is the last word
    if current_word_index == len(word_timestamps) - 1:
        return word_timestamps[current_word_index]["start"]

    next_word_index = current_word_index + 1
    while current_word_index < len(word_timestamps) - 1:
        if word_timestamps[next_word_index].get("start") is None:
            # if next word doesn't have a start timestamp
            # merge it with the current word and delete it
            word_timestamps[current_word_index]["word"] += (
                " " + word_timestamps[next_word_index]["word"]
            )

            word_timestamps[next_word_index]["word"] = None
            next_word_index += 1
            if next_word_index == len(word_timestamps):
                return final_timestamp

        else:
            return word_timestamps[next_word_index]["start"]

def filter_missing_timestamps(
    word_timestamps, initial_timestamp=0, final_timestamp=None
):
    # handle the first and last word
    if word_timestamps[0].get("start") is None:
        word_timestamps[0]["start"] = (
            initial_timestamp if initial_timestamp is not None else 0
        )
        word_timestamps[0]["end"] = _get_next_start_timestamp(
            word_timestamps, 0, final_timestamp
        )

    result = [
        word_timestamps[0],
    ]

    for i, ws in enumerate(word_timestamps[1:], start=1):
        # if ws doesn't have a start and end
        # use the previous end as start and next start as end
        if ws.get("start") is None and ws.get("word") is not None:
            ws["start"] = word_timestamps[i - 1]["end"]
            ws["end"] = _get_next_start_timestamp(word_timestamps, i, final_timestamp)

        if ws["word"] is not None:
            result.append(ws)
    return result

def cleanup(path: str):
    """path could either be relative or absolute."""
    # check if file or directory exists
    if os.path.isfile(path) or os.path.islink(path):
        # remove file
        os.remove(path)
    elif os.path.isdir(path):
        # remove directory and all its content
        shutil.rmtree(path)
    else:
        raise ValueError("Path {} is not a file or dir.".format(path))

def process_language_arg(language: str, model_name: str):
    """
    Process the language argument to make sure it's valid and convert language names to language codes.
    """
    if language is not None:
        language = language.lower()
    if language not in LANGUAGES:
        if language in TO_LANGUAGE_CODE:
            language = TO_LANGUAGE_CODE[language]
        else:
            raise ValueError(f"Unsupported language: {language}")

    if model_name.endswith(".en") and language != "en":
        if language is not None:
            logging.warning(
                f"{model_name} is an English-only model but received '{language}'; using English instead."
            )
        language = "en"
    return language

def transcribe(
    audio_file: str,
    language: str,
    model_name: str,
    compute_dtype: str,
    suppress_numerals: bool,
    device: str,
):
    from faster_whisper import WhisperModel
    # from helpers import find_numeral_symbol_tokens, wav2vec2_langs

    # Faster Whisper non-batched
    # Run on GPU with FP16
    whisper_model = WhisperModel(model_name, device=device, compute_type=compute_dtype)

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    # model = WhisperModel(model_size, device="cpu", compute_type="int8")

    if suppress_numerals:
        numeral_symbol_tokens = find_numeral_symbol_tokens(whisper_model.hf_tokenizer)
    else:
        numeral_symbol_tokens = None

    if language is not None and language in wav2vec2_langs:
        word_timestamps = False
    else:
        word_timestamps = True

    segments, info = whisper_model.transcribe(
        audio_file,
        language=language,
        beam_size=5,
        word_timestamps=word_timestamps,  # TODO: disable this if the language is supported by wav2vec2
        suppress_tokens=numeral_symbol_tokens,
        vad_filter=True,
    )
    whisper_results = []
    for segment in segments:
        whisper_results.append(segment._asdict())
    # clear gpu vram
    del whisper_model
    torch.cuda.empty_cache()
    return whisper_results, language

def transcribe_batched(
    audio_file: str,
    language: str,
    batch_size: int,
    model_name: str,
    compute_dtype: str,
    suppress_numerals: bool,
    device: str,
):
    import whisperx

    # Faster Whisper batched
    whisper_model = whisperx.load_model(
        model_name,
        device,
        compute_type=compute_dtype,
        asr_options={
            "suppress_numerals": suppress_numerals,
            "max_new_tokens": None, 
            "clip_timestamps": None,
            "hallucination_silence_threshold": None
        },
    )
    audio = whisperx.load_audio(audio_file)
    result = whisper_model.transcribe(audio, language=language, batch_size=batch_size)
    del whisper_model
    torch.cuda.empty_cache()
    return result["segments"], result["language"]

def transcription_procedure(audio_path, 
                            enable_stemming=True, 
                            batch_size=8, whisper_model_name="large-v2", 
                            suppress_numerals=True, language="en", 
                            device="cuda" if torch.cuda.is_available() else "cpu", compute_type="float16"):

    # Split the audio into vocals and background music
    if enable_stemming:
        return_code = os.system(f'python3 -m demucs.separate -n htdemucs --two-stems=vocals "{audio_path}" -o "temp_outputs"')

        if return_code != 0:
            logging.warning("Source splitting failed, using original audio file.")
            vocal_target = audio_path
        else:
            vocal_target = os.path.join(
                "temp_outputs",
                "htdemucs",
                os.path.splitext(os.path.basename(audio_path))[0],
                "vocals.wav",
            )
    else:
        vocal_target = audio_path
    
    # Transcribe the vocal target
    if batch_size != 0:
        whisper_results, language = transcribe_batched(
            vocal_target,
            language,
            batch_size,
            whisper_model_name,
            compute_type,
            suppress_numerals,
            device,
        )
    else: 
        whisper_results, language = transcribe(
            vocal_target,
            language,
            whisper_model_name,
            compute_type,
            suppress_numerals,
            device,
        )
    
    # Align the transcribed text with the audio
    if language in wav2vec2_langs: 
        device = "cuda"
        alignment_model, metadata = whisperx.load_align_model(
            language_code=language, device=device
        )
        result_aligned = whisperx.align(
            whisper_results, alignment_model, metadata, vocal_target, device
        )
        word_timestamps = filter_missing_timestamps(
            result_aligned["word_segments"],
            initial_timestamp=whisper_results[0].get("start"),
            final_timestamp=whisper_results[-1].get("end"),
        )

        # clear gpu vram
        del alignment_model
        torch.cuda.empty_cache()
    else: 
        assert batch_size == 0, (  # TODO: add a better check for word timestamps existence
            f"Unsupported language: {language}, use --batch_size to 0"
            " to generate word timestamps using whisper directly and fix this error."
        )
        word_timestamps = []
        for segment in whisper_results:
            for word in segment["words"]:
                word_timestamps.append({"word": word[2], "start": word[0], "end": word[1]})

    # convert audio to mono for NeMo combatibility
    sound = AudioSegment.from_file(vocal_target).set_channels(1)
    ROOT = os.getcwd()
    temp_path = os.path.join(ROOT, "temp_outputs")
    os.makedirs(temp_path, exist_ok=True)
    sound.export(os.path.join(temp_path, "mono_file.wav"), format="wav")

    # Initialize NeMo MSDD diarization model
    msdd_model = NeuralDiarizer(cfg=create_config(temp_path)).to(device)
    msdd_model.diarize()
    del msdd_model
    torch.cuda.empty_cache()

    # Reading timestamps <> Speaker Labels mapping
    speaker_ts = []
    with open(os.path.join(temp_path, "pred_rttms", "mono_file.rttm"), "r") as f:
        lines = f.readlines()
        for line in lines:
            line_list = line.split(" ")
            s = int(float(line_list[5]) * 1000)
            e = s + int(float(line_list[8]) * 1000)
            speaker_ts.append([s, e, int(line_list[11].split("_")[-1])])
    wsm = get_words_speaker_mapping(word_timestamps, speaker_ts, "start")

    if language in punct_model_langs:
        # restoring punctuation in the transcript to help realign the sentences
        punct_model = PunctuationModel(model="kredor/punctuate-all")

        words_list = list(map(lambda x: x["word"], wsm))

        labled_words = punct_model.predict(words_list)

        ending_puncts = ".?!"
        model_puncts = ".,;:!?"

        # We don't want to punctuate U.S.A. with a period. Right?
        is_acronym = lambda x: re.fullmatch(r"\b(?:[a-zA-Z]\.){2,}", x)

        for word_dict, labeled_tuple in zip(wsm, labled_words):
            word = word_dict["word"]
            if (
                word
                and labeled_tuple[1] in ending_puncts
                and (word[-1] not in model_puncts or is_acronym(word))
            ):
                word += labeled_tuple[1]
                if word.endswith(".."):
                    word = word.rstrip(".")
                word_dict["word"] = word
    else:
        logging.warning(f"Punctuation restoration is not available for {language} language. Using the original punctuation.")
    
    wsm = get_realigned_ws_mapping_with_punctuation(wsm)
    ssm = get_sentences_speaker_mapping(wsm, speaker_ts)

    transcript = f"{os.path.splitext(audio_path)[0]}.txt"
    with open(transcript, "w", encoding="utf-8-sig") as f:
        get_speaker_aware_transcript(ssm, f)

    transcript_with_timestamps = f"{os.path.splitext(audio_path)[0]}.srt"
    with open(transcript_with_timestamps, "w", encoding="utf-8-sig") as srt:
        write_srt(ssm, srt)

    cleanup(temp_path)
    return transcript, transcript_with_timestamps

def read_transcript(path):
    with open(path, "r",) as f:
        transcript = f.read()
        return transcript