library(rvest)
library(httr)
library(tidyverse)

user_agent("Mozilla/5.0 (Windows NT 10.0; rv:104.0) Gecko/20100101 Firefox/104.0")

blog_url <- "https://becomingminimalist.com/"

pages <- 15

for (page in 10:pages) {

    # access the page
    page <- read_html(paste0(blog_url, "page", page))

    # get every post link on the page
    post_links <- page %>% html_elements("a.entry-title-link") %>%
        html_attr("href")
    
    for (link in post_links) {

        # open the page
        page <- read_html(link)
        
        # get title
        title <- page %>% html_element("h1.entry-title") %>%
            html_text()
        
        # get author
        author <- page %>% html_element("span.entry-author-name") %>%
            html_text()
        
        # get number of comments
        n_comments <- page %>% html_element("span.entry-comments-link") %>%
            html_element("a") %>% 
            html_text()

        # get post body, removing newline characters
        content <- paste(gsub("[\r\n]", "", page %>% 
                        html_element("div.entry-content") %>%
                        html_elements("p") %>%
                        html_text()), collapse = " ")

        # write the data line by line
        write_csv(data.frame(title, author, link, n_comments, content),
                  "blogposts.csv",
                  append = TRUE)
    }
}
