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

allwords_fun<- function(llist) {
  allwords_fun1<- function(lllist) {
    return(c(lllist$name, lllist$words))
  }
  return(lapply(llist, allwords_fun1))
}
doc_allwords<- lapply(doc_corpus, allwords_fun)

vocab_fun<- function(llist) {
  vocab<- c()
  n<- length(llist)
  for(i in 1:n){
    vocab<- c(vocab,llist[[i]])
  }
  vocab<- unique(vocab)
  return(vocab)
}
vocab<- lapply(doc_allwords, vocab_fun)

index<- function(x,a) {return(which(a==x))}
doc_format<- vector("list", 14)
for(i in 1:14) {
  format_fun<- function(lllist) {
    t<- table(lllist)
    vec1<- sapply(names(t), index, a=vocab[[i]])-1
    vec2<- as.numeric(t)
    m<- matrix(as.integer(c(vec1, vec2)), ncol = 2)
    return(t(m))
  }
  doc_format[[i]] <- lapply(doc_allwords[[i]], format_fun)
}
names(doc_format)<- query.list

k<- 10
try<- lda.collapsed.gibbs.sampler(doc_format$`A Gupta`,k, vocab$`A Gupta`,
                            num.iterations = 500, alpha = k/50, eta = 0.01)











