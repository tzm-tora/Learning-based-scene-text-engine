from src.trainer import Trainer
import torch.multiprocessing as mp
import torch
import cfg
import os
import sys
os.environ["CUDA_VISIBLE_DEVICES"] = cfg.gpu
sys.setrecursionlimit(1000000)


def main_worker(rank, world_size):
    torch.cuda.set_device(rank)
    device = torch.device(rank)
    print(device)
    torch.backends.cudnn.benchmark = True
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"
    # torch.distributed.init_process_group(
    #     'nccl', init_method='tcp://127.0.0.1:25555', world_size=world_size, rank=rank)
    torch.distributed.init_process_group(
        'nccl', init_method='env://', world_size=world_size, rank=rank)
    torch.distributed.barrier()

    trainer = Trainer(device, rank)
    trainer.iterate()
    print('train finished')


if __name__ == '__main__':
    world_size = torch.cuda.device_count()
    print('world_size: ', world_size)
    mp.spawn(main_worker, args=(world_size,), nprocs=world_size, join=True)
