import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import random
import pickle 
from common_utils import *
from fungus import *

img_path='maps/'
map=5



# new_im=create_image(256,256)
# new_im.save(img_path+'map7.png', 'png')
# raise ValueError('')



#load images
img_list=[]
i=0
for img_name in os.listdir(img_path):
  if img_name.endswith(".jpg") or img_name.endswith(".png"):
    img_list.append(pil_to_np(load(img_path+img_name).convert("RGB")))
    i+=1
# np_to_pil(img_list[0]).show()
idx_map=npimg_to_int_array(img_list[map-1])


N=3#size of population
n=1#size of selected subpop
n_mutations=100
num_competitions=3
load_pop=False
max_n_iter=20

#--initialize first population
if load_pop:
	with open('best_subpop.pkl', 'rb') as f:
	    best_subpop = pickle.load(f)
	population=mutation(best_subpop,N)
else:
	population=[]
	for n in range(N):
		population.append(Fungus(n_types=4))
#-----evolution
for nc in range(num_competitions):
	print('----competition: '+str(nc+1))
	competition(population,idx_map,max_n_iter=max_n_iter)
	selected_subpop=selection(population,n)
	print('best score: '+str(selected_subpop[0].score))
	np_idx_frames=selected_subpop[0].life_frames
	make_gif(np_idx_frames,path='best_subpop_'+str(nc)+'.gif')

	with open('best_subpop.pkl', 'wb') as f:
		pickle.dump(selected_subpop, f )
	population=mutation(selected_subpop,N,n_mutations=n_mutations)


#---make gif
with open('best_subpop.pkl', 'rb') as f:
    best_subpop = pickle.load(f)
np_idx_frames=best_subpop[0].life_frames
make_gif(np_idx_frames)



