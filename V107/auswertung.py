# -*- coding: utf-8 -*-
from numpy import *
from matplotlib.pyplot import *
import linregress

# 1. Viskosität bei 20 Grad mithilfe kleiner Kugel bestimmen

t_1 = loadtxt("Temp_const_k1.txt")
K_1 = 0.07640 # mPa cm^3 /g Apparaturkonstante
r_w = 998.20 # kg/m^3
r_w = r_w /1000 #g/ cm^3 Dichte von Wasser

#Dichte von Kugel 1 bestimmen

D1_array = loadtxt("Durchmesser_K1.txt")

D_1 = mean(D1_array) # mm
D_1 = D_1 / 10 # cm
m_1 = 4.45 # g

V_1 = 4/3 * pi * (D_1/2)**3 # cm^3

r_K1 = m_1 / V_1 # g / cm^3

# Nun wirklich die Viskosität bestimmen

eta_array = K_1 * (r_K1 - r_w) * t_1 # mPa *s
eta = mean(eta_array)

# 2. K_2 mithilfe von eta und Zeitmessung bestimmen

t_2 = loadtxt("Temp_const_k2.txt")
m_2 = 4.95 # g
D_2 = 1.58 # cm
V_2 = 4/3 * pi * (D_2/2)**3


r_K2 = m_2/V_2

K_2array = eta/((r_K2 - r_w)*t_2)
K_2 = mean(K_2array)


# 3. Temperaturabhängigkeit der Viskosität

(T,t) = loadtxt("Temp_var_K2.txt",unpack = True)

eta_T = K_2*(r_K2 - r_w)*t
n1,n2,n3,n4,n5,n6,n7,n8,n9,n10 = array_split(eta_T,10)

visko = [n1,n2,n3,n4,n5,n6,n7,n8,n9,n10]

def n(x):
    return mean(visko[x])


plot(1/T, log(eta_T),'x', label = "Messwerte")



(B,A),cov = linregress.linear_fit(1/T, log(eta_T))

#Ausgleichsgerade
def f(x):
    return B*x + A

plot(1/T, f(1/T), label = "Ausgleichsgerade")
xlabel("1/T in 1/s")
ylabel("log($\eta$) in log(mPa s)")
legend(loc = 'lower right')
grid()
savefig("viskoseplot.pdf")
close()


#Reynoldszahl
v_m1_array = 10/t_1 # cm / s
v_m1 = mean(v_m1_array)
Re_1 = v_m1 * D_1 * r_w / eta


v_m2_array = 19/t_2 # cm/s
v_m2 = mean(v_m2_array)
Re_2 = v_m2 * D_2 * r_w / eta




#Fehlerrechnung bei temp.abh. Viskosität (1 Fehler pro Temp.)
t1,t2,t3,t4,t5,t6,t7,t8,t9,t10 = array_split(t,10)

temp = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10]
#temo[0]= 25 Grad, temp[1] = 32 Grad, temp[2] = 35 Grad usw...
def dn(x):
    return sqrt((K_2 * (r_K2 - r_w)* std(temp[x])/2)**2 + ((r_K2 - r_w)* mean(temp[x]) * std(K_2array)/sqrt(20))**2)
