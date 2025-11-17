### Auxiliar TTS

Este é um projeto desenvolvido para auxiliar pessoas com deficiêcia visual a consumir conteúdos textuais via audio, feito como projeto de extensão da minha graduação em *Ciência da computação* pela Universidade Positivo Cruzeiro do Sul.

---

### Instalação

Caso o usuário possua uma GPU nvidia e deseje utiliza-la para rodar o algoritmo é necessário a instalação dos softwares *CUDATOOLKIT* e também *CUDNN*. ==(os dois disponíveis nos respectivos links abaixo)==
    
>https://developer.nvidia.com/cuda-downloads
>https://developer.nvidia.com/cudnn

Para o usuário que irá usar a CPU é só iniciar a partir de agora, todo o projeto é feito em *Python* então se não estiver instalado é necessário instalar.==(Link para donwload abaixo, recomendado instalar pelo *install manager* e inserir o python em seu PATH)==

>https://www.python.org/downloads/

Também é necessario fazer o download do projeto no git, pode ser feito direto da pagina [Link da Pagina](https://github.com/Rufcca/Auxiliar_tts) ou também clonando o repositório pelo terminal no linux ou PowerShell se estiver usando windows

>`git clone https://github.com/Rufcca/Auxiliar_tts.git`

Feito a instalação dos componentes básicos, e também o donwload do projeto, agora é hora de criar um ambiente virtual para empacotar o aplicativo e não gerar nenhum conflito com outras partes do sistema.==(Comando de criação deve ser utilizado no terminal se o SisOp. for Linux, se for Windows executar no PowerShell)==

>python -m venv aux_tts
>cd aux_tts

##### Windows
>`.\Scripts\activate.ps1`


##### Linux
>`source /bin/activate`

Agora é necessário instalar as bibliotecas que o projeto utiliza para funcionar, todas estão nomeadas no arquivos *requirements.txt*, então para instala-las basta utilizar o comando()
>`pip install -r requirements.txt`
##### Caso for utilizara a GPU
>`pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu129`

Pronto todos as preparações foram feitas e agora só resta iniciar o programa. Você pode, dentro do terminal do seu SisOp, fazer isso indo até a pasta onde foi feito o donwload do projeto e (com o ambiente virtual criando aux_tts, que pode ser ativado indo até a pasta criada no Local do seu usuário e inserir comando do seu respectivo SisOp) inserir o comando 

>`python main.py`

Na primeira inicialização sera feito o donwload do modelo pela API ==(uma dica valiosa é anotar onde o modelo foi baixado para utilizalo melhor depois, após terminado o donwload o programa faz um print do local onde foi baixado)==, após isso você pode (se desejar) ir no arquivo *config.yaml* e inserir um local onde você poderá inserir os audios de uma vóz que vc deseje que seja copiada e emulada para as suas leituras, só criar a pasta inserir os audios nela e depois iniciar o programa que eles serão convertidos e incorporados ao modelo.

### Utilização

| Comando      | Ação         | 
| -----------: | :--------------: |                           
| ALT + T      | para apenas gerar o audio na pasta do cache | 
| ALT + [      | pagar gerar o audio e reproduzi-lo          |
| ALT + K      | para encerrar o aplicativo                  |

Existe um arquivo de configurações (***config.yaml***) onde você encontrara uma lista de opções configuráveis, duas configurações que valem ser explicadas é a opção ***motor*** e também a opção ***local_modelo***, essas servem respectivamente para selecionar se sera utilizado modelo somente, ou se toda a API sera utilizada, a vantagem de usar apenas o modelo é uma melhora pequena no audio gerado, pois é possivel configurar parametros de saida. Só se faz necessario encontrar onde a API fez o download, se anotado como na dica dada apenas ***colar*** o diretorio no ***local_modelo*** e *configurar* ***motor*** como ***"api"***.
