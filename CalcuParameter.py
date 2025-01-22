import numpy as np
'''
Where, 𝜎_𝑌is the yield stress (306 N/mm2), 
𝐸 is Young’s modulus (205,000 N/mm2), 
and 𝜈 is Poisson’s ratio (0.3). 
The breadth of plate, thickness of plate, t is 12 mm. 
The buckling coefficient of a projection panel, k is 0.425.
'''
b1 = 300 # model setting plate width-high
b2 = 300 # model setting plate width
t = 12 # thickness
v = 0.3 # Poisson's ratio
thetaY = 306 # Base Plate Yield Stress  (295 N/mm2)
E = 205000 # Young’s modulus (205,000 N/mm2)
k1 = 4 # 4-simply supported
k2 = 0.425 # 3-simply supported + 1-free
# slenderness parameter λ (this research also called Width-Thickness Ratio Parameter R)


R1 = (1 / np.pi) * (b1 / t) * (((12 * (1 - v**2))/ k1) * (thetaY / E)) ** 0.5

R2 = (1 / np.pi) * (b2 / t) * (((12 * (1 - v**2))/ k2) * (thetaY / E)) ** 0.5

# print("R1: "+ str(R1))
print("R2: "+ str(R2))