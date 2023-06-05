
# IVI Translate

Project based on mPanGu-α-53 from Pengcheng Laboratory.

# Web aplication for demonstration
 Flask in backend and Vue in fronted


# About mPanGu-Alpha-53

mPanGu-α-53 Come from Pengcheng·PanGu-α,Based on the multi-language translation scenario application of the Belt and Road, pre-training + mixed corpus training was conducted on the self-constructed 2TB high-quality multi-language single and dual language corpus set based on "Pengcheng Yunnao 2" 128 card, and 2.6B pre-training multi-language model +2.6B Belt and Road 53 language machine translation model was obtained, supporting the "transfer learning" of multi-language translation tasks. It supports distributed training (at least 8 cards) and reasoning (full precision /FP16, 1 card) based on MindSpore on NPU/GPU. The single model supports the mutual translation between any two languages of 53 languages. In the WMT2021 Multilingual quest track, in the FLORES-101 devtest dataset, compare the 50 languages covered by Quest List No.1. -&gt; The average BLEU value in 100 translation directions increased by 0.354.

At present, there are two versions of GPU/NPU because MindSpore versions are different. The mainstream version of MindSpore supported by 'Pengcheng Yunnao 2' NPU is 1.3 at present, and the MS1.6 version of GPU platform has better adaptability

More info about original project mPanGu-Alpha-53 [here]( https://git.openi.org.cn/PCL-Platform.Intelligence/mPanGu-Alpha-53)




