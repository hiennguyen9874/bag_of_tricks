import torch
import os
import logging
from datetime import datetime

from torch.utils.tensorboard import SummaryWriter

from logger import setup_logging

class BaseTrainer(object):
    def __init__(self, config):
        self.config = config
        
        self.cfg_trainer = config['trainer_colab'] if config['colab'] == True else config['trainer']

        self.run_id = datetime.now().strftime(r'%m%d_%H%M%S')
        
        self.checkpoint_dir = os.path.join(self.cfg_trainer['checkpoint_dir'], self.run_id)
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        
        self.logs_dir = os.path.join(self.cfg_trainer['log_dir'], self.run_id)
        os.makedirs(self.logs_dir, exist_ok=True)

        self.logs_dir_saved = os.path.join(self.cfg_trainer['log_dir_saved'], self.run_id)

        setup_logging(self.logs_dir)
        self.logger = logging.getLogger('train')

        self.logger.info('Tensorboard: tensorboard --logdir {}'.format(self.cfg_trainer['log_dir']))

        self.use_gpu = config['n_gpu'] > 0 and torch.cuda.is_available()
        self.device = torch.device('cuda:0' if self.use_gpu else 'cpu')
        self.map_location = (lambda storage, loc: storage) if self.use_gpu else None

        self.epochs = self.cfg_trainer['epochs']
        self.start_epoch = 1
        self.writer = SummaryWriter(self.logs_dir)