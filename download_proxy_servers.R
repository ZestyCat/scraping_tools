# Download from spys.me
url <- "https://spys.me/proxy.txt"

proxies <- readLines(url)[7:406]

split <- strsplit(proxies, ":| ")

df <- as.data.frame(do.call(rbind, split))

names(df) <- c("ip", "port", "country-anonymity-ssl", "google_passed")

write.csv(df, "~/Fiverr/templates/proxies.csv")
