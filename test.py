"""run predict"""
from tokenizer.tokenizer_spm import SpmTokenizer

from tokenizer.tokenizer_spm import langs_ID, translate_ID
import jieba



# Define tokenizer
vocab_file = 'tokenizer/spm.128k.model.1'
tokenizer = SpmTokenizer(vocab_file)
EOT = tokenizer.eot_id


i="""У дисертацији је представљена нова метода за аутоматско подешавање ПИД (пропорционално-интегрално-диференцијалног) регулатора заснована на експерт-ском знању имплементираном у расплинути (фази) систем закључивања. Предложена метода итеративно покушава да побољша перформансе система у затвореној спрези. Као мере перформанси предложена метода користи карактеристике одскочног одзива (време успона, прескок и време смирења). Параметри ПИД регула-тора у првој итерацији могу се израчунати на основу једноставног експеримента у отвореној спрези или је могуће користити постојеће параметре. У свакој узастопној итерацији се врши прорачун карактеристика одскочног одзива. Релативне промене изражене у процентима вредности у првој итерацији се затим израчунавају и претва-рају у лингвистичке вредности. Користећи базу од 29 правила, фази експертски систем израчунава фази вредности које се користе након дефaзификације као фактори мно-жења за тренутне ПИД параметре. Да би се постигао баланс између агресивног и ро-бусног одзива у затвореној спрези, као и између споријег и бржег, фази експертски систем може да ради у три различита режима рада: за убрзавање система, за смањење прескока и за уравнотежено смањење времена успона и прескока.  Верификација рачунарским симулацијама је извршена коришћењем широког спектра различитих модела процеса који се најчешће налазе у проблемима аутомати-зације стамбено-пословних објеката. Како би се извршила верификација у реалним експерименталним условима пре-дложена метода је имплементирана на реалном контролеру који се обично користи у аутоматизацији стамбено-пословних објеката. Верификација је извршена на експери-менталној HIL (Hardware-in-loop) поставци у оквиру које је на посебном контролеру реализован модел топлотне подстанице система даљинског грејања који се извршава у реалном времену. Кључне речи: ПИД, расплинута (фази) логика, експертско знање, аутоматско по-дешавање параметара, стамбено-пословни објекти, модел у реалном времену"""

o=tokenizer.tokenize(''.join(jieba.cut(i)))
len(o)




from src.generate import generate, generate_increment
D.init()
rank = D.get_rank()



# inference mode
generate_func = generate_increment if config.use_past else generate
langs = ['vi', 'ko', 'en', 'nl', 
            'de', 'ms', 'id', 'tl', 
            'mn', 'my', 'th', 'lo', 
            'km', 'lt', 'et', 'lv', 
            'hu', 'pl', 'cs', 'sk', 
            'sl', 'hr', 'bs', 'sr',
            'bg', 'mk', 'ru', 'uk', 
            'be', 'el', 'ka', 'hy', 
            'ro', 'fr', 'es', 'pt',
            'fa', 'he', 'ar', 'ps', 
            'tr', 'kk', 'uz', 
            'az', 'hi', 'ta', 
            'ur', 'bn', 'ne', 'zh']


try:
    while True:
        while True:
            src_langs=input("Unesite ulazni jezik: ")
            if src_langs=="!quit":
                raise Exception("End")
            if src_langs in langs:
                break
        while True:
            tag_langs=input("Unesite izlazni jezik: ")
            if tag_langs=="!quit":
                raise Exception("End")
            if tag_langs in langs:
                break
        src_txt=input("Unesite text: ")
        if src_txt=="!quit":
            raise Exception("End")
        
        tokenized_src_langs = tokenizer.tokenize(''.join(jieba.cut(''+src_txt)))
        src_id = tokenizer.convert_tokens_to_ids(tokenized_src_langs)
        # Tokenize input sentence to ids 

        src_trans2_tag_input = [langs_ID[src_langs], langs_ID[src_langs], langs_ID[src_langs]] +\
                                src_id + \
                                [translate_ID, translate_ID, translate_ID] + \
                                [langs_ID[tag_langs], langs_ID[tag_langs], langs_ID[tag_langs]]

        
except Exception as error:
    print(" error, continue...", error)  