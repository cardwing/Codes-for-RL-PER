from collections import deque
import random
import rank_based

class ReplayBuffer(object):

  def __init__(self, buffer_size):

    self.buffer_size = buffer_size
    self.num_experiences = 0
    #self.buffer = deque()
    conf = {'size': 10000,
            'learn_start': 32,
            'partition_num': 32,
            'total_step': 10000,
            'batch_size': 32}
    self.replay_memory = rank_based.Experience(conf)

  def getBatch(self, batch_size):
    # random draw N
    #return random.sample(self.buffer, batch_size)
    batch, w, e_id = self.replay_memory.sample(self.num_experiences)
    self.e_id=e_id
    self.w_id=w
    '''#state t
    self.state_t_batch = [item[0] for item in batch]
    self.state_t_batch = np.array(self.state_t_batch)
    #state t+1        
    self.state_t_1_batch = [item[1] for item in batch]
    self.state_t_1_batch = np.array( self.state_t_1_batch)
    self.action_batch = [item[2] for item in batch]
    self.action_batch = np.array(self.action_batch)
    self.action_batch = np.reshape(self.action_batch,[len(self.action_batch),self.num_actions])
    self.reward_batch = [item[3] for item in batch]
    self.reward_batch = np.array(self.reward_batch)
    self.done_batch = [item[4] for item in batch]
    self.done_batch = np.array(self.done_batch)''' 
    return batch, self.w_id, self.e_id


  def size(self):
    return self.buffer_size

  def add(self, state, action, reward, next_state, done):#add(self, state, next_state, action, reward, done):
    #new_experience = (state, next_action, action, reward, done)#(state, action, reward, next_state, done)
    self.replay_memory.store((state, action, reward, next_state, done))
    #if self.num_experiences < self.buffer_size:
    #  self.buffer.append(new_experience)
    self.num_experiences += 1
    #else:
    #  self.buffer.popleft()
    #  self.buffer.append(new_experience)

  def count(self):
    # if buffer is full, return buffer size
    # otherwise, return experience counter
    return self.num_experiences

  #def erase(self):
  #  self.buffer = deque()
  #  self.num_experiences = 0
  def rebalance(self):
    self.replay_memory.rebalance()

  def update_priority(self, indices, delta):
    self.replay_memory.update_priority(indices, delta)
