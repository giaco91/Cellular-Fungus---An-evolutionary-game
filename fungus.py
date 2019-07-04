import random
import numpy as np
from common_utils import *

class Fungus():
    def __init__(self,gene=None,n_types=3):
    	self.n_types=n_types
    	self.score=0
    	self.alive=True
    	self.size=None
    	self.life_frames=[]#here we store the played frames
    	if gene is not None:
    		self.gene=gene
    	else:
    		p=[0.8,0.2]
    		gene=np.zeros((n_types,n_types,n_types,n_types,n_types,n_types,n_types,n_types,n_types)).astype(int)
    		for i1 in range(n_types):
    			for i2 in range(n_types):
    				for i3 in range(n_types):
    					for i4 in range(n_types):
    						for i5 in range(n_types):
    							for i6 in range(n_types):
    								for i7 in range(n_types):
    									for i8 in range(n_types):
    										for i9 in range(n_types):
    											gene[i1,i2,i3,i4,i5,i6,i7,i8,i9]=np.random.choice(2, 1, p=p)
    		self.gene=gene


    def get_mutation_gene(self,N=1):
    	mut_gene=np.copy(self.gene)
    	for n in range(N):
	    	i=np.random.randint(self.n_types,size=9)
	    	idx=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])
	    	mut_gene[idx]=-mut_gene[idx]+1
    	# print(np.array_equal(mut_gene,self.gene))
    	return mut_gene

class Game():
	def __init__(self,idx_map,fungus,save_frames=False,max_size=1000):
		self.fungus=fungus
		self.n_iter=0
		self.frame_list=[]
		self.frame_list.append(idx_map)
		self.save_frames=save_frames
		self.max_size=max_size

	def play_green_is_win(self,max_n_iter=10000):
		s=self.frame_list[-1].shape
		while self.n_iter<max_n_iter:
			current_idx_map=self.frame_list[-1]
			new_idx_map=np.copy(current_idx_map)
			current_size=(new_idx_map == 1).sum()
			for i in range(1,s[0]-1):
				for j in range(1,s[1]-1):
					#living space condition
					if current_idx_map[i,j] ==1 or current_idx_map[i,j] ==0:
						nh=current_idx_map[i-1:i+2,j-1:j+2].flatten().astype(int)
						#win condition
						if 1 in nh and 3 in nh:
							print('game is won in the '+str(self.n_iter+1)+' round!')
							self.fungus.life_frames=self.frame_list
							self.fungus.size=current_size
							self.fungus.alive=True
							return self.n_iter
						#locality condition						
						if 1 in nh:
							new_idx_map[i,j]=self.fungus.gene[nh[0],nh[1],nh[2],nh[3],nh[4],nh[5],nh[6],nh[7],nh[8]]
			if not self.save_frames:
				del self.frame_list[-1]
			self.frame_list.append(new_idx_map)
			self.n_iter+=1
			
			print('round: '+str(self.n_iter)+'----current size: '+str(current_size))
			if current_size==0 or current_size>self.max_size or np.array_equal(self.frame_list[-1],self.frame_list[-2]):
				self.fungus.life_frames=self.frame_list
				self.fungus.size=current_size
				self.fungus.alive=False
				print('the fungus died!')
				return self.n_iter
		print('the fungus died!')
		self.fungus.life_frames=self.frame_list
		self.fungus.size=current_size
		self.fungus.alive=False
		return self.n_iter

	def play_no_win(self,max_n_iter=10000):
		s=self.frame_list[-1].shape
		while self.n_iter<max_n_iter:
			current_idx_map=self.frame_list[-1]
			new_idx_map=np.copy(current_idx_map)
			for i in range(1,s[0]-1):
				for j in range(1,s[1]-1):
					#living space condition
					if current_idx_map[i,j] ==0 or current_idx_map[i,j] ==1 or current_idx_map[i,j] ==3:
						nh=current_idx_map[i-1:i+2,j-1:j+2].flatten().astype(int)					
						if 1 in nh:
							new_idx_map[i,j]=self.fungus.gene[nh[0],nh[1],nh[2],nh[3],nh[4],nh[5],nh[6],nh[7],nh[8]]
			if not self.save_frames:
				del self.frame_list[-1]
			self.frame_list.append(new_idx_map)
			self.n_iter+=1
			# print('round: '+str(self.n_iter))
			if np.array_equal(self.frame_list[-1],self.frame_list[-2]):
				self.fungus.life_frames=self.frame_list
				self.fungus.size=(new_idx_map == 1).sum()
				self.fungus.alive=False
				print('the fungus died!')
				return self.n_iter
		self.fungus.life_frames=self.frame_list
		self.fungus.size=(new_idx_map == 1).sum()
		return self.n_iter		


def competition(population,idx_map,max_n_iter=200):
	i=1
	for fungus in population:
		print('play-round of fungus: '+str(i))
		n_iter=Game(idx_map,fungus,save_frames=True).play_no_win(max_n_iter=max_n_iter)
		fungus.score=((fungus.life_frames[0]==3).sum()-(fungus.life_frames[-1]==3).sum()+1)/(fungus.size+1)
		make_gif(fungus.life_frames)
		i+=1

def selection(population,N):
	L=len(population)
	selected_population=[]
	if N>=L:
		print('no selection!')
		return population
	alive_fungus=[]
	dead_fungus=[]
	score_table=[]
	for l in range(L):
		if population[l].alive:
			alive_fungus.append(population[l])
			score_table.append(population[l].score)
		else:
			dead_fungus.append(population[l])
	if len(alive_fungus)==0:
		raise ValueError('Unfortunatelly, all fungus are dead:(')
	print(score_table)
	sorted_idx=np.argsort(-np.asarray(score_table))
	sorted_alife_fungus = [alive_fungus[i] for i in sorted_idx]
	return (sorted_alife_fungus+dead_fungus)[:N]

def mutation(ancestors,N,n_mutations=100):
	L=len(ancestors)
	n=0
	descendants=[]
	while n<=N-1:
		mutated_gene=ancestors[np.mod(n,L)].get_mutation_gene(N=n_mutations)
		descendants.append(Fungus(gene=mutated_gene))
		n+=1
	return(descendants)

def make_gif(life_frames,path='best_fungus.gif'):
	frames=[]
	for f in life_frames:
		np_f=int_array_to_npimg(f)
		pil_f=np_to_pil(np_f)
		frames.append(pil_f)
	frames[0].save(path,
	               save_all=True,
	               append_images=frames[1:],
	               duration=150,
	               loop=0)





