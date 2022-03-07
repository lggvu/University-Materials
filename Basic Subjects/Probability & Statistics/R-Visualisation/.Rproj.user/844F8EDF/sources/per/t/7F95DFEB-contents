### population of exponential distribution
lambda = .5
n <- 10000
N <- 1000

mu <- 1/lambda
sigma <- 1/lambda  # sqrt of variance

for (i in 1:N) {
        x <- rexp(n, rate=lambda)
        x_bar[i] <- sum(x)/n
        
}

hist(x_bar, prob=T, breaks=50)
lines(density(x_bar),col='red')

# z <- (x_bar-mean(x_bar))/(sigma / sqrt(n))
z <- (x_bar - mu) / (sigma / sqrt(n))
hist(z, prob=T, breaks=100, main='Sampling distribution of z')

lines(density(z), col='blue')
 # mean should be 0, var should be 1