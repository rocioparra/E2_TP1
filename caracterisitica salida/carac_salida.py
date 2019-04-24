import numpy as np
import matplotlib.pyplot as plt
import csv
import itertools


def plot_med(voreg, file):
	vo = []
	io = []
	with open(file, 'r') as csvfile:
		f = csv.reader(csvfile)

		first_row = next(itertools.islice(f, 1)) # elementos hasta el 1 -> solo el 0
		k = first_row.index(str(voreg))

		f = itertools.islice(f, 2, None) # elementos del 2 en adelante
		for row in f:
			vo.append(float(row[k]))
			io.append(float(row[k+1]))

	plt.plot(io, vo, "ro")


def plot_sim(voreg):
	vo = []
	io = []
	with open("e2_tp1_foldback_"+str(voreg)+"V.csv", 'r') as file:
		f = csv.reader(file, delimiter=';')
		f = itertools.islice(f, 1, None)

		for row in f:
			vo.append(float(row[1]))
			io.append(float(row[2]))

	plt.plot(io, vo, "go")


def plot_calc(voreg):
	io, vo = foldback(voreg)
	io = list(io) + [0]
	vo = vo + [voreg]
	plt.plot(io, vo, 'b')


def foldback(voreg):
	r4 = 0.6
	vbe = 0.7
	r2 = 39e3
	r3 = 1.5e3
	beta = r2/(r2+r3)

	iocc = vbe/r4/beta
	iomax = (vbe+voreg*(1-beta))/r4/beta

	io = np.linspace(iocc, iomax, num=50, endpoint=True)
	vo = [(i*r4*beta - vbe)/(1-beta) for i in io]
	return io, vo


def plot_all(voreg):
	if voreg not in [9, 12, 15]:
		print("ahre")
		return

	plot_calc(voreg)
	plt.legend(["Calculado"])
	plot_sim(voreg)
	plt.legend(["Simulado"])
	plot_med(voreg, "e2_tp1_carac_salida_med.csv")
	plt.legend(["Calculado", "Simulado", "Medido"])

	plt.minorticks_on()
	plt.grid(which='major', linestyle='-', linewidth=0.3, color='black')
	plt.grid(which='minor', linestyle=':', linewidth=0.1, color='black')

	plt.xlabel("Corriente de salida (A)")
	plt.ylabel("Tensión de salida (V)")
	#plt.legend('Calculado', 'Simulado', 'Medido')
	plt.show()
	#fig.savefig("e2_tp1_carac_salida_"+str(voreg), dpi=300)

plot_all(9)
plot_all(12)
plot_all(15)
plt.show()
