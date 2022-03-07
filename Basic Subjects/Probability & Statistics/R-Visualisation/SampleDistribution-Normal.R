n <- 10000  # sample size, the more the better
# population is normal distribution
mu <- 5
sigma <- 2

N <- 1000  # iterations
x_bar <- rep(0, N)

for (i in 1:N) {
        x <- rnorm(n, mean=mu, sd=sigma)
        x_bar[i] <- sum(x)/n
}

hist(x_bar, breaks = 50, probability = T)
mean(x_bar)  # close to 5
var(x_bar)  # close 0.4
lines(density(x_bar), col='red')
