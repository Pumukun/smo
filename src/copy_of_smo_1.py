# -*- coding: utf-8 -*-
"""Copy of SMO_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xzVPpbqNlpSH2nHqxcSjg-MrefkR5D7C
"""

n = 6
m = 13
deltaT_z = 0.724 #(1)
T_ob = 0.738
lamda = 1.142
mu_1 = 1.412 #(1)
mu_2 = 0.235

import numpy as np

def rfind(arr, item):
  b = list(reversed(arr))
  return len(arr) - b.index(item) - 1

t_ob = round(np.random.exponential(1/mu_1), 5)

l = [1]
t_sob = [deltaT_z]
Type = [1]
C_l = [1]
t_ost = [t_ob]
t_ozh = [deltaT_z]
j_l = [1]

for i in range(1, 100):
  l.append(i + 1)
  if (Type[i-1] == 1 or Type[i-1] == 3):
    if(t_sob[i-1] + t_ost[i-1] < t_sob[i-1] + t_ozh[i-1]):
      t_sob.append(round(t_sob[i-1] + t_ost[i-1], 5))
      Type.append(2)
      C_l.append(0)
      t_ost.append(-1)
      t_ozh.append(round(t_ozh[i-1] - t_ost[i-1], 5))
      if (Type[i-1] == 3):
        j_l.append(j_l[rfind(Type, 1)])
      else:
        j_l.append(j_l[i-1])
    else:
      t_sob.append(round(t_sob[i-1] + t_ozh[i-1], 5))
      Type.append(3)
      C_l.append(1)
      t_ost.append(round(t_ost[i-1] - t_ozh[i-1], 5))
      t_ozh.append(deltaT_z)
      j_l.append(j_l[i-1] + 1)
  elif(Type[i-1] == 2):
    t_sob.append(round(t_sob[i-1] + t_ozh[i-1], 5))
    Type.append(1)
    C_l.append(1)
    t_ost.append(round(np.random.exponential(1/mu_1), 5))
    t_ozh.append(deltaT_z)
    j_l.append(max(j_l) + 1)

print(f"l;t_sob;Type;C_l;t_ost;t_ozh;j_l")
for i in range(100):
    print(f"{l[i]};{t_sob[i]};{Type[i]};{C_l[i]};{t_ost[i]};{t_ozh[i]};{j_l[i]}")

t_z = []
t_obsl = []
t_kob = []

for i in range(1, max(j_l) + 1):
  t_z.append(t_sob[j_l.index(i)])
  if (Type[j_l.index(i)] != 3):
    t_obsl.append(t_ost[j_l.index(i)])
    t_kob.append(t_z[i-1] + t_obsl[i-1])
  else:
    t_obsl.append(0)
    t_kob.append(t_z[i-1])

#print(len(t_z))
#print("t_z: ", t_z)
#print("t_obsl", t_obsl)
#print("t_kob: ", t_kob)

print("j;t_z;t_obsl;t_kob")
for i in range(max(j_l)):
    print(f"{i};{t_z[i]};{t_obsl[i]};{t_kob[i]}")

R_0 = C_l.count(0)
R_1 = C_l.count(1)

v_0 = R_0 / 100
v_1 = R_1 / 100

T_0 = 0
T_1 = 0

for i in range(100):
  if (C_l[i] == 1):
    T_1 += t_ost[i]
T_0 = max(t_sob) - T_1

T_0 = round(T_0, 5)
T_1 = round(T_1, 5)

delta_0 = round(T_0 / max(t_sob), 5)
delta_1 = round(T_1 / max(t_sob), 5)

print("R_i v_i T_i    D_i")
print(R_0, v_0, T_0, delta_0)
print(R_1, v_1, T_1, delta_1)
print(R_0 + R_1, v_0 + v_1, T_0 + T_1, delta_0 + delta_1)

#print(R_0, R_1)
#print(v_0, v_1)
#print(T_0, T_1)
#print(delta_0, delta_1)

J = max(j_l)
JF = 0
for i in range(100):
  if (Type[i] == 2):
    JF += 1
JL = J - JF
T_zan = T_0
T_svob = T_1

print(f"J: {J}")
print(f"JF: {JF}")
print(f"JL: {JL}")
print(f"T_zan: {T_zan}")
print(f"T_svob: {T_svob}")