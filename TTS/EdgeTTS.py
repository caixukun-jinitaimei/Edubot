import asyncio
import requests
import json
import os
from edge_tts import Communicate, SubMaker
from io import TextIOWrapper
from typing import Any, TextIO, Union
import sys
sys.path.append('../Linly-Talker')
sys.path.append('../Linly-Talker-main')
from src import cost_time
from src.cost_time import calculate_time    
os.environ["GRADIO_TEMP_DIR"]= './temp'

"""
Constants for the Edge TTS project.
"""

TRUSTED_CLIENT_TOKEN = "6A5AA1D4EAFF4E9FB37E23D68491D6F4"

WSS_URL = (
    "wss://speech.platform.bing.com/consumer/speech/synthesize/"
    + "readaloud/edge/v1?TrustedClientToken="
    + TRUSTED_CLIENT_TOKEN
)

VOICE_LIST = (
    "https://speech.platform.bing.com/consumer/speech/synthesize/"
    + "readaloud/voices/list?trustedclienttoken="
    + TRUSTED_CLIENT_TOKEN
)

def list_voices_fn(proxy=None):
    """
    List all available voices and their attributes.

    This pulls data from the URL used by Microsoft Edge to return a list of
    all available voices.

    Returns:
        dict: A dictionary of voice attributes.
    """
    # ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    headers = {
        "Authority": "speech.platform.bing.com",
        "Sec-CH-UA": '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        "Sec-CH-UA-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41",
        "Accept": "*/*",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(VOICE_LIST, headers=headers)
    data = json.loads(response.text)
    return data


