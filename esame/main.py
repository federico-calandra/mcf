import rossi
import numpy as np

# rossi.evolve()
print('n_part = '+str(rossi.n_part))
print('en_ion = '+str(rossi.en_ion))

print(np.sum(rossi.en_ion))
