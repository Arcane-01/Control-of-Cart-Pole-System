import matplotlib.pyplot as plt 
import math 
import numpy as np  
import scipy.linalg

x_arr = []
theta_arr = []
ss = 0.1
M = 5
m = 1
L = 2
g = 9.8

theta_des = 3.14
theta_ini = 0
A = np.array([[0,1,0,0],\
              [0,0,-1*m*g/M,0],\
              [0,0,0,1],\
              [0,0,1*(m+M)*g/(M*L),0]])
B = np.array([0,1/M,0,-1/(M*L)])
B = B.reshape([4,1])

Q = np.array([[90,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
R = [[4000]]  

state = np.array([0,0,-1*np.pi,0],dtype="float")
state = state.reshape([4,1])

state_des = np.array([5,0,0,0],dtype="float")
state_des = state_des.reshape([4,1])

S = scipy.linalg.solve_continuous_are(A, B, Q, R)
temp = np.matmul(np.linalg.inv(R),np.transpose(B))  #np.linalg.inv(R)*np.transpose(B)*S
k = np.matmul(temp,S)

time = []
u_arr = []
theta_ddot = 0
theta_dot = 0
theta = 0
x = 0
x_dot = 0
x_ddot = 0

for i in range(0,600):
  u = [[1]]*np.matmul(k,state_des-state)
  u = u[0][0]
  #print(state[2][0])
  x_ddot = (u+m*math.sin(state[2][0])*(L*(state[3][0]**2)-g*math.cos(state[2][0])))/(M+m*(math.sin(state[2][0])**2))
  theta_ddot = ( (-1*u*math.cos(state[2][0])) - (m*L*(state[3][0]**2)*math.sin(state[2][0])*math.cos(state[2][0])) + ((M+m)*g*math.sin(state[2][0])))/(L*(M+(m*(math.sin(state[2][0])**2))))
 
  state[3][0]+=(theta_ddot*ss)
  state[2][0]+=(0.5*theta_ddot*(ss**2))+state[3][0]*ss

  state[1][0]+=(x_ddot*ss)
  state[0][0]+=(0.5*x_ddot*(ss**2))+state[1][0]*ss
  #print(state[2][0])
  # if state[2][0] < -1*math.pi:
  #   state[2][0] = (2*math.pi + state[2][0])
  # if state[2][0] > 1*math.pi:
  #   state[2][0] = -1*(2*math.pi - state[2][0])

  # if state[2][0] < -1*math.pi:
  #   while state[2][0] < -2*math.pi:
  #     state[2][0] = 2*math.pi + state[2][0]
  #   state[2][0] = (2*math.pi + state[2][0])
  # if state[2][0] > 1*math.pi:
  #   while state[2][0] > 2*math.pi:
  #     state[2][0] =  state[2][0] - 2*math.pi
  #   state[2][0] = -1*(2*math.pi - state[2][0])


  # a = math.tan(state[2][0])
  # b = math.atan(a)
  # state[2][0] = b

  state[2][0] = math.atan2(math.sin(state[2][0]), math.cos(state[2][0]))

  x_arr.append(state[0][0])
  theta_arr.append(state[2][0])
  time.append(i/10)
  u_arr.append(u)



plot4=plt.figure(4)
plt.plot(time,theta_arr,linewidth=2,label='theta')
plt.xlabel('time')
plt.ylabel('theta')
plt.title('theta vs time')
plt.legend()

plot2=plt.figure(2)
plt.plot(time,x_arr,linewidth=2,label='x')
plt.xlabel('time')
plt.ylabel('x')
plt.title('x vs time')
plt.legend()

plot3=plt.figure(3)
plt.plot(time,u_arr,linewidth=2,label='u')
plt.xlabel('time')
plt.ylabel('u')
plt.title('u vs time')
plt.legend()
plt.show()

plt.show()

def plot():

        import math
        from matplotlib.animation import FuncAnimation 
        from matplotlib import pyplot as plt
        from math import pi
        from matplotlib import rc
        rc('animation', html='jshtml')
        # obj = ip()
        rod_length = 7
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111,autoscale_on=False,\
                        xlim=(-10,50),ylim=( -30,30))
        mass1, = ax.plot([],[],linestyle='None',marker='s',\
                        markersize=30,markeredgecolor='k',\
                        color='orange',markeredgewidth=2)

        mass2, = ax.plot([],[],linestyle='None',marker='o',\
                        markersize=20,markeredgecolor='k',\
                        color='orange',markeredgewidth=2)
        line, = ax.plot([],[],'o-',color='orange',lw=4,\
                        markersize=6,markeredgecolor='k',\
                        markerfacecolor='k')
        def animate(i):
                x = x_arr[i]
                y = 0
                #angle = -1*theta_arr[i]  +  pi
                angle = theta_arr[i] 
                mass1.set_data([x_arr[i]],[0])
                mass2.set_data([x + rod_length*math.sin(angle)],[y + rod_length*math.cos(angle) ])
                line.set_data([x ,x + rod_length*math.sin(angle) ],[y , y + rod_length*math.cos(angle)])
                return  mass1 , mass2 , line ,

        anim = FuncAnimation(fig, animate, init_func = None, 
                        frames = len(x_arr), interval = 200, blit = True ) 

        anim.save('optimize.gif', writer='pillow', fps=10)
        plt.show()

plot()