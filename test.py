"""run predict"""
from tokenizer.tokenizer_spm import SpmTokenizer
from src.generate import generate, generate_increment
from tokenizer.tokenizer_spm import langs_ID, translate_ID
import jieba
D.init()
rank = D.get_rank()

# Define tokenizer
vocab_file = 'tokenizer/spm.128k.model.1'
tokenizer = SpmTokenizer(vocab_file)
EOT = tokenizer.eot_id
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