
def sigma_ewma(
	prev_sigma2: float,
	current_return: float,
	lam: float = 0.94
	)-> float:

   sigma2 = lam * prev_sigma2 + ( 1 - lam ) * current_return ** 2 

   return sigma2