from sklearn.preprocessing import StandardScaler
#apply standard scaling to a spectrum (mean center and divide each bin by the standard deviation of that bin)
def standard_scale(self, col):
    self.df[col] = StandardScaler().fit_transform(self.df[col])
