
pull from [DynamicDet](https://github.com/VDIGPKU/DynamicDet)

<!-- <details>
<summary> Table Notes </summary>

- FPS is measured on the same machine with 1 NVIDIA V100 GPU, with `batch_size = 1`, `no_trace` and `fp16`.

- More results can be found on the paper.

</details> -->


## Quick Start
```bash
# create the docker container, you can change the share memory size if you have more.
docker run --gpus all --name dynamicdet -it -v your_code_path/:/dynamicdet --shm-size=64g nvcr.io/nvidia/pytorch:21.08-py3

# apt install required packages
apt update
apt install -y zip htop screen libgl1-mesa-glx

# pip install required packages
pip install seaborn thop
```



### Data preparation

<!-- Download MS COCO dataset images ([train](http://images.cocodataset.org/zips/train2017.zip), [val](http://images.cocodataset.org/zips/val2017.zip), [test](http://images.cocodataset.org/zips/test2017.zip)) and [labels](https://github.com/VDIGPKU/DynamicDet/releases/download/v0.1/coco2017labels-segments.zip). -->

```
DOTA
  ├── test_split_1024
  │   └── images
  ├── train_split_1024
  │   ├── images
  │   ├── labels
  │   └── original_labels
  ├── val_split_1024
  │   ├── images
  │   ├── labels
  │   └── original_labels
```

### Training

Step1: Training cascaded detector

- Single GPU training

  ```bash
  python train_step1.py --workers 8 --device 0 --batch-size 16 --epochs 300 --img 1024 --cfg cfg/dy-yolov7-step1.yaml --weight '' --data data/DOTA_1024.yaml --hyp hyp/hyp.scratch.p5.yaml --name dy-yolov7-step1
  ```

- Multiple GPU training (OURS, RECOMMENDED 🚀)

  ```bash
  python -m torch.distributed.launch --nproc_per_node 8 --master_port 9527 train_step1.py --workers 8 --device 0,1,2,3,4,5,6,7 --sync-bn --batch-size 128 --epochs 300 --img 1024 --cfg cfg/dy-yolov7-step1.yaml --weight '' --data data/DOTA_1024.yaml --hyp hyp/hyp.scratch.p5.yaml --name dy-yolov7-step1
  ```

Step2: Training adaptive router

```bash
python train_step2.py --workers 4 --device 0 --batch-size 1 --epochs 2 --img 1024 --adam --cfg cfg/dy-yolov7-step2.yaml --weight runs/train/dy-yolov7-step1/weights/last.pt --data data/DOTA_1024.yaml --hyp hyp/hyp.finetune.dynamic.adam.yaml --name dy-yolov7-step2
```

### Getting the dynamic thresholds for variable-speed inference

  ```bash
python get_dynamic_thres.py --device 0 --batch-size 1 --img-size 1024 --cfg cfg/dy-yolov7-step2.yaml --weight weights/dy-yolov7.pt --data data/DOTA_1024.yaml --task val
  ```

### Testing

  ```bash
python test.py --img-size 1024 --batch-size 1 --conf 0.001 --iou 0.65 --device 0 --cfg cfg/dy-yolov7-step2.yaml --weight weights/dy-yolov7.pt --data data/DOTA_1024.yaml --dy-thres <DY_THRESHOLD>
  ```

### Inference

  ```bash
python detect.py --cfg cfg/dy-yolov7-step2.yaml --weight weights/dy-yolov7.pt --num-classes 16 --source <IMAGE/VIDEO> --device 0 --dy-thres <DY_THRESHOLD>
  ```

## Citation

If you find this repo useful in your research, please consider citing the following paper:

```BibTex
@inproceedings{lin2023dynamicdet,
  title={DynamicDet: A Unified Dynamic Architecture for Object Detection},
  author={Lin, Zhihao and Wang, Yongtao and Zhang, Jinhe and Chu, Xiaojie},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2023}
}
```

## License

The project is only free for academic research purposes, but needs authorization for commerce. For commerce permission, please contact wyt@pku.edu.cn.
