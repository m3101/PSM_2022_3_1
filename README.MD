# Repositório do Projeto 1 - Processamento de Sinais Multimídia - Jan. 2023

Vide report [aqui](tex/relatorio.pdf).

Para compilar e construir a aplicação: no diretório-raíz (onde está este arquivo), rode `make`.

> A compilação presume acesso à biblioteca pulse (libpulse & libpulse-simple).
> A execução do código python presume acesso às bibliotecas QT (pyside6), numpy (numpy) e pyaudio (pyaudio).

Para vê-la em ação:

> Esta aplicação presume um ambiente linux com driver PulseAudio de som. A operação correta requer também a aplicação `pavucontrol` para poder selecionar qual stream de audio cada aplicação usará.

* Defina a variável de ambiente `PSM_PIPE` para algum diretório acessível pelo usuário que executará o programa.
> Neste diretório será criado um arquivo de socket UNIX, então cuidado com a localização, para que não sobrescreva algo que já existe lá.
* Abra o host de DSP.
* Configure as fontes de áudio como quiser para cada aplicação usando
    * `pavucontrol`
    * `pactl load-module module-null-sink sink_name=x[n]`
* Abra, em qualquer ordem, as aplicações de interação (`python3 <arquivo>`).