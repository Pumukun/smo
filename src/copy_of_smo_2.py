# -*- coding: utf-8 -*-
"""Copy of SMO_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DEn_wmnUVL8AcUixs-YD7DIBc9H_KJWB
"""

n = 6
m = 13
deltaT_z = 0.724
T_ob = 0.738 #(2)
lamda = 1.142 #(2)
mu_1 = 1.412
mu_2 = 0.235

import numpy as np

def rfind(arr, item):
  b = list(reversed(arr))
  return len(arr) - b.index(item) - 1

t_z = round(np.random.exponential(1/lamda), 5)

l = [1]
t_sob = [t_z]
Type = [1]
C_l = [1]
t_ost = [T_ob]
t_ozh = [round(np.random.exponential(1/mu_1), 5)]
j_l = [1]

for i in range(1, 100):
  l.append(i + 1)
  if(t_ost[i-1] < t_ozh[i-1] and t_ost[i-1] != -1):
    t_sob.append(round(t_sob[i-1] + T_ob, 5))
    Type.append(2)
    C_l.append(C_l[i-1] - 1)
    if(C_l[i] != 0):
      t_ost.append(round(T_ob, 5))
    else:
      t_ost.append(-1)
    t_ozh.append(round(t_ozh[i-1] - t_ost[i-1], 5))
    j_l.append(max(j_l) - C_l[i])
  else:
    t_sob.append(round(t_sob[i-1] + t_ozh[i-1], 5))
    Type.append(1)
    C_l.append(C_l[i-1] + 1)
    if (t_ost[i-1] != -1):
      t_ost.append(round(t_ost[i-1] - t_ozh[i-1], 5))
    else:
      t_ost.append(T_ob)
    t_ozh.append(round(np.random.exponential(1/mu_1), 5))
    j_l.append(max(j_l) + 1)

print(l)
print(t_sob)
print(Type)
print(C_l)
print(t_ost)
print(t_ozh)
print(j_l)

print("l;t_sob;Type;C_l;t_ost;t_ozh;j_l")
for i in range(100):
  print(f"{l[i]};{t_sob[i]};{Type[i]};{C_l[i]};{t_ost[i]};{t_ozh[i]};{j_l[i]}")

t_z = []
q_j = []
t_och = []
t_nob = []
t_obsl = []
t_kob = []
j = []

for i in range(1, max(j_l) + 1):
  j.append(i)
  t_z.append(t_sob[j_l.index(i)])

  if(C_l[j_l.index(i)] > 1):
    q_j.append(C_l[j_l.index(i)] - 1)
    t_och.append(round(t_ost[j_l.index(i)] + T_ob * q_j[i-1], 5))
    t_nob.append(round(t_z[i-1] + t_och[i-1], 5))
  else:
    q_j.append(0)
    t_och.append(0)
    t_nob.append(t_z[i-1])

  t_obsl.append(T_ob)
  t_kob.append(round(t_nob[i-1] + T_ob, 5))

print("j;t_z;q_j;t_och;t_nob;t_obsl;t_kob")
for i in range(len(j)):
  print(f"{j[i]};{t_z[i]};{q_j[i]};{t_och[i]};{t_nob[i]};{t_obsl[i]};{t_kob[i]}")

R = []
v = []
T = list(np.zeros(len(set(C_l))))
delta = []

for i in range(0, max(C_l) + 1):
  R.append(C_l.count(i))
  v.append(R[i] / 100)
  for j in range(99):
    if (C_l[j] == i):
      T[i] += round(t_sob[j+1] - t_sob[j], 5)
  T[i] = round(T[i], 5)
  delta.append(round(T[i] / max(t_z), 5))

print("R;v;T;delta")
for i in range(len(R)):
    print(f"{R[i]};{v[i]};{T[i]};{delta[i]}")

#print(R)
#print(v)
#print(T)
#print(delta)

for i in range(len(R)):
  print(delta[i])

J = max(j_l)
JF = 0
for i in range(100):
  if (Type[i] == 2):
    JF += 1
z = round(sum(C_l) / 100, 5)
_t_och = round(sum(t_och) / JF, 5)
_t_smo = round((sum(t_kob) - sum(t_z)) / JF, 5)

T_svob = round(T[0], 5)

print("J:", J)
print("JF: ", JF)
print("z: ", z)
print("_t_och: ", _t_och)
print("_t_smo: ", _t_smo)
print("T_svob: ", T_svob)

