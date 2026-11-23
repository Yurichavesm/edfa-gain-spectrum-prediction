# Databricks: cole este codigo em UMA CELULA de um NOTEBOOK PYTHON NOVO.
# Compatível com Unity Catalog Volumes: ZIP é criado NO DISCO LOCAL.
from pathlib import Path
from tempfile import TemporaryDirectory
import zipfile

ROOT = Path('/Volumes/workspace/default/ofc2026')
RESULT = ROOT / 'resultados/modelagem_espectral_transferencia'
ARQUIVO_SAIDA = ROOT / 'artefatos_reproducao_edfa.zip'

# Somente artefatos associados ao pipeline MLP principal.
ESSENCIAIS = [
    RESULT/'indices_cosmos_train.npy',
    RESULT/'indices_cosmos_val.npy',
    RESULT/'features_challenge_mlp_v2.npy',
    RESULT/'mlp_v2_pretrained.pt',
    RESULT/'mlp_v2_pretrained_extended.pt',
    RESULT/'mlp_v2_pretrained_48ep.pt',
    RESULT/'mlp_v2_48ep_finetuned.pt',
    RESULT/'historico_mlp_v2.csv',
    RESULT/'historico_pretrain_extended.csv',
    RESULT/'historico_pretrain_48ep.csv',
    RESULT/'predicoes_mlp_v2_48ep_testground.csv',
]
OPCIONAIS = [
    RESULT/'folds_challenge.csv',
    RESULT/'avaliacao_cv_mlp_v2_48ep.csv',
    RESULT/'avaliacao_mlp_final.csv',
    RESULT/'manifesto_validacao_final.json',
    RESULT/'manifesto_reproducao_essencial.json',
]

print('Conferindo acessibilidade dos arquivos:')
for p in ESSENCIAIS:
    try:
        print('OK ' if p.is_file() else 'AUSENTE ',p)
    except OSError as e:
        print('ERRO AO CONSULTAR',p,repr(e))

faltantes=[]
for p in ESSENCIAIS:
    try:
        if not p.is_file(): faltantes.append(str(p))
    except OSError as exc:
        raise RuntimeError(f'Nao consegui consultar {p}; confira as permissoes de leitura no Volume: {exc}') from exc
if faltantes:
    raise FileNotFoundError('Essenciais ausentes:\n'+'\n'.join(faltantes))

# A compactação exige seek/reescrita do índice central do ZIP.
# Não fazer zipfile.ZipFile('/Volumes/...') diretamente.
base_temp=Path('/local_disk0/tmp')
if not base_temp.is_dir():
    base_temp=Path('/tmp')

with TemporaryDirectory(prefix='edfa_zip_',dir=str(base_temp)) as tmp:
    zip_local=Path(tmp)/'artefatos_reproducao_edfa.zip'
    with zipfile.ZipFile(zip_local,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for p in ESSENCIAIS+OPCIONAIS:
            if not p.is_file():
                print('Opcional ausente:',p.name)
                continue
            print('Lendo:',p)
            try:
                z.write(p,arcname=str(p.relative_to(ROOT)))
            except Exception as exc:
                raise RuntimeError(f'Falha ao LER ou compactar: {p} ({exc})') from exc
    with zipfile.ZipFile(zip_local) as z:
        ruim=z.testzip()
        if ruim: raise RuntimeError(f'Arquivo danificado dentro do ZIP: {ruim}')
    print('ZIP local completo:',zip_local,'bytes=',zip_local.stat().st_size)
    destino='dbfs:'+str(ARQUIVO_SAIDA)
    origem='file:'+str(zip_local)
    print('Copiando do disco local para:',destino)
    ok=dbutils.fs.cp(origem,destino)
    if not ok: raise RuntimeError('dbutils.fs.cp retornou False. Verifique WRITE VOLUME.')
    print('SUCESSO! No Catalog Explorer, baixe:',ARQUIVO_SAIDA)