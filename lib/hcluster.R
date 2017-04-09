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

# Calculate topic-word matrix
h <- try$topics
W <- length(vocab$`A Gupta`)
beta <- 0.01
a <- matrix(NA,nrow=k,ncol=W)
sum_h <- rowSums(h)
matrix_sumh <- matrix(rep(sum_h,k),nrow=k,ncol=W)
a <- (h+beta)/(matrix_sumh+W*beta)

# Calculate topic-document matrix
hd <- try$document_sums
alpha <- k/50
D <- length(doc_format$`A Gupta`)
theta <- matrix(NA,nrow=k,ncol=D)
sum_hd <- colSums(hd)
matrix_sumhd <- matrix(rep(sum_hd,each=k),nrow=k,ncol=D)
theta <- (hd+alpha)/(matrix_sumhd+k*alpha)

# Agglomerative Clustering
topic_document <- data.frame(t(theta))
hcluster <- hclust(dist(topic_document), "complete")
plot(hcluster, hang = -1)
