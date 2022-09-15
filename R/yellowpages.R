library(httr)
library(rvest)
source("R/proxy_tools.R")

proxies <- get_free_proxy_list(n = 25)

yp <- "https://www.yellowpages.com/search?search_terms=%s&geo_location_terms=%s"
states <- state.abb
search <- "hotels"

leads <- data.frame(name = c(), link = c(), phone = c(), addr = c(), loc = c())
for (state in states) {
    tryCatch({
        print(paste("getting data for", state))
        url <- sprintf(yp, search, state)
        resp <- rotate_GET(proxies, url)
        html <- read_html(resp)
        cards <- html_elements(html, "div.v-card")

        for (card in cards) {
            business <- data.frame(
                name = html_element(card, "a.business-name")
                %>% html_text(),
                phone = html_element(card, "div.phone")
                %>% html_text(),
                addr = html_element(card, "div.street-address")
                %>% html_text(),
                loc = html_element(card, "div.locality")
                %>% html_text(),
                link = html_element(card, "a.track-visit-website")
                %>% html_attr("href")
            )
            leads <- rbind(leads, business)
        }
    }, error = function(cond) {
        print(cond)
    })
}

leads <- leads[!is.na(leads$addr), ]
leads <- leads[!grepl("Holiday Inn", leads$name)]
write.csv(leads, "./data/lodging_leads.csv")
