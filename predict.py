# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
PanGu predict run
"""
import os

import numpy as np

import mindspore.common.dtype as mstype
from mindspore import context, Tensor
from mindspore import export
from mindspore.context import ParallelMode
from mindspore.parallel import set_algo_parameters
from mindspore.parallel._cost_model_context import _set_multi_subgraphs
from mindspore.train.model import Model
from mindspore.train.serialization import load_distributed_checkpoint
#from src.serialization import load_distributed_checkpoint
from src.pangu_alpha import PanguAlpha, EvalNet
from src.pangu_alpha_config import PANGUALPHAConfig, set_parse
from src.utils import get_args

import time
from mindspore.train.serialization import load_checkpoint

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

def load_model(args_opt):
    """
     The main function for load model
    """
    # Set execution mode
    context.set_context(save_graphs=False,
                        mode=context.GRAPH_MODE,
                        device_target=args_opt.device_target)
    context.set_context(max_device_memory="30GB")
    

    device_num = 1
    context.reset_auto_parallel_context()
    context.set_auto_parallel_context(
        strategy_ckpt_load_file=args_opt.strategy_load_ckpt_path)

    use_past = (args_opt.use_past == "true")
    if args_opt.export:
        use_past = True
    # Set model property
    model_parallel_num = args_opt.op_level_model_parallel_num
    data_parallel_num = int(device_num / model_parallel_num)
    per_batch_size = args_opt.per_batch_size
    batch_size = per_batch_size * data_parallel_num
    # Now only support single batch_size for predict
    if args_opt.run_type == "predict":
        batch_size = 1
    config = PANGUALPHAConfig(
        data_parallel_num=data_parallel_num,
        model_parallel_num=model_parallel_num,
        batch_size=batch_size,
        seq_length=args_opt.seq_length,
        vocab_size=args_opt.vocab_size,
        embedding_size=args_opt.embedding_size,
        num_layers=args_opt.num_layers,
        num_heads=args_opt.num_heads,
        expand_ratio=4,
        post_layernorm_residual=False,
        dropout_rate=0.0,
        compute_dtype=mstype.float16,
        use_past=use_past,
        stage_num=args_opt.stage_num,
        micro_size=args_opt.micro_size,
        eod_reset=False,
        word_emb_dp=True,
        load_ckpt_path=None,#args_opt.load_ckpt_local_path,
        param_init_type=mstype.float32 if args_opt.param_init_type == 'fp32' else mstype.float16)
    # print("===config is: ", config, flush=True)
    # print("=====args_opt is: ", args_opt, flush=True)

    ckpt_name = args_opt.load_ckpt_name
    # Define network
    pangu_alpha = PanguAlpha(config)
    eval_net = EvalNet(pangu_alpha)
    eval_net.set_train(False)
    model_predict = Model(eval_net)
    # Compile network and obtain tensor layout for loading ckpt
    inputs_np = Tensor(np.ones(shape=(config.batch_size, config.seq_length)), mstype.int32)
    current_index = Tensor(np.array([0]), mstype.int32)

    if args_opt.distribute == "false":
        predict_layout = None
    elif config.use_past:
        batch_valid_length = Tensor(np.array([0]), mstype.int32)
        init_true = Tensor([True], mstype.bool_)
        init_false = Tensor([False], mstype.bool_)
        inputs_np_1 = Tensor(np.ones(shape=(config.batch_size, 1)), mstype.int32)
        model_predict.predict_network.add_flags_recursive(is_first_iteration=True)
        predict_layout = model_predict.infer_predict_layout(inputs_np, current_index, init_false, batch_valid_length)
        model_predict.predict_network.add_flags_recursive(is_first_iteration=False)
        _ = model_predict.infer_predict_layout(inputs_np_1, current_index, init_true, batch_valid_length)
    else:
        predict_layout = model_predict.infer_predict_layout(inputs_np, current_index)
    ##------------------------------------------------------------------------------------------------------
    print("======start load checkpoint", flush=True)
    
    local_ckpt_path = args_opt.load_ckpt_path + args_opt.load_ckpt_name
    load_checkpoint(local_ckpt_path, eval_net)
    print("================load param ok=================", flush=True)

    return model_predict, config

def run_predict(model_predict, config, args_opt, src_langs, tag_langs,src_txt):
    """run predict"""
    from tokenizer.tokenizer_spm import SpmTokenizer
    from src.generate import generate, generate_increment
    from tokenizer.tokenizer_spm import langs_ID, translate_ID
    import jieba
    
    # Define tokenizer
    vocab_file = args_opt.tokenizer_path + 'spm.128k.model.1'
    tokenizer = SpmTokenizer(vocab_file)

            
            
    # inference mode
    generate_func = generate_increment if config.use_past else generate
        
    try:  
        tokenized_src_langs = tokenizer.tokenize(''.join(jieba.cut(''+src_txt)))
        src_id = tokenizer.convert_tokens_to_ids(tokenized_src_langs)
        # Tokenize input sentence to ids 

        src_trans2_tag_input = [langs_ID[src_langs], langs_ID[src_langs], langs_ID[src_langs]] +\
                                src_id + \
                                [translate_ID, translate_ID, translate_ID] + \
                                [langs_ID[tag_langs], langs_ID[tag_langs], langs_ID[tag_langs]]

        # Call inference
        
        src2tag_output_ids = generate_func(model_predict, np.array([src_trans2_tag_input]), args_opt).tolist()
        # Decode output ids to sentence
        src_output = tokenizer.convert_ids_to_tokens(src2tag_output_ids[len(src_trans2_tag_input):])
                        
        return src_output
    except Exception as error:
        return "error:"+str(error)
    
def main():
    """Main process"""
    opt = get_args(True)
    set_parse(opt)
    model_predict, config = load_model(opt)
    print("model učitan")
    prediction = run_predict(model_predict, config, opt, 'en', 'sr', "test")
    print("inicijalizovano")
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
            src_output=run_predict(model_predict, config, opt, src_langs, tag_langs,src_txt)
            print("\nPrevod: " + src_output + "\n")
    except Exception as error:
        print("\nerror:"+error)
if __name__ == "__main__":
    main()