class EdgeTTS:
    def __init__(self, list_voices = False, proxy = None) -> None:
        try:
            voices = list_voices_fn(proxy=proxy)
            self.SUPPORTED_VOICE = [item['ShortName'] for item in voices]
            self.SUPPORTED_VOICE.sort(reverse=True)
            # print(self.SUPPORTED_VOICE)
            if list_voices:
                print(", ".join(self.SUPPORTED_VOICE))
        except:
            self.SUPPORTED_VOICE = ['zu-ZA-ThembaNeural', 'zu-ZA-ThandoNeural',  'zh-TW-YunJheNeural', 'zh-TW-HsiaoYuNeural', 'zh-TW-HsiaoChenNeural', 'zh-HK-WanLungNeural', 
                                    'zh-HK-HiuMaanNeural', 'zh-HK-HiuGaaiNeural', 'zh-CN-shaanxi-XiaoniNeural', 'zh-CN-liaoning-XiaobeiNeural', 
                                    'zh-CN-YunyangNeural', 'zh-CN-YunxiaNeural', 'zh-CN-YunxiNeural', 'zh-CN-YunjianNeural', 
                                    'zh-CN-XiaoyiNeural', 'zh-CN-XiaoxiaoNeural', 'vi-VN-NamMinhNeural', 'vi-VN-HoaiMyNeural', 
                                    'uz-UZ-SardorNeural', 'uz-UZ-MadinaNeural', 'ur-PK-UzmaNeural', 'ur-PK-AsadNeural', 
                                    'ur-IN-SalmanNeural', 'ur-IN-GulNeural', 'uk-UA-PolinaNeural', 'uk-UA-OstapNeural', 
                                    'tr-TR-EmelNeural', 'tr-TR-AhmetNeural', 'th-TH-PremwadeeNeural', 'th-TH-NiwatNeural', 
                                    'te-IN-ShrutiNeural', 'te-IN-MohanNeural', 'ta-SG-VenbaNeural', 'ta-SG-AnbuNeural', 
                                    'ta-MY-SuryaNeural', 'ta-MY-KaniNeural', 'ta-LK-SaranyaNeural', 'ta-LK-KumarNeural', 
                                    'ta-IN-ValluvarNeural', 'ta-IN-PallaviNeural', 'sw-TZ-RehemaNeural', 'sw-TZ-DaudiNeural', 
                                    'sw-KE-ZuriNeural', 'sw-KE-RafikiNeural', 'sv-SE-SofieNeural', 'sv-SE-MattiasNeural', 
                                    'su-ID-TutiNeural', 'su-ID-JajangNeural', 'sr-RS-SophieNeural', 'sr-RS-NicholasNeural', 'sq-AL-IlirNeural', 'sq-AL-AnilaNeural', 
                                    'so-SO-UbaxNeural', 'so-SO-MuuseNeural', 'sl-SI-RokNeural', 'sl-SI-PetraNeural', 
                                    'sk-SK-ViktoriaNeural', 'sk-SK-LukasNeural', 'si-LK-ThiliniNeural', 'si-LK-SameeraNeural', 
                                    'ru-RU-SvetlanaNeural', 'ru-RU-DmitryNeural', 'ro-RO-EmilNeural', 'ro-RO-AlinaNeural', 'pt-PT-RaquelNeural', 'pt-PT-DuarteNeural', 'pt-BR-ThalitaNeural', 'pt-BR-FranciscaNeural', 
                                    'pt-BR-AntonioNeural', 'ps-AF-LatifaNeural', 'ps-AF-GulNawazNeural', 'pl-PL-ZofiaNeural', 
                                    'pl-PL-MarekNeural', 'nl-NL-MaartenNeural', 'nl-NL-FennaNeural', 'nl-NL-ColetteNeural', 
                                    'nl-BE-DenaNeural', 'nl-BE-ArnaudNeural', 'ne-NP-SagarNeural', 'ne-NP-HemkalaNeural', 
                                    'nb-NO-PernilleNeural', 'nb-NO-FinnNeural', 'my-MM-ThihaNeural', 'my-MM-NilarNeural', 
                                    'mt-MT-JosephNeural', 'mt-MT-GraceNeural', 'ms-MY-YasminNeural', 'ms-MY-OsmanNeural', 
                                    'mr-IN-ManoharNeural', 'mr-IN-AarohiNeural', 'mn-MN-YesuiNeural', 'mn-MN-BataaNeural', 
                                    'ml-IN-SobhanaNeural', 'ml-IN-MidhunNeural', 'mk-MK-MarijaNeural', 'mk-MK-AleksandarNeural', 
                                    'lv-LV-NilsNeural', 'lv-LV-EveritaNeural', 'lt-LT-OnaNeural', 'lt-LT-LeonasNeural', 'lo-LA-KeomanyNeural', 'lo-LA-ChanthavongNeural', 
                                    'ko-KR-SunHiNeural', 'ko-KR-InJoonNeural', 'ko-KR-HyunsuNeural', 'kn-IN-SapnaNeural', 
                                    'kn-IN-GaganNeural', 'km-KH-SreymomNeural', 'km-KH-PisethNeural', 'kk-KZ-DauletNeural', 
                                    'kk-KZ-AigulNeural', 'ka-GE-GiorgiNeural', 'ka-GE-EkaNeural', 'jv-ID-SitiNeural', 'jv-ID-DimasNeural', 
                                    'ja-JP-NanamiNeural', 'ja-JP-KeitaNeural', 'it-IT-IsabellaNeural', 'it-IT-GiuseppeNeural', 'it-IT-ElsaNeural', 
                                    'it-IT-DiegoNeural', 'is-IS-GunnarNeural', 'is-IS-GudrunNeural', 'id-ID-GadisNeural', 'id-ID-ArdiNeural', 
                                    'hu-HU-TamasNeural', 'hu-HU-NoemiNeural', 'hr-HR-SreckoNeural', 'hr-HR-GabrijelaNeural', 'hi-IN-SwaraNeural', 
                                    'hi-IN-MadhurNeural', 'he-IL-HilaNeural', 'he-IL-AvriNeural', 'gu-IN-NiranjanNeural', 'gu-IN-DhwaniNeural', 
                                    'gl-ES-SabelaNeural', 'gl-ES-RoiNeural', 'ga-IE-OrlaNeural', 'ga-IE-ColmNeural', 'fr-FR-VivienneMultilingualNeural', 
                                    'fr-FR-RemyMultilingualNeural', 'fr-FR-HenriNeural', 'fr-FR-EloiseNeural', 'fr-FR-DeniseNeural', 'fr-CH-FabriceNeural', 
                                    'fr-CH-ArianeNeural', 'fr-CA-ThierryNeural', 'fr-CA-SylvieNeural', 'fr-CA-JeanNeural', 'fr-CA-AntoineNeural', 
                                    'fr-BE-GerardNeural', 'fr-BE-CharlineNeural', 'fil-PH-BlessicaNeural', 'fil-PH-AngeloNeural', 'fi-FI-NooraNeural', 
                                    'fi-FI-HarriNeural', 'fa-IR-FaridNeural', 'fa-IR-DilaraNeural', 'et-EE-KertNeural', 'et-EE-AnuNeural', 
                                    'es-VE-SebastianNeural', 'es-VE-PaolaNeural', 'es-UY-ValentinaNeural', 'es-UY-MateoNeural', 'es-US-PalomaNeural', 
                                    'es-US-AlonsoNeural', 'es-SV-RodrigoNeural', 'es-SV-LorenaNeural', 'es-PY-TaniaNeural', 'es-PY-MarioNeural', 
                                    'es-PR-VictorNeural', 'es-PR-KarinaNeural', 'es-PE-CamilaNeural', 'es-PE-AlexNeural', 'es-PA-RobertoNeural', 
                                    'es-PA-MargaritaNeural', 'es-NI-YolandaNeural', 'es-NI-FedericoNeural', 'es-MX-JorgeNeural', 'es-MX-DaliaNeural', 
                                    'es-HN-KarlaNeural', 'es-HN-CarlosNeural', 'es-GT-MartaNeural', 'es-GT-AndresNeural', 'es-GQ-TeresaNeural', 
                                    'es-GQ-JavierNeural', 'es-ES-XimenaNeural', 'es-ES-ElviraNeural', 'es-ES-AlvaroNeural', 'es-EC-LuisNeural', 
                                    'es-EC-AndreaNeural', 'es-DO-RamonaNeural', 'es-DO-EmilioNeural', 'es-CU-ManuelNeural', 'es-CU-BelkysNeural', 
                                    'es-CR-MariaNeural', 'es-CR-JuanNeural', 'es-CO-SalomeNeural', 'es-CO-GonzaloNeural', 'es-CL-LorenzoNeural', 
                                    'es-CL-CatalinaNeural', 'es-BO-SofiaNeural', 'es-BO-MarceloNeural', 'es-AR-TomasNeural', 'es-AR-ElenaNeural', 
                                    'en-ZA-LukeNeural', 'en-ZA-LeahNeural', 'en-US-SteffanNeural', 'en-US-RogerNeural', 'en-US-MichelleNeural', 
                                    'en-US-JennyNeural', 'en-US-GuyNeural', 'en-US-EricNeural', 'en-US-EmmaNeural', 'en-US-ChristopherNeural', 
                                    'en-US-BrianNeural', 'en-US-AvaNeural', 'en-US-AriaNeural', 'en-US-AndrewNeural', 'en-US-AnaNeural', 
                                    'en-TZ-ImaniNeural', 'en-TZ-ElimuNeural', 'en-SG-WayneNeural', 'en-SG-LunaNeural', 'en-PH-RosaNeural', 
                                    'en-PH-JamesNeural', 'en-NZ-MollyNeural', 'en-NZ-MitchellNeural', 'en-NG-EzinneNeural', 
                                    'en-NG-AbeoNeural', 'en-KE-ChilembaNeural', 'en-KE-AsiliaNeural', 'en-IN-PrabhatNeural', 
                                    'en-IN-NeerjaNeural', 'en-IN-NeerjaExpressiveNeural', 'en-IE-EmilyNeural', 'en-IE-ConnorNeural', 
                                    'en-HK-YanNeural', 'en-HK-SamNeural', 'en-GB-ThomasNeural', 'en-GB-SoniaNeural', 'en-GB-RyanNeural', 
                                    'en-GB-MaisieNeural', 'en-GB-LibbyNeural', 'en-CA-LiamNeural', 'en-CA-ClaraNeural', 'en-AU-WilliamNeural', 
                                    'en-AU-NatashaNeural', 'el-GR-NestorasNeural', 'el-GR-AthinaNeural', 'de-DE-SeraphinaMultilingualNeural', 
                                    'de-DE-KillianNeural', 'de-DE-KatjaNeural', 'de-DE-FlorianMultilingualNeural', 'de-DE-ConradNeural', 
                                    'de-DE-AmalaNeural', 'de-CH-LeniNeural', 'de-CH-JanNeural', 'de-AT-JonasNeural', 'de-AT-IngridNeural', 
                                    'da-DK-JeppeNeural', 'da-DK-ChristelNeural', 'cy-GB-NiaNeural', 'cy-GB-AledNeural', 'cs-CZ-VlastaNeural',
                                    'cs-CZ-AntoninNeural', 'ca-ES-JoanaNeural', 'ca-ES-EnricNeural', 'bs-BA-VesnaNeural', 'bs-BA-GoranNeural', 
                                    'bn-IN-TanishaaNeural', 'bn-IN-BashkarNeural', 'bn-BD-PradeepNeural', 'bn-BD-NabanitaNeural', 'bg-BG-KalinaNeural', 
                                    'bg-BG-BorislavNeural', 'az-AZ-BanuNeural', 'az-AZ-BabekNeural', 'ar-YE-SalehNeural', 'ar-YE-MaryamNeural', 
                                    'ar-TN-ReemNeural', 'ar-TN-HediNeural', 'ar-SY-LaithNeural', 'ar-SY-AmanyNeural', 'ar-SA-ZariyahNeural', 
                                    'ar-SA-HamedNeural', 'ar-QA-MoazNeural', 'ar-QA-AmalNeural', 'ar-OM-AyshaNeural', 'ar-OM-AbdullahNeural', 
                                    'ar-MA-MounaNeural', 'ar-MA-JamalNeural', 'ar-LY-OmarNeural', 'ar-LY-ImanNeural', 'ar-LB-RamiNeural', 'ar-LB-LaylaNeural', 
                                    'ar-KW-NouraNeural', 'ar-KW-FahedNeural', 'ar-JO-TaimNeural', 'ar-JO-SanaNeural', 'ar-IQ-RanaNeural', 'ar-IQ-BasselNeural', 
                                    'ar-EG-ShakirNeural', 'ar-EG-SalmaNeural', 'ar-DZ-IsmaelNeural', 'ar-DZ-AminaNeural', 'ar-BH-LailaNeural', 'ar-BH-AliNeural', 
                                    'ar-AE-HamdanNeural', 'ar-AE-FatimaNeural', 'am-ET-MekdesNeural', 'am-ET-AmehaNeural', 'af-ZA-WillemNeural', 'af-ZA-AdriNeural']

    def preprocess(self, rate, volume, pitch):
        if rate >= 0:
            rate = f'+{rate}%'
        else:
            rate = f'{rate}%'
        if pitch >= 0:
            pitch = f'+{pitch}Hz'
        else:
            pitch = f'{pitch}Hz'
        volume = 100 - volume
        volume = f'-{volume}%'
        return rate, volume, pitch
    @calculate_time
    def predict(self,TEXT, VOICE, RATE, VOLUME, PITCH, OUTPUT_FILE='result.wav', OUTPUT_SUBS='result.vtt', words_in_cue = 8):
        async def amain() -> None:
            """Main function"""
            rate, volume, pitch = self.preprocess(rate = RATE, volume = VOLUME, pitch = PITCH)
            communicate = Communicate(TEXT, VOICE, rate = rate, volume = volume, pitch = pitch)
            subs: SubMaker = SubMaker()
            sub_file: Union[TextIOWrapper, TextIO] = (
                open(OUTPUT_SUBS, "w", encoding="utf-8")
            )
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    # audio_file.write(chunk["data"])
                    pass
                elif chunk["type"] == "WordBoundary":
                    # print((chunk["offset"], chunk["duration"]), chunk["text"])
                    subs.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
            sub_file.write(subs.generate_subs(words_in_cue))
            await communicate.save(OUTPUT_FILE)
            
        
        # loop = asyncio.get_event_loop_policy().get_event_loop()
        # try:
        #     loop.run_until_complete(amain())
        # finally:
        #     loop.close()
        asyncio.run(amain())
        with open(OUTPUT_SUBS, 'r', encoding='utf-8') as file:
            vtt_lines = file.readlines()

        # 去掉每一行文字中的空格
        vtt_lines_without_spaces = [line.replace(" ", "") if "-->" not in line else line for line in vtt_lines]
        # print(vtt_lines_without_spaces)
        with open(OUTPUT_SUBS, 'w', encoding='utf-8') as output_file:
            output_file.writelines(vtt_lines_without_spaces)
        return OUTPUT_FILE, OUTPUT_SUBS

def test():
    tts = EdgeTTS(list_voices=True)
    TEXT = '''近日，苹果公司起诉高通公司，状告其未按照相关合约进行合作，高通方面尚未回应。这句话中“其”指的是谁？'''
    VOICE = "zh-CN-XiaoxiaoNeural"
    OUTPUT_FILE, OUTPUT_SUBS = "tts.wav", "tts.vtt"
    audio_file, sub_file = tts.predict(TEXT, VOICE, 0, 0, 0, OUTPUT_FILE, OUTPUT_SUBS)
    print("Audio file written to", audio_file, "and subtitle file written to", sub_file)

if __name__ == "__main__":
    test()