library(lda)
source("cleandata.R")

corpus<- function(llist){
  
  document<- function(lllist) {
    words_apperance <- c(unlist(strsplit(lllist[[4]], " ")), unlist(strsplit(lllist[[5]], " ")))
    name_appearance <- unlist(lllist[[3]])
    doc <- list(words = words_apperance, name = name_appearance)
    return(doc)
  }
  
  return(lapply(llist, document))
}

doc_corpus<- lapply(data_list, corpus)

# arthor_name<- substring(names(lllist)[1], 1, nchar(names(lllist)[1])-2)


