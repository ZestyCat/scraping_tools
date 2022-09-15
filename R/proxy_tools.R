library(httr)
library(rvest)

get_free_proxy_list <- function(n = 25, country = "US", https = TRUE) {
    url <- "https://www.free-proxy-list.net/"
    html <- read_html(url)
    table <- html_table(html)[[1]]
    names(table) <- c("ip", "port", "code", "country", "anonymity",
                      "google", "https", "last checked")
    if (https) {
        table <- table[table$https == "yes", ]
    }
    if (!is.null(country)) {
        table <- table[table$code == country, ]
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

rotate_GET <- function(proxies, url, ...) {
    while (TRUE) {
        p <- sample(seq_len(nrow(proxies)), 1)
        ip <- proxies[p, ]$ip
        port <- as.numeric(proxies[p, ]$port)
        tryCatch({
            message(sprintf("using proxy %s to access %s...", ip, url))
            response <- proxy_GET(url, ip, port, ...) # try getting resource
            if (response["status_code"] > 400) {
                stop(sprintf("received %s \n", response["status_code"]))
            }
            message(sprintf("successfully retrieved %s", url))
            break
        }, error = function(cond) {
            message(sprintf("request failed with message %s: ", cond))
        })
    }
    return(response)
}
