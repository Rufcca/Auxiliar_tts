import os ,sys ,time
import torch
import torchaudio
import soundfile as sf

sist_oper = sys.platform
if sist_oper.startswith("linux"):
    from pydub import AudioSegment
    
class MotorSonoro:
    def __init__(self, modelo_tts = "" , local_do_modelo = ""):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.motor = "modelo" #["api" , "modelo"]

        
        
        if self.motor == "api":
            from TTS.api import TTS
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            self.speakers = [ speaker.lower() for speaker in self.tts.speakers ]
 
        elif self.motor == "modelo":
            from TTS.tts.configs.xtts_config import XttsConfig
            from TTS.tts.models.xtts import Xtts
            config = XttsConfig()
            config.load_json(f"{local_do_modelo}config.json")
            self.model = Xtts.init_from_config(config)
            self.model.load_checkpoint(config, checkpoint_dir=local_do_modelo, use_deepspeed=False)

            if device == "cpu":
                self.model.cpu()
            elif device == "cuda":
                self.model.cuda()

        if device == "cpu":
            print(f"{self.motor} Iniciado na CPU")
        elif device == "cuda":
            print(f"{self.motor} Iniciado na GPU")
            
        self.local_pasta_audios_speaker = ""
        self.local_audio_tratamento = ""
        self.speaker_gerador = "Gilberto Mathias"
        self.speaker_a_gerar  = "Customizado"
        

    def retorna_speakers(self):
        return self.tts.speakers

    def retorna_audios_pasta(self):
        audios_pasta = os.listdir(self.local_pasta_audios_speaker)
        return audios_pasta

    def retorna_audios_wav_pasta(self):
        audios_pasta = os.listdir(self.local_pasta_audios_speaker)
        audios_wav = [audio_wav for audio_wav in audios_pasta if audio_wav[-4:] == ".wav"]
        return audios_wav

    def define_local_audios_speaker(self, local_audios):
        self.local_pasta_audios_speaker = local_audios

    def converte_wav(self):
        i=0
        audios_pasta = self.retorna_audios_pasta(self.local_pasta_audios_speaker)
        string_audios = ""
        for audio in audios_pasta:
            formato_audio = audio[-4:]
            if formato_audio == '.ogg' or formato_audio == '.mp3':
                string_audios+= audio[:-4]
                caminho_audio = os.path.join(self.local_pasta , audio)
                dados , freq_amostragem = sf.read(caminho_audio)
                caminho_convertido =  os.path.join(self.local_pasta , f"audio_{i}" + ".wav")
                sf.write(caminho_convertido, dados , freq_amostragem)
                i+=1
        print(f"{i} audios convertidos")

    def gera_speaker_api(self):
        speaker_a_gerar_interno = self.speaker_a_gerar

        print(f"Cadastrando {speaker_a_gerar_interno}")
        self.speaker_a_gerar = speaker_a_gerar_interno
        audios_speaker = self.retorna_audios_wav_pasta()
        audios_speaker = [os.path.join(self.local_pasta_audios_speaker , audio) for audio in audios_speaker ]
        if(len(audios_speaker) < 1):        
            self.converte_wav(self.local_pasta_audios_speaker,self.retorna_audios_pasta())
            audios_speaker = self.retorna_audios_wav_pasta()
            
        self.tts.tts_to_file(
        text= "Olá mundo, eu agora, sou uma vóz digital !",
        speaker_wav = audios_speaker,
        speaker = self.speaker_a_gerar,
        language="pt",
        file_path="teste_speaker_gerado.wav" 
        )
        self.speaker_gerador = speaker_a_gerar_interno

    def define_speaker_modelo(self,falante = "Gilberto Mathias"):
        print("Computing speaker latents...")
        self.gpt_cond_latent, self.speaker_embedding = self.model.speaker_manager.speakers[falante].values()

    def gera_speaker_modelo(self,):
        #retorna lista
        audios_speaker = self.retorna_audios_wav_pasta()
        audios_speaker = [os.path.join(self.local_pasta_audios_speaker , audio) for audio in audios_speaker ]
        if(len(audios_speaker) < 1):        
            self.converte_wav(self.local_pasta_audios_speaker,self.retorna_audios_pasta())
            audios_speaker = self.retorna_audios_wav_pasta()
        #gera o falante    
        self.gpt_cond_latent, self.speaker_embedding = self.model.get_conditioning_latents(audio_path=audios_speaker,max_ref_length=120)
    
    def inferencia(self,texto , lingua, local_salvamento):
        #Define speaker padrão Gilberto Mathias caso não haja um customizado 
        if(len(self.local_pasta_audios_speaker) < 1):
            self.define_speaker_modelo()

        out = self.model.inference(
            texto,
            lingua,
            self.gpt_cond_latent,
            self.speaker_embedding,
            temperature=0.45, # Add custom parameters here
            enable_text_splitting=True,
            speed=0.99,
            repetition_penalty = 2.20
        )
        torchaudio.save(local_salvamento, torch.tensor(out["wav"]).unsqueeze(0) , format="wav", sample_rate=24000, encoding="PCM_U")
    
    def gera_audio(self,  texto , local_salvamento = ""):
        
        if sist_oper.startswith("linux"):
            arquivo_saida = os.path.join( local_salvamento +"/" +  f"output{round(time.time_ns() / 100000)}.wav" )
        elif sist_oper.startswith("win"):
            arquivo_saida = os.path.join( local_salvamento + "\\" + f"output{round(time.time_ns() / 100000)}.wav" )

        if(self.motor == "api"):
            self.tts.tts_to_file( texto , speaker = self.speaker_gerador , language = "pt", file_path = arquivo_saida)
        elif(self.motor == "modelo"):
            self.inferencia(texto, "pt",arquivo_saida)

        self.local_audio_tratamento = arquivo_saida
        
        if sist_oper.startswith("linux"):
            self.converte_mp3()

        return arquivo_saida
   
    def converte_mp3(self):
         
        audio_wav = AudioSegment.from_wav(self.local_audio_tratamento)
        nome_audio = self.local_audio_tratamento.split("/")[-1][:-4]
        caminho_pasta_audio = self.local_audio_tratamento.split("/")[:-1]
        print(nome_audio)
        audio_wav.export(os.path.join("/".join(caminho_pasta_audio),nome_audio + ".mp3"), format = "mp3")

if __name__ == "__main__":

    t0 = time.time() 
    motor_son = MotorSonoro("tts_models/multilingual/multi-dataset/xtts_v2", "local\do\modelo") 
    motor_son.define_local_audios_speaker("E:\\audios")
    t1 = time.time()
    print(f"delta :{t1-t0}s")
    motor_son.gera_speaker_modelo()
    quit()

