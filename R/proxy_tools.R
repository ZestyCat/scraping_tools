library(httr)
library(rvest)

get_free_proxy_list <- function(n = 25, https = TRUE) {
    url <- "https://www.free-proxy-list.net/"
    html <- read_html(url)
    table <- html_table(html)[[1]]
    names(table) <- c("ip", "port", "code", "country", "anonymity",
                      "google", "https", "last checked")
    if (https) {
        table <- table[table$https == "yes", ]
    }
    return(table[1:n, ])
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


find_good_proxies <- function(proxies, test = "https://httpbin.org/get",
                              https = TRUE, ...) {
    if (https == TRUE) {
        tryCatch({
            proxies <- proxies[proxies["https"] == "yes", ]
        }, error = function(cond) {
            stop("proxy dataframe must have 'https' column")
        })
    }
    good_proxies <- c()
    for (p in seq_len(nrow(proxies))) {
        ip <- proxies[p, ]$ip
        port <- as.numeric(proxies[p, ]$port)
        tryCatch({
            message(sprintf("trying proxy %s https: %s",
                            ip, proxies[p, ]$https))
            proxy_GET(test, ip, port, ...)
            message("proxy passed timeout test")
            good_proxies <- append(good_proxies, p)
        }, error = function(cond) {
            message("proxy failed timeout test")
        })
    }
    return(proxies[good_proxies, ])
}

rotate_proxies <- function(proxies, url, callback, ...) {
    while (TRUE) {
        p <- sample(seq_len(nrow(proxies)), 1)
        ip <- proxies[p, ]$ip
        port <- as.numeric(proxies[p, ]$port)
        tryCatch({
            message(sprintf("using proxy %s to access %s...", ip, url))
            page <- proxy_GET(url, ip, port, ...) # try getting resource
            message(sprintf("successfully retrieved %s", url))
            match.fun(callback)(page) # run the callback
            message("callback success")
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
