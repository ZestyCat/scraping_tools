library(httr)
library(rvest)

get_freeproxylist_proxies <- function() {
    url <- "https://www.freeproxylists.net/"
}

get_spys_proxies <- function(url = "https://spys.me/proxy.txt") {
    proxies <- readLines(url)[7:406]
    split <- strsplit(proxies, ":| ")
    df <- as.data.frame(do.call(rbind, split))
    names(df) <- c("ip", "port", "country-anonymity-ssl", "google_passed")
    return(df)
}

proxy_GET <- function(url, proxy_ip, proxy_port, timeout = 3, ...) {
    page <- httr::GET(
                url,
                httr::use_proxy(proxy_ip, proxy_port),
                timeout(timeout),
                ...
    )
    return(page)
}


find_good_proxies <- function(proxies, test = "https://httpbin.org/get", ...) {
    good_proxies <- c()
    for (p in seq_len(nrow(proxies))) {
        ip <- proxies[p, ]$ip
        port <- as.numeric(proxies[p, ]$port)
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

rotate_proxies <- function(proxies, urls, callback, ...) {
    for (p in seq_len(nrow(proxies))) { # loop through proxies
        ip <- proxies[p, ]$ip
        port <- as.numeric(proxies[p, ]$port)
        tryCatch({
            for (url in urls) {
                message(sprintf("using proxy %s to access %s...", ip, url))
                page <- proxy_GET(url, ip, port, ...) # try getting resource
                message(sprintf("successfully retrieved %s", url))
                match.fun(callback)(page) # run the callback
                message("callback success")
                urls <- urls[!urls %in% url] # dont get the same url twice
            }
        }, error = function(cond) {
            message(sprintf("request failed with message %s: ", cond))
        })
    }
}

if (!interactive()) {
    proxies <- get_spys_proxies()
    filename <- sprintf("proxies/good_proxies_%s.csv", Sys.Date())
    good <- find_good_proxies(proxies)
    write.csv(good[2:5], filename)
}
