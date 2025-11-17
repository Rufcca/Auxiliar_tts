from multiprocessing import Process
from pynput.keyboard import *
import os, signal ,sys
import pyperclip
from motor_sonoro import MotorSonoro
import time
import wave
import pyaudio
import yaml

MotorSon = None
pid = os.getpid()
pid_proc_arm = int()
keyboard = Controller()
n_max_audios = int()
wf = None
pasta_cache = "cache_audios"
configs = dict()
sist_oper = sys.platform

def carrega_config(caminho_arq = "config.yaml"):
    configuracoes = None
    with open(caminho_arq, "r") as configs:
        try:
            configuracoes = yaml.safe_load(configs)
        except yaml.YAMLError as exc:
            print(exc)
    return configuracoes


#controla o fluxo de armazenamento dos audios em cache
def observador_armazenamento(n_max_audios):
    while(1):
        audios_do_cache = os.listdir(pasta_cache)
        audios_do_cache = [os.path.join(pasta_cache , audio) for audio in audios_do_cache]
        if (len(audios_do_cache) > 0):

            arquivo_mais_velho = min(audios_do_cache, key=os.path.getctime)
            if sist_oper.startswith("linux"):
                if len(audios_do_cache) / 2 > n_max_audios:
                    os.remove(arquivo_mais_velho)
                    print(arquivo_mais_velho)
            elif sist_oper.startswith("win"):
                if len(audios_do_cache) > n_max_audios:
                    os.remove(arquivo_mais_velho)
                    print(arquivo_mais_velho)
        time.sleep(3)

#encerra o processo e todos seus dependentes
def encerra_processo():
    if sist_oper == "win32":
        os.kill(pid_proc_arm, signal.SIGTERM)
        os.kill(pid, signal.SIGTERM)
    elif sist_oper.startswith('linux'):
        os.killpg(pid, signal.SIGKILL)

# gera um audio no cache com o conteudo do clipboard
def on_activate_transcodificacao():
    texto_a_gerar = pyperclip.paste()
    MotorSon.gera_audio(texto_a_gerar,pasta_cache)

#função que retira o conteúdo da clipboard e alimenta o motor sonoro, para que ele gere um audio e o reproduza no player embarcado
def on_activate_auto_play():
    texto_a_gerar = pyperclip.paste()
    local_audio_gerado = MotorSon.gera_audio(texto_a_gerar,pasta_cache)
    audio_player(local_audio_gerado)

#player de audio embarcado 
def audio_player(local_audio):
    with wave.open(local_audio) as wf:
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)

            return (data, pyaudio.paContinue)
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)
        while stream.is_active():
            time.sleep(0.1)
        stream.close()
        p.terminate()





if __name__ == "__main__":
    #recupera configuracoes
    configs = carrega_config()
    motor = configs["motor"]
    n_max_audios = configs["max_audios_cache"]
    pasta_cache = configs["pasta_cache"]  
    #valida existencia da pasta de cache e a cria se necessario 
    if os.path.isdir(configs["pasta_cache"]):
        pass     
    else:
        os.mkdir(configs["pasta_cache"])
         

    #inicia motor sonoro
    MotorSon = MotorSonoro("tts_models/multilingual/multi-dataset/xtts_v2" , configs["local_modelo"])
    if MotorSon != None:
        print("modulo de TTS carregado")
    else:
        encerra_processo()

    MotorSon.define_local_audios_speaker(configs["local_speaker"])

    if MotorSon.motor == "modelo": 
        MotorSon.gera_speaker_modelo()
    elif MotorSon.motor == "api":
        MotorSon.gera_speaker_api("Belle")



    #inicia manutencao do armazenamento

    processo_armazenamento = Process(target=observador_armazenamento, args=(n_max_audios ,))
    processo_armazenamento.start()
    pid_proc_arm = processo_armazenamento.pid

    #configura hotkeys

    hotkeys_e_funcoes = {
        configs["hotkey-encerramento"]: encerra_processo,
        configs["hotkey-encodificador"]: on_activate_transcodificacao,
        configs["hotkey-encode-play"] : on_activate_auto_play,

    }
    #inicia o observador das hotkeys 
    with GlobalHotKeys(hotkeys_e_funcoes) as observador_hotkeys:
        observador_hotkeys.join()