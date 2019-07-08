import random
import numpy as np
from common_utils import *

def sigmoid(s):
	return 1/(1+np.exp(-s))

class Fungus():
    def __init__(self,gene=None,n_types=4,n_space=3,n_states=2,sig=-1):
    	self.n_types=n_types
    	self.n_space=n_space
    	self.n_states=n_states
    	self.score=0
    	self.alive=True
    	self.size=None
    	self.sig=sig
    	prob=sigmoid(sig)#the marginal probability to create a living cell
    	self.p=np.zeros(2)
    	self.p[0]=1-prob
    	self.p[1]=prob
    	self.life_frames=[]#here we store the played frames
    	if gene is not None:
    		self.gene=gene
    	else:
    		gene=np.zeros((n_types,n_types,n_types,n_types,n_space,n_types,n_types,n_types,n_types)).astype(int)
    		for i1 in range(n_types):
    			for i2 in range(n_types):
    				for i3 in range(n_types):
    					for i4 in range(n_types):
    						for i5 in range(n_space):
    							for i6 in range(n_types):
    								for i7 in range(n_types):
    									for i8 in range(n_types):
    										for i9 in range(n_types):
    											gene[i1,i2,i3,i4,i5,i6,i7,i8,i9]=int(np.random.choice(n_states, 1, p=self.p))
    		self.gene=gene

    def get_mutation_gene(self,N=1):
    	mut_gene=np.copy(self.gene)
    	for n in range(N):
	    	i=np.random.randint(self.n_types,size=8)
	    	j=np.random.randint(self.n_space,size=1)
	    	idx=(i[0],i[1],i[2],i[3],j[0],i[4],i[5],i[6],i[7])
	    	#mut_gene[idx]=-mut_gene[idx]+1 #flip mutation
	    	mut_gene[idx]=np.random.choice(self.n_states,1,p=self.p)
    	# print(np.sum(mut_gene!=self.gene))
    	self.sig+=(2*np.random.randint(2,size=1)-1)*(0.1*np.abs(self.sig)+0.1)
    	return mut_gene,self.sig

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
		self.fungus.size=(self.frame_list[-1] == 1).sum()
		self.fungus.score=((self.frame_list[0]==3).sum()-(self.frame_list[-1]==3).sum()+10)/((self.frame_list[-1]== 1).sum()+10)
		return self.n_iter		

	def play_green_is_life(self,max_n_iter=10000,die_fac=1000):
		s=self.frame_list[-1].shape
		mass_integrator=0
		score=0
		while self.n_iter<max_n_iter:
			current_idx_map=self.frame_list[-1]
			current_size=(current_idx_map == 1).sum()
			mass_integrator+=current_size
			current_grass_eaten=((self.frame_list[0]==3).sum()-(self.frame_list[-1]==3).sum())+10
			score=current_grass_eaten**1.5/mass_integrator
			#print('current grass eaten='+str(current_grass_eaten)+'-- mass integrator='+str(mass_integrator))
			p_die=2*(1-sigmoid(die_fac*score))#probability to die for any living cell
			prob=[p_die,1-p_die]
			new_idx_map=np.copy(current_idx_map)
			for i in range(1,s[0]-1):
				for j in range(1,s[1]-1):
					#living space condition
					if current_idx_map[i,j] ==0 or current_idx_map[i,j] ==1 or current_idx_map[i,j] ==3:
						nh=current_idx_map[i-1:i+2,j-1:j+2].flatten().astype(int)
						if current_idx_map[i,j]==1:
							current_idx_map[i,j]=int(np.random.choice(2, 1, p=prob))
						if 1 in nh:
							if nh[4]==3:
								nh[4]=2
							new_idx_map[i,j]=self.fungus.gene[nh[0],nh[1],nh[2],nh[3],nh[4],nh[5],nh[6],nh[7],nh[8]]
			if not self.save_frames:
				del self.frame_list[-1]
			self.frame_list.append(new_idx_map)
			self.n_iter+=1
			if current_size==0 or np.array_equal(self.frame_list[-1],self.frame_list[-2]):
				self.fungus.life_frames=self.frame_list
				self.fungus.size=current_size
				self.fungus.alive=False
				print('the fungus died!')
				return self.n_iter
		self.fungus.life_frames=self.frame_list
		self.fungus.size=(new_idx_map == 1).sum()
		self.fungus.score=score
		return self.n_iter	

def competition(population,idx_map,max_n_iter=200):
	i=1
	for fungus in population:
		print('play-round of fungus: '+str(i))
		n_iter=Game(idx_map,fungus,save_frames=True).play_green_is_life(max_n_iter=max_n_iter)
		#fungus.score=((fungus.life_frames[0]==3).sum()-(fungus.life_frames[-1]==3).sum()+10)/(fungus.size+10)
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
		mutated_gene,mutated_s=ancestors[np.mod(n,L)].get_mutation_gene(N=n_mutations)
		descendants.append(Fungus(gene=mutated_gene,sig=mutated_s))
		n+=1
	return descendants

def make_gif(life_frames,path='best_fungus.gif'):
	frames=[]
	for f in life_frames:
		np_f=int_array_to_npimg(f)
		pil_f=np_to_pil(np_f)
		frames.append(pil_f)
	frames[0].save(path,
	               save_all=True,
	               append_images=frames[1:],
	               duration=100,
	               loop=0)





