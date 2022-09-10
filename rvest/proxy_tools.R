library(httr)

download_proxies <- function(url = "https://spys.me/proxy.txt") {
    proxies <- readLines(url)[7:406]
    split <- strsplit(proxies, ":| ")
    df <- as.data.frame(do.call(rbind, split))
    names(df) <- c("ip", "port", "country-anonymity-ssl", "google_passed")
    return(df)
}

proxy_GET <- function(url, proxy_ip, proxy_port, timeout = 3) {
    page <- httr::content(
        httr::GET(
            url,
            httr::use_proxy(proxy_ip, proxy_port),
            timeout(timeout)
        )
    )
    return(page)
}


find_good_proxies <- function(proxies, test = "https://httpbin.org/get", ...) {
    good_proxies <- c()
    for (p in seq_len(nrow(proxies))) {
        ip <- proxies[p, 2]
        port <- proxies[p, 3]
        tryCatch({
            proxy_GET(test, ip, port, ...)
            message("proxy passed timeout test")
            good_proxies <- append(good_proxies, p)
        }, error = function(cond) {
            message("proxy failed timeout test")
        })
    }
    return(proxies[good_proxies, ])
}

proxies <- read.csv("./proxies.csv")
filename <- sprintf("good_proxies_%s.csv", Sys.Date())
good <- find_good_proxies(proxies)
write.csv(good, filename)
