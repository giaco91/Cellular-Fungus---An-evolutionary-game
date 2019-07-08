import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import random
import pickle
import argparse

from common_utils import *
from fungus import *

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
parser.add_argument('--map_path', default='maps/', help='path to map')
parser.add_argument('--gif_path', default='gifs/', help='path where gifs should be stored')
parser.add_argument('--winner_path', default='selected_pop/', help='where to store the best fungus subpopulation')
parser.add_argument('--map', type=int, help='which map do you want to play?', default=6)
parser.add_argument('--n_pop', type=int, help='size of population?', default=2)
parser.add_argument('--n_survive', type=int, help='number of selected subpopulation?', default=1)
parser.add_argument('--n_gen', type=int, help='how many generations?', default=3)
parser.add_argument('--n_mut', type=int, help='how many point mutations?', default=1000)
parser.add_argument('--n_iter', type=int, help='how many iterations per game?', default=20)
parser.add_argument('--load_pop', type=str2bool, help='do you want to load a saved popuplation?', default=False)


opt = parser.parse_args()
print(opt)

# new_im=create_image(256,256)
# new_im.save(img_path+'map7.png', 'png')
# raise ValueError('')


#load images
map_list=[]
i=0
for map_name in os.listdir(opt.map_path):
  if map_name.endswith(".jpg") or map_name.endswith(".png"):
    map_list.append(pil_to_np(load(opt.map_path+map_name).convert("RGB")))
    i+=1
# np_to_pil(img_list[0]).show()
idx_map=npimg_to_int_array(map_list[opt.map-1])

#--initialize first population
if opt.load_pop:
	print('load old generation')
	with open(opt.winner_path+'best_subpop_map='+str(opt.map)+'.pkl', 'rb') as f:
	    best_subpop = pickle.load(f)
	population=mutation(best_subpop,opt.n_pop,n_mutations=opt.n_mut)
else:
	print('create new generation')
	population=[]
	for n in range(opt.n_pop):
		population.append(Fungus(n_types=4))


#-----evolution
for nc in range(opt.n_gen):
	print('----competition: '+str(nc+1))
	competition(population,idx_map,max_n_iter=opt.n_iter)
	selected_subpop=selection(population,opt.n_survive)
	print('best score: '+str(selected_subpop[0].score))
	print('marginal life probability of best fungus: '+str(selected_subpop[0].p))
	np_idx_frames=selected_subpop[0].life_frames
	make_gif(np_idx_frames,path=opt.gif_path+'best_fungus_map='+str(opt.map)+'_gen='+str(nc)+'.gif')

	with open(opt.winner_path+'best_subpop_map='+str(opt.map)+'.pkl', 'wb') as f:
		pickle.dump(selected_subpop, f )
	population=mutation(selected_subpop,opt.n_pop,n_mutations=opt.n_mut)


#---make gif
with open(opt.winner_path+'best_subpop_map='+str(opt.map)+'.pkl', 'rb') as f:
    best_subpop = pickle.load(f)
np_idx_frames=best_subpop[0].life_frames
make_gif(np_idx_frames,path=opt.gif_path+'best_subpop_map='+str(opt.map)+'.gif')



