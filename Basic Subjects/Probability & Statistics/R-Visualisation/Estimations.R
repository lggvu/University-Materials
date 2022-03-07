## Estimation
# 1. Normal Distribution
mu = 5
sigma = 2
n = 200

x <- rnorm(n, mean=mu, sd=sigma)
x
summary(x)
mean(x)
sd(x)
hist(x, prob=T, breaks=20, col='blue', border='white', xlim=c(-1, 11))

